# 🚀 StudyBuddy DK - Quick Start Guide

## ⏱️ 30 Second Setup

### Step 1: Make sure you're in the right folder
```bash
cd /path/to/studybuddy-dk
```

### Step 2: Activate the Python environment
**Windows:**
```bash
venv311\Scripts\activate
```

**Mac/Linux:**
```bash
source venv311/bin/activate
```

### Step 3: Start the full system
**Windows:**
```bash
run.bat
```

**Mac/Linux:**
```bash
bash run.sh
```

## 🌐 Access the System

### Frontend (Streamlit)
- **URL:** http://localhost:8501
- **Purpose:** Interactive student profile analyzer
- **Features:** Program finder, program explorer, system monitoring

### Backend (FastAPI)
- **URL:** http://127.0.0.1:8000
- **Purpose:** REST API for pipeline execution
- **Docs:** http://127.0.0.1:8000/docs (Swagger UI)

### MLflow Tracking
- **URL:** http://127.0.0.1:5000
- **Purpose:** View experiment runs and artifacts
- **Run this separately:** `mlflow ui --backend-store-uri sqlite:///mlflow.db`

---

## 📝 What Each Service Does

### FastAPI (api.py)
- Accepts POST requests with student profiles
- Runs the 3-agent pipeline
- Returns program matches, gaps, costs, deadlines
- Serves data endpoints (/programs, /courses, /rates)

### Streamlit (app.py)
- Beautiful interactive dashboard
- Input student profile with sliders/dropdowns
- Display results with tabs
- Filter/explore all 17 programs
- Monitor system health

### Database (database.py)
- SQLite with 4 tables
- 17 programs from 6 universities
- 12 gap-filling courses
- Exchange rates history
- Pipeline run logs

### Pipeline (pipeline.py)
- Orchestrates all 3 agents
- Agent 1: Profile + Matching + Eligibility
- Agent 2: Gap Analysis + Costs + Deadlines
- Agent 3: Monitoring + Drift Detection
- Logs to MLflow

---

## 🧪 Test It

### Option A: Using Streamlit (Easiest)
1. Open http://localhost:8501
2. Fill in your profile:
   - Name: "Alina Shrestha"
   - Degree: "BBA Finance"
   - ECTS: 60 business, 30 quantitative, 0 programming, 30 research
   - IELTS: 6.5
   - Country: Nepal
3. Click "Find My Programs"
4. See your personalized recommendations!

### Option B: Using Swagger API Docs (Technical)
1. Open http://127.0.0.1:8000/docs
2. Click "POST /analyse"
3. Click "Try it out"
4. Paste this JSON:
```json
{
  "name": "Alina Shrestha",
  "degree": "BBA Finance",
  "ects_business": 60,
  "ects_quantitative": 30,
  "ects_programming": 0,
  "ects_research": 30,
  "ielts": 6.5,
  "country": "Nepal",
  "eu_student": false
}
```
5. Click "Execute"
6. See the JSON response with all recommendations

### Option C: Using curl (Command Line)
```bash
curl -X POST http://127.0.0.1:8000/analyse \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alina Shrestha",
    "degree": "BBA Finance",
    "ects_business": 60,
    "ects_quantitative": 30,
    "ects_programming": 0,
    "ects_research": 30,
    "ielts": 6.5,
    "country": "Nepal",
    "eu_student": false
  }'
```

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
# Make sure venv311 is activated and reinstall
pip install fastapi uvicorn streamlit requests pandas mlflow langchain langchain-openai beautifulsoup4
```

### "Port already in use" error
```bash
# Windows
taskkill /PID <PID> /F

# Mac/Linux
kill -9 <PID>
```

### "Cannot connect to API" from Streamlit
1. Make sure FastAPI is running (check terminal 1)
2. Wait 3 seconds for FastAPI to start
3. Refresh the Streamlit page (http://localhost:8501)

### Database error
```bash
# Reinitialize database
python database.py

# Reload data
python load_data.py

# Then start the system again
run.bat  # or bash run.sh
```

---

## 📂 Key Files

| File | Purpose | Lines |
|------|---------|-------|
| api.py | FastAPI backend with REST endpoints | 282 |
| app.py | Streamlit frontend dashboard | 450+ |
| pipeline.py | 3-agent orchestration | 100+ |
| database.py | SQLite database management | 250+ |
| agents/agent1_profile_matching.py | Agent 1 logic | 180+ |
| agents/agent2_gap_preparation.py | Agent 2 logic | 220+ |
| agents/agent3_monitoring.py | Agent 3 logic | 200+ |
| **Total** | **Complete MLOps System** | **~1,800** |

---

## 🎯 What You Can Do

With the full system running, you can:

### As a Student
✅ Enter your academic profile  
✅ Get personalized program recommendations  
✅ See which skills you're missing  
✅ Find courses to fill gaps  
✅ Calculate costs in your home currency  
✅ Know how many days until deadline  

### As a System Admin
✅ Monitor API health  
✅ View database statistics  
✅ Check monitoring alerts  
✅ See exchange rate drift  
✅ Review CBS requirement changes  
✅ Analyze pipeline performance  

### As a Developer
✅ Access REST API with Swagger docs  
✅ View experiment runs in MLflow  
✅ Inspect database directly  
✅ Extend agents with custom logic  
✅ Add more data sources  
✅ Deploy to production  

---

## 📊 System Architecture

```
Student Input
    ↓
FastAPI (/analyse endpoint)
    ↓
Pipeline Orchestrator
    ↓
Agent 1: Profile + Matching + Eligibility
    ↓
Agent 2: Gap Analysis + Costs + Deadlines
    ↓
Agent 3: Monitoring + Drift Detection
    ↓
SQLite Database (logs)
    ↓
MLflow (artifacts + metrics)
    ↓
Streamlit Dashboard (display results)
```

---

## ✨ Features

### Data Layer
- 17 Danish master programs (CBS, DTU, KU, AAU, AU, SDU)
- 12 gap-filling courses (Coursera, Udemy, edX)
- Live exchange rates (5 currencies)
- Automatic deadline countdowns
- CBS requirement monitoring

### Processing Layer
- **Agent 1:** Cosine similarity matching algorithm
- **Agent 2:** Gap identification + course recommendations
- **Agent 3:** Drift detection + change monitoring

### Deployment Layer
- REST API (FastAPI + Uvicorn)
- Interactive Dashboard (Streamlit)
- Experiment Tracking (MLflow)
- Database Persistence (SQLite)

### Monitoring
- Exchange rate drift detection (>5% threshold)
- CBS requirement change detection
- Pipeline performance metrics
- Full artifact logging

---

## 🔗 Useful Links

- **Frontend:** http://localhost:8501
- **API Docs (Swagger):** http://127.0.0.1:8000/docs
- **API Docs (ReDoc):** http://127.0.0.1:8000/redoc
- **MLflow Dashboard:** http://127.0.0.1:5000
- **API Health:** http://127.0.0.1:8000/health

---

## 🎓 Learning Resources

- **API Docs**: See /docs or /redoc while API is running
- **Database**: studybuddy.db (open with SQLite viewer)
- **Code**: agents/ folder for 3-agent logic
- **Data**: data/static/ folder for source datasets
- **Logs**: MLflow for full run history with artifacts

---

## ⏰ Performance

- Pipeline execution: **~4 seconds per student**
- API response: **~4 seconds** (includes pipeline + overhead)
- Streamlit rendering: **instant**
- Database queries: **<100ms**
- Exchange rate fetch: **<1 second**
- MLflow logging: **<500ms**

---

## 🚀 You're Ready!

Everything is set up and ready to go. Just run:

```bash
run.bat  # Windows
# or
bash run.sh  # Mac/Linux
```

Then visit **http://localhost:8501** and start finding your perfect Danish master's program! 🎓

---

**Questions?** Check FRONTEND_GUIDE.md for detailed documentation.
