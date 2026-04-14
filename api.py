"""
StudyBuddy DK — FastAPI Backend
Provides REST endpoint for pipeline execution
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
import sys
import os
from datetime import datetime

# Add parent directory to path so we can import agents and database
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline import run_pipeline
from database import get_connection

# ===== PYDANTIC MODELS =====

class StudentInput(BaseModel):
    """Student profile input for analysis"""
    name: str
    degree: str
    ects_business: float
    ects_quantitative: float
    ects_programming: float
    ects_research: float
    ielts: float
    country: str
    eu_student: bool = False

# ===== FASTAPI APP =====

app = FastAPI(
    title="StudyBuddy DK API",
    description="AI-powered Danish master's program finder for international students",
    version="1.0.0"
)

# Add CORS middleware to allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== ROUTES =====

@app.get("/")
async def root():
    """Health check and API info"""
    return {
        "service": "StudyBuddy DK API",
        "status": "✅ Running",
        "version": "1.0.0",
        "endpoints": {
            "POST /analyse": "Run full pipeline with student profile",
            "GET /programs": "List all available programs",
            "GET /courses": "List all available courses",
            "GET /exchange-rates": "Get latest exchange rates",
            "GET /health": "Health check"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "✅ Healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/programs")
async def get_programs():
    """Get all available programs"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM programs")
        columns = [description[0] for description in cursor.description]
        programs = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return {
            "count": len(programs),
            "programs": programs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/courses")
async def get_courses():
    """Get all available gap-filling courses"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses")
        columns = [description[0] for description in cursor.description]
        courses = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return {
            "count": len(courses),
            "courses": courses
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/exchange-rates")
async def get_exchange_rates():
    """Get latest exchange rates"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM exchange_rates 
            ORDER BY date DESC 
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()

        if not row:
            return {"status": "No exchange rates found"}

        columns = [description[0] for description in cursor.description]
        rates = dict(zip(columns, row))
        return {"latest_rates": rates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyse")
async def analyse_student(student: StudentInput):
    """
    Run full pipeline with student profile.
    Returns program matches, gap analysis, costs, deadlines, and monitoring alerts.
    """
    try:
        student_input = student.dict()

        print(f"\n{'='*60}")
        print(f"API REQUEST: /analyse")
        print(f"Student: {student_input['name']}")
        print(f"{'='*60}\n")

        # Run pipeline
        result = run_pipeline(student_input)

        # ── Map pipeline keys → API response ──
        # Pipeline returns: top3_matches, gaps, recommendations,
        #                   costs (dict), deadlines, monitoring, run_duration_s
        top3    = result.get("top3_matches", [])
        monitor = result.get("monitoring", {})
        alerts  = monitor.get("alerts", []) if isinstance(monitor, dict) else []

        response = {
            "student_name":    result.get("student_name"),
            "student_degree":  result.get("profile", {}).get("degree", ""),
            "student_country": result.get("profile", {}).get("country", ""),
            "top_programs":    top3,
            "gaps":            result.get("gaps", []),
            "recommendations": result.get("recommendations", []),
            "costs":           result.get("costs", {}),
            "deadlines":       result.get("deadlines", []),
            "monitoring_alerts": alerts,
            "runtime_seconds": float(result.get("run_duration_s", 0)),
            "timestamp":       datetime.now().isoformat()
        }

        print(f"\n✅ API RESPONSE: Pipeline completed successfully")
        print(f"   Top program: {top3[0]['program_name'] if top3 else 'None'}")
        print(f"   Gaps found:  {len(response['gaps'])}")
        print(f"   Runtime:     {response['runtime_seconds']:.2f}s\n")

        return response

    except Exception as e:
        print(f"\n❌ API ERROR: {str(e)}\n")
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline execution failed: {str(e)}"
        )

@app.get("/monitoring-alerts")
async def get_monitoring_alerts():
    """Get latest monitoring alerts"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM monitoring_alerts 
            ORDER BY timestamp DESC 
            LIMIT 10
        """)
        columns = [description[0] for description in cursor.description]
        alerts = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return {
            "count": len(alerts),
            "alerts": alerts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pipeline-runs")
async def get_pipeline_runs():
    """Get recent pipeline runs"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM pipeline_runs 
            ORDER BY created_at DESC 
            LIMIT 20
        """)
        columns = [description[0] for description in cursor.description]
        runs = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return {
            "count": len(runs),
            "runs": runs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== STARTUP MESSAGE =====

@app.on_event("startup")
async def startup_event():
    print("\n" + "="*60)
    print("  🚀 StudyBuddy DK API — FastAPI Backend")
    print("="*60)
    print("✅ Server running at http://127.0.0.1:8000")
    print("📚 Documentation at http://127.0.0.1:8000/docs")
    print("🔌 Ready to process student profiles")
    print("="*60 + "\n")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )