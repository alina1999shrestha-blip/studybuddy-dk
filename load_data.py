import json
import requests
from datetime import datetime, date

# ── Load static programs ──────────────────────────────────────────────────────
with open("data/static/programs.json", "r") as f:
    programs = json.load(f)

# ── Load static courses ───────────────────────────────────────────────────────
with open("data/static/courses.json", "r") as f:
    courses = json.load(f)

print("=" * 55)
print("  STUDYBUDDY DK — DATA LOADED SUCCESSFULLY")
print("=" * 55)

# ── Show programs ─────────────────────────────────────────────────────────────
print(f"\n✅ {len(programs)} programs loaded from 6 Danish universities\n")
for i, p in enumerate(programs, 1):
    print(f"  {i:2}. {p['name']} — {p['university_full']}")

# ── Show courses ──────────────────────────────────────────────────────────────
print(f"\n✅ {len(courses)} gap-filling courses loaded\n")
skills = list(set(c["skill"] for c in courses))
for s in skills:
    skill_courses = [c for c in courses if c["skill"] == s]
    print(f"  {s}: {len(skill_courses)} course(s) available")

# ── Fetch live exchange rates ─────────────────────────────────────────────────
print("\n" + "=" * 55)
print("  LIVE EXCHANGE RATES — fetched from frankfurter.app")
print("=" * 55)

try:
    # frankfurter.app does not support NPR — fetch NPR separately
    response = requests.get(
        "https://api.frankfurter.app/latest?from=DKK&to=INR,USD,EUR,GBP",
        timeout=5
    )
    data = response.json()
    rates = data["rates"]

    # Fetch NPR rate separately from exchangerate-api
    npr_response = requests.get(
        "https://open.er-api.com/v6/latest/DKK",
        timeout=5
    )
    npr_data = npr_response.json()
    npr_rate = npr_data["rates"].get("NPR", 0)
    eur_rate = float(rates.get("EUR", 0))
    rates["NPR"] = npr_rate

    # Fetch EUR to NPR
    eur_npr_response = requests.get(
        "https://open.er-api.com/v6/latest/EUR",
        timeout=5
    )
    eur_npr_data = eur_npr_response.json()
    eur_to_npr = eur_npr_data["rates"].get("NPR", 0)

    print(f"\n✅ Exchange rates fetched successfully ({data['date']})\n")
    print(f"  1 DKK = {float(rates.get('INR', 0)):.2f} INR  (Indian Rupee)")
    print(f"  1 DKK = {float(npr_rate):.2f} NPR  (Nepali Rupee)")
    print(f"  1 DKK = {float(rates.get('USD', 0)):.4f} USD  (US Dollar)")
    print(f"  1 DKK = {float(rates.get('EUR', 0)):.4f} EUR  (Euro)")
    print(f"  1 DKK = {float(rates.get('GBP', 0)):.4f} GBP  (British Pound)")
    print(f"  1 EUR = {float(eur_to_npr):.2f} NPR  (Euro to Nepali Rupee)")

    # Show tuition in NPR for top program
    top = programs[0]
    tuition_dkk = top["tuition_non_eu_dkk"]
    tuition_npr = tuition_dkk * float(npr_rate)
    tuition_inr = tuition_dkk * float(rates.get("INR", 0))
    print(f"\n  Example: {top['name']} tuition")
    print(f"  {tuition_dkk:,} DKK/year = {tuition_npr:,.0f} NPR/year")
    print(f"  {tuition_dkk:,} DKK/year = {tuition_inr:,.0f} INR/year")

except Exception as e:
    print(f"⚠️  Could not fetch live rates — using offline mode ({e})")

# ── Deadline countdown ────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("  DEADLINE COUNTDOWN — calculated today")
print("=" * 55)
today = date.today()
print(f"\n  Today: {today}\n")

for p in programs[:5]:
    deadline_str = p.get("deadline_non_eu_september") or p.get("deadline_september")
    if deadline_str:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        days_left = (deadline - today).days
        flag = "🔴 URGENT" if days_left < 60 else "🟡 Soon" if days_left < 180 else "✅ On track"
        print(f"  {p['university']} {p['name'][:30]:<30} → {days_left} days  {flag}")

print("\n" + "=" * 55)
print("  ✅ PIPELINE READY — StudyBuddy DK")
print("=" * 55)