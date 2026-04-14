# StudyBuddy DK - Complete File Structure

## 📂 Your Project Folder (Updated)

```
studybuddy-dk/
│
├── 🔴 FRONTEND & API (NEW)
├── api.py                              # FastAPI backend (282 lines)
├── app.py                              # Streamlit frontend (450+ lines)
├── run.bat                             # Windows launcher
├── run.sh                              # Mac/Linux launcher
│
├── 📊 CORE PIPELINE (EXISTING)
├── pipeline.py                         # Orchestrates 3 agents
├── database.py                         # SQLite management
├── mlflow_tracker.py                   # MLflow logging
├── load_data.py                        # Data loading
│
├── 🤖 AGENTS (EXISTING)
├── agents/
│   ├── __init__.py
│   ├── agent1_profile_matching.py      # (180 lines)
│   ├── agent2_gap_preparation.py       # (220 lines)
│   └── agent3_monitoring.py            # (200 lines)
│
├── 📚 DATA (EXISTING)
├── data/static/
│   ├── programs.json                   # 17 programs
│   └── courses.json                    # 12 courses
│
├── 💾 DATABASE & MLflow (EXISTING)
├── studybuddy.db                       # SQLite database
├── mlflow_tracking/                    # MLflow experiment logs
│
├── 📖 DOCUMENTATION (NEW)
├── QUICK_START.md                      # 30-second setup guide
├── FRONTEND_GUIDE.md                   # Detailed usage guide
├── IMPLEMENTATION_SUMMARY.md           # This guide
├── FILE_STRUCTURE.md                   # File organization
│
├── 🐍 ENVIRONMENT (EXISTING)
├── venv311/                            # Python 3.11.9 virtual env
│   └── Scripts/
│       └── python.exe, pip, etc.
│
└── 📝 PROJECT ROOT (EXISTING)
    └── (You're here!)
```

---

## 📋 What Each File Does

### Frontend & API (NEW - Total 30 KB)

#### `api.py` (8.1 KB)
**FastAPI REST Backend**
- Purpose: Serve HTTP endpoints for analysis
- Ports: 8000 (local), 0.0.0.0 (network)
- Endpoints: 8 (/, /health, /analyse, /programs, /courses, /rates, /alerts, /runs)
- Response time: ~4 seconds
- Documentation: http://127.0.0.1:8000/docs

Key functions:
- `@app.post("/analyse")` - Main pipeline endpoint
- `@app.get("/programs")` - List all programs
- `@app.get("/health")` - Health check
- CORS enabled for Streamlit communication

#### `app.py` (18 KB)
**Streamlit Interactive Dashboard**
- Purpose: User-facing interactive interface
- Port: 8501
- Pages: 3 (Program Finder, Explorer, Status)
- Users: Can be multiple concurrent users

Key features:
- Sidebar navigation
- Form inputs with validation
- 4 tabbed result display
- Real-time API communication
- Error handling & fallbacks

#### `run.bat` (923 bytes)
**Windows Launcher Script**
- Starts FastAPI in background
- Waits 3 seconds
- Starts Streamlit in foreground
- Auto-cleanup on exit

#### `run.sh` (952 bytes)
**Mac/Linux Launcher Script**
- Same as run.bat but for Unix
- Makes it easy: `bash run.sh`

---

### Core Pipeline (EXISTING - Total 800+ lines)

#### `pipeline.py` (~100 lines)
**Pipeline Orchestrator**
- Purpose: Run all 3 agents in sequence
- Input: Student profile dict
- Output: Combined results from all agents
- Execution time: ~4 seconds
- Logging: MLflow + SQLite

Process:
1. Agent 1 → Profile + Matching
2. Agent 2 → Gaps + Costs
3. Agent 3 → Monitoring
4. Log all results
5. Return combined output

#### `database.py` (~250 lines)
**SQLite Database Management**
- Purpose: Persist data and logs
- Database: studybuddy.db (SQLite)
- Tables: 4 (programs, courses, exchange_rates, pipeline_runs)
- Queries: Fetch programs, save rates, log runs

Tables:
- `programs` - 17 Danish programs (CBS, DTU, KU, AAU, AU, SDU)
- `courses` - 12 gap-filling courses (Coursera, Udemy, edX)
- `exchange_rates` - DKK to INR, NPR, USD, EUR, GBP
- `pipeline_runs` - Logs of every analysis

#### `mlflow_tracker.py` (~120 lines)
**MLflow Experiment Tracking**
- Purpose: Log artifacts and metrics
- Backend: SQLite (sqlite:///mlflow.db)
- Artifacts: 5 JSON files per run
- Metrics: Match scores, gaps, costs, runtime
- UI: http://127.0.0.1:5000

#### `load_data.py` (~150 lines)
**Data Loading & Display**
- Purpose: Load JSON → SQLite on startup
- Loads: programs.json, courses.json
- Fetches: Live exchange rates
- Displays: Summary of loaded data
- Use: `python load_data.py`

---

### Agents (EXISTING - Total 600+ lines)

#### `agents/agent1_profile_matching.py` (~180 lines)
**Agent 1: Profile + Matching + Eligibility**
- Input: Student profile
- Output: Profile + top 3 matches + eligibility
- Algorithm: Cosine similarity scoring
- Matching: Across 5 ECTS dimensions
- Eligibility: Check IELTS + ECTS requirements

#### `agents/agent2_gap_preparation.py` (~220 lines)
**Agent 2: Gap Analysis + Preparation + Costs + Deadline**
- Input: Student profile + top programs
- Output: Gaps + courses + costs + deadlines
- Gap detection: ECTS per subject area
- Courses: Filter by skill from courses.json
- Costs: Calculate in DKK/NPR/INR/USD
- Deadlines: Calculate days remaining

#### `agents/agent3_monitoring.py` (~200 lines)
**Agent 3: Monitoring + Drift Detection**
- Input: Previous rates + requirements
- Output: Alerts + updated rates
- Drift: >5% change triggers alert
- CBS monitoring: Scrape and compare
- Logging: Save all alerts to database

---

### Data (EXISTING - ~350 lines JSON)

#### `data/static/programs.json` (~200 lines)
**17 Danish Master's Programs**

Format:
```json
{
  "program_id": "cbs_finance",
  "name": "MSc Finance",
  "university": "Copenhagen Business School",
  "ects_required": 180,
  "ielts_min": 6.5,
  "tuition_eu_dkk": 0,
  "tuition_non_eu_dkk": 85000,
  "deadline": "2027-01-15",
  "url": "https://..."
}
```

Universities:
- CBS (4 programs)
- DTU (2 programs)
- KU (2 programs)
- AAU (3 programs)
- AU (3 programs)
- SDU (3 programs)

#### `data/static/courses.json` (~150 lines)
**12 Gap-Filling Courses**

Format:
```json
{
  "course_id": "python_coursera_1",
  "skill": "Python",
  "course_name": "Python for Everybody",
  "platform": "Coursera",
  "cost_dkk": 0,
  "url": "https://..."
}
```

Skills:
- Python, SQL, Machine Learning
- Statistics, Linear Algebra
- Docker, IELTS

---

### Database & MLflow (AUTO-GENERATED)

#### `studybuddy.db`
**SQLite Database**
- Auto-created by database.py
- Size: ~100 KB
- Tables: 4
- Records: ~17 programs + 12 courses + exchange rates + logs

#### `mlflow_tracking/`
**MLflow Experiment Directory**
- Auto-created by mlflow_tracker.py
- Contains: runs/, models/, metrics/
- Size: Grows with each run
- View: http://127.0.0.1:5000

---

### Documentation (NEW - Total 23 KB)

#### `QUICK_START.md` (7.0 KB)
**Quick Setup Guide**
- 30-second installation
- 3 ways to test (Streamlit, Swagger, curl)
- Troubleshooting tips
- Performance metrics
- Architecture diagram

#### `FRONTEND_GUIDE.md` (8.9 KB)
**Detailed Frontend Documentation**
- How to run both services
- All endpoints documented
- Request/response examples
- Feature descriptions
- Advanced usage

#### `IMPLEMENTATION_SUMMARY.md` (5.5 KB)
**Architecture & Components**
- What was built
- How it works together
- Performance characteristics
- Testing instructions
- Next steps

#### `FILE_STRUCTURE.md` (This file)
**File Organization**
- Complete folder structure
- What each file does
- File sizes
- Key functions
- How to find things

---

## 🎯 Quick Navigation

### "I want to run the system"
→ Follow `QUICK_START.md`
1. Activate venv311
2. Run `run.bat` (Windows) or `bash run.sh` (Mac/Linux)
3. Open http://localhost:8501

### "I want API documentation"
→ Visit while FastAPI is running
- http://127.0.0.1:8000/docs (Swagger UI)
- http://127.0.0.1:8000/redoc (ReDoc)

### "I want to understand the code"
→ Start here:
1. `pipeline.py` - See how 3 agents work together
2. `agents/` - See each agent's logic
3. `api.py` - See REST endpoint handling
4. `app.py` - See Streamlit UI

### "I want to test the system"
→ Choose your method:
1. **Easy**: Use Streamlit (http://localhost:8501)
2. **Technical**: Use Swagger (/docs)
3. **CLI**: Use curl (see QUICK_START.md)

### "Something is broken"
→ Check QUICK_START.md troubleshooting section

---

## 📊 Code Statistics

| Component | Files | Lines | Size |
|-----------|-------|-------|------|
| Frontend & API | 4 | 750+ | 30 KB |
| Core Pipeline | 4 | 650+ | 25 KB |
| Agents | 3 | 600+ | 20 KB |
| Data | 2 | 350 | 15 KB |
| Documentation | 4 | 1,500+ | 30 KB |
| **TOTAL** | **17** | **3,850+** | **120 KB** |

---

## 🔌 Port Assignment

| Service | Port | Protocol | URL |
|---------|------|----------|-----|
| Streamlit Frontend | 8501 | HTTP | http://localhost:8501 |
| FastAPI Backend | 8000 | HTTP | http://127.0.0.1:8000 |
| MLflow UI | 5000 | HTTP | http://127.0.0.1:5000 |
| Database | (file) | SQLite | studybuddy.db |

---

## 🔑 Key Environment Variables

```bash
# Streamlit API URL (in app.py)
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# Python version
python --version  # Should be 3.11.9

# Virtual environment
venv311/  # Python 3.11.9

# Database path
studybuddy.db  # SQLite database

# MLflow tracking
sqlite:///mlflow.db  # MLflow backend
```

---

## 📦 Dependencies Summary

Already installed in venv311:
- fastapi==0.135.3
- uvicorn==0.28.0
- streamlit==1.56.0
- requests==2.31.0
- pandas==2.0.0
- openai==latest
- beautifulsoup4==4.12.0
- mlflow==3.11.1
- langchain==latest
- sqlite3 (built-in)

Install command:
```bash
pip install fastapi uvicorn streamlit requests pandas openai beautifulsoup4 mlflow
```

---

## ✅ Verification Checklist

Before proceeding to Docker (April 15):

- [ ] `api.py` copied to studybuddy-dk folder
- [ ] `app.py` copied to studybuddy-dk folder
- [ ] `run.bat` in main folder (Windows users)
- [ ] `run.sh` in main folder (Mac/Linux users)
- [ ] `QUICK_START.md` available
- [ ] `FRONTEND_GUIDE.md` available
- [ ] Database (`studybuddy.db`) exists
- [ ] All 3 agents work individually
- [ ] Pipeline runs in ~4 seconds
- [ ] FastAPI starts on port 8000
- [ ] Streamlit starts on port 8501
- [ ] Both can communicate (no API errors)

---

## 🎓 What's Complete

✅ **Backend**: FastAPI with 8 endpoints  
✅ **Frontend**: Streamlit with 3 pages  
✅ **Integration**: Seamless API communication  
✅ **Documentation**: Complete guides  
✅ **Testing**: 3 ways to test  
✅ **Error Handling**: Comprehensive  

## 🚀 What's Next

❌ Docker containerization (April 15)
❌ GitHub Actions workflow (April 15)
❌ Final technical report (April 16)
❌ GitHub repository (April 17)

---

## 💡 Pro Tips

1. **Keep database.py handy** - Use it to reinitialize if something breaks
2. **Check MLflow UI** - http://127.0.0.1:5000 to see all runs
3. **Use Swagger docs** - Test individual endpoints easily
4. **Monitor system logs** - Terminal shows all activity
5. **Save your work** - Regular backups of studybuddy-dk folder

---

## 🆘 Emergency Commands

```bash
# Reset database
python database.py

# Reload data
python load_data.py

# Test pipeline only
python pipeline.py

# Test API only
python api.py

# Test Streamlit only
streamlit run app.py

# Start both (recommended)
run.bat  # Windows
bash run.sh  # Mac/Linux
```

---

That's it! You now have a complete, documented MLOps system. 🎓

See you on April 15 for Docker! 🐳

