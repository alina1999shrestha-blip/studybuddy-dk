# FastAPI Backend & Streamlit Frontend Guide

## 📋 Overview

StudyBuddy DK has two main components:

1. **FastAPI Backend** (`api.py`) - REST API on port 8000
2. **Streamlit Frontend** (`app.py`) - Interactive dashboard on port 8501

## 🚀 Quick Start

### Option 1: Automatic (Recommended)

**On Windows:**
```bash
run.bat
```

**On Mac/Linux:**
```bash
bash run.sh
```

This will start both FastAPI and Streamlit automatically.

---

### Option 2: Manual (Two Terminal Windows)

**Terminal 1 - FastAPI Backend:**
```bash
# Make sure you're in the venv311 environment
python api.py
```

You should see:
```
============================================================
  🚀 StudyBuddy DK API — FastAPI Backend
============================================================
✅ Server running at http://127.0.0.1:8000
📚 Documentation at http://127.0.0.1:8000/docs
🔌 Ready to process student profiles
============================================================
```

**Terminal 2 - Streamlit Frontend:**
```bash
# Make sure you're in the venv311 environment
streamlit run app.py
```

You should see:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## 🔗 Access the System

Once both are running, open your browser to:

**Frontend Dashboard:** http://localhost:8501

You should see:
- 🎓 StudyBuddy DK title
- Three tabs on the left: 
  - 🔍 Program Finder
  - 📊 Program Explorer
  - ⚙️ System Status

---

## 📡 API Documentation

While FastAPI is running, visit:

**Swagger UI:** http://127.0.0.1:8000/docs
**ReDoc:** http://127.0.0.1:8000/redoc

### Main Endpoints

#### 1. Analyze Student Profile
```bash
POST http://127.0.0.1:8000/analyse
Content-Type: application/json

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

**Response:**
```json
{
  "student_name": "Alina Shrestha",
  "student_country": "Nepal",
  "top_programs": [...],
  "gaps": [...],
  "costs": [...],
  "deadlines": [...],
  "monitoring_alerts": [...],
  "runtime_seconds": 3.42,
  "timestamp": "2026-04-14T10:30:00"
}
```

#### 2. Get All Programs
```bash
GET http://127.0.0.1:8000/programs
```

Returns list of 17 programs with all details.

#### 3. Get All Courses
```bash
GET http://127.0.0.1:8000/courses
```

Returns list of 12 gap-filling courses.

#### 4. Get Exchange Rates
```bash
GET http://127.0.0.1:8000/exchange-rates
```

Returns latest exchange rates.

#### 5. Health Check
```bash
GET http://127.0.0.1:8000/health
```

Returns system status.

---

## 🎨 Frontend Features

### Tab 1: Program Finder
Enter your academic profile:
- Full name
- Bachelor's degree
- ECTS breakdown (business, quantitative, programming, research)
- IELTS score
- Country of origin
- EU citizen status

Click **Find My Programs** to get:

1. **Top Matches** - Your best 3 matching programs with scores
2. **Gap Analysis** - Skills you're missing with course recommendations
3. **Costs & Deadlines** - Tuition in your home currency + countdown
4. **Monitoring** - System status & alerts

### Tab 2: Program Explorer
Browse all 17 programs:
- Filter by university
- See all program details
- Download as CSV

### Tab 3: System Status
Monitor the system:
- API status
- Database statistics
- Recent pipeline runs
- Active monitoring alerts

---

## 🛠️ Troubleshooting

### FastAPI won't start
**Problem:** Port 8000 already in use
**Solution:**
```bash
# Find process using port 8000
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows
```

### Streamlit won't start
**Problem:** Port 8501 already in use
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### API connection refused
**Problem:** Streamlit can't reach FastAPI
**Solution:**
1. Make sure FastAPI is running first
2. Check firewall settings
3. Verify API_URL in app.py is correct:
   ```python
   API_URL = "http://127.0.0.1:8000"
   ```

### Database errors
**Problem:** SQLite database locked or missing
**Solution:**
```bash
# Reinitialize database
python database.py

# Then run pipeline to populate
python pipeline.py

# Then start API and Streamlit
```

---

## 📊 Example Workflow

1. **Open browser** → http://localhost:8501

2. **Fill in profile:**
   - Name: "John Smith"
   - Degree: "BSc Computer Science"
   - ECTS: Business 20, Quantitative 50, Programming 60, Research 30
   - IELTS: 7.0
   - Country: Germany
   - EU Citizen: Yes

3. **Click "Find My Programs"**

4. **See results:**
   - MSc Data Science @ DTU (94.5% match) ✅ Eligible
   - MSc AI @ Aalborg (92.1% match) ⚠️ 1 gap
   - MSc Computer Science @ KU (90.8% match) ⚠️ 2 gaps

5. **Explore gaps:**
   - See what courses to take
   - Check costs (FREE for EU students!)
   - Know exact deadline

6. **Monitor system:**
   - Check if requirements changed
   - See exchange rate stability
   - Review system performance

---

## 🔧 Advanced Usage

### Custom API Port
```bash
python -m uvicorn api:app --host 0.0.0.0 --port 8080
```

### Streamlit with config
Create `streamlit_config.py`:
```python
import streamlit as st

st.set_page_config(
    page_title="StudyBuddy DK",
    layout="wide"
)
```

Then run:
```bash
streamlit run app.py --config.toml config.toml
```

### Testing with curl
```bash
# Test API
curl -X POST http://127.0.0.1:8000/analyse \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "degree": "BBA",
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

## 📝 API Request/Response Examples

### Example 1: Student from Nepal
**Request:**
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

**Response (shortened):**
```json
{
  "student_name": "Alina Shrestha",
  "student_country": "Nepal",
  "top_programs": [
    {
      "program_name": "MSc Finance",
      "university": "CBS",
      "match_score": 92.5,
      "eligible": true,
      "gaps_count": 2
    }
  ],
  "costs": [
    {
      "tuition_dkk": 85000,
      "tuition_npr": 1984243,
      "tuition_inr": 1240414,
      "exchange_rate_date": "2026-04-14"
    }
  ],
  "runtime_seconds": 3.42
}
```

### Example 2: Student from Germany (EU)
**Request:**
```json
{
  "name": "Hans Mueller",
  "degree": "BSc Computer Science",
  "ects_business": 20,
  "ects_quantitative": 50,
  "ects_programming": 60,
  "ects_research": 30,
  "ielts": 7.0,
  "country": "Germany",
  "eu_student": true
}
```

**Response (shortened):**
```json
{
  "student_name": "Hans Mueller",
  "student_country": "Germany",
  "top_programs": [
    {
      "program_name": "MSc Data Science",
      "university": "DTU",
      "match_score": 95.0,
      "eligible": true,
      "gaps_count": 0
    }
  ],
  "costs": [
    {
      "tuition_dkk": 0,
      "tuition_npr": 0,
      "tuition_inr": 0,
      "exchange_rate_date": "2026-04-14"
    }
  ],
  "runtime_seconds": 3.18
}
```

---

## 📦 What's Included

```
studybuddy-dk/
├── api.py                          # FastAPI backend
├── app.py                          # Streamlit frontend
├── pipeline.py                     # Pipeline orchestration
├── database.py                     # SQLite management
├── mlflow_tracker.py               # MLflow logging
├── agents/
│   ├── agent1_profile_matching.py  # Agent 1
│   ├── agent2_gap_preparation.py   # Agent 2
│   └── agent3_monitoring.py        # Agent 3
├── data/static/
│   ├── programs.json               # 17 programs
│   └── courses.json                # 12 courses
├── studybuddy.db                   # SQLite database
├── run.sh                          # Mac/Linux launcher
├── run.bat                         # Windows launcher
└── README.md                       # This file
```

---

## ✅ Checklist Before Running

- [ ] Python 3.11.9 installed
- [ ] Virtual environment activated (venv311)
- [ ] All dependencies installed: `pip list | grep streamlit`
- [ ] Database initialized: `python database.py`
- [ ] Pipeline tested: `python pipeline.py`
- [ ] Port 8000 available: `lsof -i :8000` (Mac/Linux)
- [ ] Port 8501 available: `lsof -i :8501` (Mac/Linux)

---

## 🎯 Next Steps

1. Start the system (FastAPI + Streamlit)
2. Open http://localhost:8501
3. Enter your profile
4. Get personalized recommendations
5. Explore all 17 programs
6. Check system status
7. View API docs at http://127.0.0.1:8000/docs

Enjoy! 🚀

---

**Questions?** Check the MLflow dashboard at http://127.0.0.1:5000 for run history and artifacts.
