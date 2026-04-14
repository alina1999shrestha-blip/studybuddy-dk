import json
import requests
import sqlite3
from datetime import datetime, date
from database import (get_connection, get_latest_exchange_rate,
                      save_exchange_rate, log_pipeline_run)

DRIFT_THRESHOLD = 0.05  # 5% change triggers alert

def fetch_fresh_exchange_rates() -> dict:
    """Fetch latest exchange rates from APIs."""
    try:
        r1 = requests.get(
            "https://api.frankfurter.app/latest?from=DKK&to=INR,USD,EUR,GBP",
            timeout=5
        ).json()
        r2 = requests.get(
            "https://open.er-api.com/v6/latest/DKK", timeout=5
        ).json()
        r3 = requests.get(
            "https://open.er-api.com/v6/latest/EUR", timeout=5
        ).json()
        return {
            "date":        r1["date"],
            "dkk_to_inr":  r1["rates"]["INR"],
            "dkk_to_npr":  r2["rates"]["NPR"],
            "dkk_to_usd":  r1["rates"]["USD"],
            "dkk_to_eur":  r1["rates"]["EUR"],
            "dkk_to_gbp":  r1["rates"]["GBP"],
            "eur_to_npr":  r3["rates"]["NPR"],
        }
    except Exception as e:
        return None

def check_exchange_rate_drift(old: dict, new: dict) -> list:
    """Compare old vs new rates. Flag if change > 5%."""
    alerts = []
    pairs = [
        ("dkk_to_inr", "DKK/INR"),
        ("dkk_to_npr", "DKK/NPR"),
        ("dkk_to_usd", "DKK/USD"),
        ("dkk_to_eur", "DKK/EUR"),
    ]
    for key, label in pairs:
        old_val = old.get(key) or 0
        new_val = new.get(key) or 0
        if old_val > 0:
            change = abs(new_val - old_val) / old_val
            if change > DRIFT_THRESHOLD:
                direction = "up" if new_val > old_val else "down"
                alerts.append({
                    "type":       "exchange_rate_drift",
                    "pair":       label,
                    "old_value":  round(old_val, 4),
                    "new_value":  round(new_val, 4),
                    "change_pct": round(change * 100, 2),
                    "direction":  direction,
                    "severity":   "high" if change > 0.10 else "medium",
                    "message":    f"{label} changed {round(change*100,2)}% {direction} ({round(old_val,4)} → {round(new_val,4)})"
                })
    return alerts

def check_cbs_requirements() -> list:
    """
    Scrape CBS page and compare key fields against stored data.
    Only flags changes if scraped IELTS is a valid score (4.0 - 9.0).
    Returns list of change alerts.
    """
    alerts = []
    try:
        from bs4 import BeautifulSoup
        import re

        url = "https://www.cbs.dk/en/study/graduate/msc-in-business-administration-and-data-science"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True).lower()

        # Get stored IELTS from database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ielts_min FROM programs WHERE id = 'cbs_bds'")
        row = cursor.fetchone()
        conn.close()

        stored_ielts = row[0] if row else 6.5

        # ── FIXED: Only accept valid IELTS scores between 4.0 and 9.0 ──
        # This prevents false positives from page numbers, course codes, etc.
        ielts_matches = re.findall(r"ielts[^\d]*(\d+\.?\d*)", text)
        valid_ielts = [
            float(m) for m in ielts_matches
            if 4.0 <= float(m) <= 9.0
        ]

        if valid_ielts:
            scraped_ielts = valid_ielts[0]
            if scraped_ielts != stored_ielts:
                alerts.append({
                    "type":      "requirement_change",
                    "program":   "CBS MSc BDS",
                    "field":     "IELTS minimum",
                    "old_value": stored_ielts,
                    "new_value": scraped_ielts,
                    "severity":  "high",
                    "message":   f"CBS IELTS requirement changed from {stored_ielts} to {scraped_ielts}"
                })

        # Always log a successful scrape
        alerts.append({
            "type":     "scrape_success",
            "program":  "CBS MSc BDS",
            "message":  "CBS page scraped successfully — no changes detected",
            "severity": "info"
        })

    except Exception as e:
        alerts.append({
            "type":     "scrape_failed",
            "program":  "CBS",
            "message":  f"CBS scrape failed — using static data. Error: {str(e)[:50]}",
            "severity": "low"
        })
    return alerts

def save_monitoring_alerts(alerts: list):
    """Save all alerts to database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_type TEXT,
            severity TEXT,
            message TEXT,
            details TEXT,
            created_at TEXT
        )
    """)
    for alert in alerts:
        cursor.execute("""
            INSERT INTO monitoring_alerts
            (alert_type, severity, message, details, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            alert.get("type"),
            alert.get("severity"),
            alert.get("message", str(alert)),
            json.dumps(alert),
            datetime.utcnow().isoformat()
        ))
    conn.commit()
    conn.close()

def run_agent3() -> dict:
    """
    Main Agent 3 function.
    Checks exchange rate drift and CBS requirement changes.
    Logs everything to database.
    """
    print("\n🤖 Agent 3 — Monitoring")
    print("-" * 40)

    all_alerts = []

    # ── Step 1: Fetch fresh exchange rates ──
    print("🔍 Fetching latest exchange rates...")
    new_rates = fetch_fresh_exchange_rates()

    if new_rates:
        old_rates = get_latest_exchange_rate()
        if old_rates:
            drift_alerts = check_exchange_rate_drift(old_rates, new_rates)
            if drift_alerts:
                for a in drift_alerts:
                    print(f"   🚨 DRIFT ALERT: {a['pair']} changed {a['change_pct']}% {a['direction']}")
                all_alerts.extend(drift_alerts)
            else:
                print(f"   ✅ Exchange rates stable — no significant drift")
        save_exchange_rate(new_rates)
        print(f"✅ Exchange rates saved to database")
        print(f"   ✅ Rates updated: 1 DKK = {new_rates['dkk_to_npr']:.2f} NPR")
    else:
        print("   ⚠️  Could not fetch rates — using cached data")

    # ── Step 2: Check CBS requirements ──
    print("\n🔍 Checking CBS program requirements...")
    cbs_alerts = check_cbs_requirements()
    for a in cbs_alerts:
        if a["severity"] == "high":
            print(f"   🚨 CHANGE DETECTED: {a['message']}")
        elif a["severity"] == "info":
            print(f"   ✅ {a['message']}")
        else:
            print(f"   ⚠️  {a['message']}")
    all_alerts.extend(cbs_alerts)

    # ── Step 3: Save all alerts ──
    save_monitoring_alerts(all_alerts)

    # ── Step 4: Log run ──
    high_alerts = [a for a in all_alerts if a.get("severity") == "high"]
    status = "alerts_found" if high_alerts else "success"
    log_pipeline_run(
        "agent3_monitoring",
        status,
        f"Total alerts: {len(all_alerts)} | High priority: {len(high_alerts)}"
    )

    print(f"\n✅ Monitoring complete")
    print(f"   Total alerts logged: {len(all_alerts)}")
    print(f"   High priority alerts: {len(high_alerts)}")

    return {
        "alerts":        all_alerts,
        "high_alerts":   high_alerts,
        "rates_updated": new_rates is not None
    }

if __name__ == "__main__":
    result = run_agent3()
    print("\n✅ Agent 3 complete")