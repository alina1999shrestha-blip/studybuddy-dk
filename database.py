import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "studybuddy.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Programs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS programs (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            university TEXT NOT NULL,
            university_full TEXT,
            url TEXT,
            ects_required INTEGER,
            ects_quantitative_min INTEGER,
            ects_business_min INTEGER,
            ects_programming_min INTEGER,
            ielts_min REAL,
            toefl_min INTEGER,
            deadline_september TEXT,
            deadline_non_eu_september TEXT,
            tuition_eu_dkk INTEGER,
            tuition_non_eu_dkk INTEGER,
            background_required TEXT,
            teaching_language TEXT,
            location TEXT,
            description TEXT,
            source TEXT,
            scraped_at TEXT
        )
    """)

    # Courses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id TEXT PRIMARY KEY,
            skill TEXT NOT NULL,
            course_name TEXT NOT NULL,
            platform TEXT,
            provider TEXT,
            duration_weeks INTEGER,
            cost TEXT,
            level TEXT,
            url TEXT,
            rating REAL
        )
    """)

    # Exchange rates table — stores history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exchange_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            dkk_to_inr REAL,
            dkk_to_npr REAL,
            dkk_to_usd REAL,
            dkk_to_eur REAL,
            dkk_to_gbp REAL,
            eur_to_npr REAL,
            fetched_at TEXT
        )
    """)

    # MLflow-style run log table
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_type TEXT,
                status TEXT,
                details TEXT,
                created_at TEXT
            )
        """)

    # User feedback table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating TEXT,
            comment TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database tables created")

def load_programs_to_db():
    with open("data/static/programs.json", "r") as f:
        programs = json.load(f)

    conn = get_connection()
    cursor = conn.cursor()

    count = 0
    for p in programs:
        cursor.execute("""
            INSERT OR REPLACE INTO programs VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, (
            p["id"], p["name"], p["university"], p.get("university_full"),
            p.get("url"), p.get("ects_required"), p.get("ects_quantitative_min"),
            p.get("ects_business_min"), p.get("ects_programming_min"),
            p.get("ielts_min"), p.get("toefl_min"),
            p.get("deadline_september"), p.get("deadline_non_eu_september"),
            p.get("tuition_eu_dkk"), p.get("tuition_non_eu_dkk"),
            json.dumps(p.get("background_required", [])),
            p.get("teaching_language"), p.get("location"),
            p.get("description"), p.get("source"), p.get("scraped_at")
        ))
        count += 1

    conn.commit()
    conn.close()
    print(f"✅ {count} programs saved to database")
    
def load_courses_to_db():
    with open("data/static/courses.json", "r") as f:
        courses = json.load(f)

    conn = get_connection()
    cursor = conn.cursor()

    count = 0
    for c in courses:
        cursor.execute("""
            INSERT OR REPLACE INTO courses VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, (
            c["id"], c["skill"], c["course_name"], c.get("platform"),
            c.get("provider"), c.get("duration_weeks"), c.get("cost"),
            c.get("level"), c.get("url"), c.get("rating")
        ))
        count += 1

    conn.commit()
    conn.close()
    print(f"✅ {count} courses saved to database")

def save_exchange_rate(rates: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO exchange_rates
        (date, dkk_to_inr, dkk_to_npr, dkk_to_usd, dkk_to_eur, dkk_to_gbp, eur_to_npr, fetched_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        rates.get("date"),
        rates.get("dkk_to_inr"),
        rates.get("dkk_to_npr"),
        rates.get("dkk_to_usd"),
        rates.get("dkk_to_eur"),
        rates.get("dkk_to_gbp"),
        rates.get("eur_to_npr"),
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()
    print(f"✅ Exchange rates saved to database")

def log_pipeline_run(run_type: str, status: str, details: str = ""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pipeline_runs (run_type, status, details, created_at)
        VALUES (?, ?, ?, ?)
    """, (run_type, status, details, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def get_all_programs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM programs")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_courses_for_skill(skill: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM courses WHERE LOWER(skill) = LOWER(?)", (skill,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_latest_exchange_rate():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM exchange_rates ORDER BY id DESC LIMIT 1"
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def save_feedback(rating: str, comment: str = ""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating TEXT,
            comment TEXT,
            created_at TEXT
        )
    """)
    cursor.execute(
        "INSERT INTO user_feedback (rating, comment, created_at) VALUES (?, ?, ?)",
        (rating, comment, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close() 

if __name__ == "__main__":
    print("=" * 50)
    print("  STUDYBUDDY DK — DATABASE SETUP")
    print("=" * 50)
    init_database()
    load_programs_to_db()
    load_courses_to_db()
    log_pipeline_run("database_setup", "success", "Initial data loaded")
    print("\n✅ Database ready — studybuddy.db created")
    print("=" * 50)