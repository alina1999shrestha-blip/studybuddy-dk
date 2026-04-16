"""
StudyBuddy DK — Final Streamlit Dashboard
"""

import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime
import dotenv; dotenv.load_dotenv(encoding='utf-8-sig')

# ── Try to import pipeline directly (works on Streamlit Cloud) ──
PIPELINE_ERROR = None
try:
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from pipeline import run_pipeline
    from database import init_database, load_programs_to_db, load_courses_to_db, get_connection
    if not os.path.exists("studybuddy.db"):
        init_database()
        load_programs_to_db()
        load_courses_to_db()
    PIPELINE_DIRECT = True
except Exception as e:
    PIPELINE_DIRECT = False
    PIPELINE_ERROR = str(e)

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="StudyBuddy DK",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def api_ok():
    if PIPELINE_DIRECT:
        return True
    try:
        return requests.get(f"{API_URL}/health", timeout=4).status_code == 200
    except:
        return False

# ===== CUSTOM CSS =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }
.hero {
    background: linear-gradient(135deg, #0f2352 0%, #1a3a7a 50%, #0f2352 100%);
    border-radius: 20px; padding: 3rem 2rem 2.5rem;
    text-align: center; margin-bottom: 2rem;
    position: relative; overflow: hidden;
}
.hero::before { content:''; position:absolute; top:-60px; right:-60px; width:200px; height:200px; background:rgba(255,255,255,0.04); border-radius:50%; }
.hero::after  { content:''; position:absolute; bottom:-40px; left:-40px; width:150px; height:150px; background:rgba(255,255,255,0.03); border-radius:50%; }
.hero h1 { font-family:'DM Serif Display',serif !important; font-size:3rem; color:white; margin:0 0 0.5rem 0; letter-spacing:-1px; }
.hero p  { color:rgba(255,255,255,0.75); font-size:1.1rem; margin:0; }
.hero .flag-row { font-size:1.6rem; margin-bottom:1rem; letter-spacing:6px; }
.program-card {
    background:white; border:2px solid #e8edf5; border-top:4px solid #0f2352;
    border-radius:16px; padding:1.5rem; margin-bottom:1rem;
    position:relative; transition:all 0.2s; box-shadow:0 2px 8px rgba(15,35,82,0.06);
}
.program-card:hover { box-shadow:0 8px 24px rgba(15,35,82,0.15); transform:translateY(-2px); }
.rank-badge {
    position:absolute; top:1.2rem; right:1.2rem;
    background:linear-gradient(135deg,#0f2352,#2563eb); color:white;
    border-radius:50%; width:38px; height:38px;
    display:flex; align-items:center; justify-content:center;
    font-weight:700; font-size:0.9rem; box-shadow:0 4px 12px rgba(15,35,82,0.3);
}
.program-name  { font-size:1.15rem; font-weight:700; color:#0f2352; margin:0 0 0.25rem 0; }
.university-name { color:#6b7a99; font-size:0.9rem; margin:0 0 1rem 0; }
.score-row { display:flex; align-items:center; gap:12px; margin-bottom:0.75rem; }
.score-label { font-size:0.85rem; color:#6b7a99; width:80px; flex-shrink:0; }
.score-bar-bg { flex:1; background:#eef2ff; border-radius:99px; height:12px; overflow:hidden; }
.score-bar-fill { height:100%; border-radius:99px; transition:width 0.8s ease; }
.score-value { font-weight:700; font-size:0.9rem; width:45px; text-align:right; flex-shrink:0; }
.pill-eligible { display:inline-block; background:linear-gradient(135deg,#dcfce7,#bbf7d0); color:#166534; border:1px solid #86efac; border-radius:99px; padding:0.3rem 1rem; font-size:0.8rem; font-weight:700; }
.pill-gaps     { display:inline-block; background:linear-gradient(135deg,#fff7ed,#fed7aa); color:#9a3412; border:1px solid #fdba74; border-radius:99px; padding:0.3rem 1rem; font-size:0.8rem; font-weight:700; }
.readiness-circle {
    background:linear-gradient(135deg,#0f2352,#2563eb); border-radius:50%;
    width:130px; height:130px; display:flex; flex-direction:column;
    align-items:center; justify-content:center; color:white; margin:0 auto 1rem;
    box-shadow:0 8px 32px rgba(15,35,82,0.35);
}
.readiness-circle .pct   { font-size:2.2rem; font-weight:700; line-height:1; }
.readiness-circle .label { font-size:0.6rem; opacity:0.8; letter-spacing:2px; text-transform:uppercase; margin-top:2px; }
.gap-card {
    background:linear-gradient(135deg,#fffbeb,#fef3c7);
    border-left:5px solid #f59e0b; border-radius:0 14px 14px 0;
    padding:1.2rem 1.5rem; margin-bottom:1rem;
    box-shadow:0 2px 8px rgba(245,158,11,0.12);
}
.gap-card .gap-title { font-weight:700; color:#78350f; font-size:1.05rem; margin-bottom:0.3rem; }
.gap-card .gap-sub   { color:#92400e; font-size:0.88rem; }
.course-chip {
    display:inline-block; background:linear-gradient(135deg,#fffbeb,#fef9c3);
    border:1px solid #fde68a; border-radius:10px; padding:0.5rem 1rem;
    font-size:0.82rem; margin:0.3rem 0.3rem 0 0; color:#78350f;
    box-shadow:0 1px 4px rgba(245,158,11,0.1);
}
.course-chip .free-tag { color:#059669; font-weight:700; }
.cost-card { border-radius:18px; padding:1.8rem 1.5rem; text-align:center; color:white; box-shadow:0 6px 20px rgba(0,0,0,0.15); }
.cost-card-dkk { background:linear-gradient(135deg,#065f46,#059669); }
.cost-card-npr { background:linear-gradient(135deg,#1e3a5f,#2563eb); }
.cost-card-inr { background:linear-gradient(135deg,#4c1d95,#7c3aed); }
.cost-card-usd { background:linear-gradient(135deg,#78350f,#d97706); }
.cost-card-eur { background:linear-gradient(135deg,#065f46,#059669); }
.cost-card-gbp { background:linear-gradient(135deg,#1e3a5f,#2563eb); }
.cost-card .currency { font-size:0.75rem; opacity:0.85; text-transform:uppercase; letter-spacing:2px; margin-bottom:0.4rem; }
.cost-card .amount   { font-size:2rem; font-weight:700; font-family:'DM Serif Display',serif; }
.cost-card .per-year { font-size:0.75rem; opacity:0.65; margin-top:0.3rem; }
.deadline-urgent { background:linear-gradient(135deg,#fff1f2,#ffe4e6); border:2px solid #fca5a5; border-left:5px solid #ef4444; border-radius:14px; padding:1.2rem 1.5rem; margin-bottom:0.8rem; box-shadow:0 2px 8px rgba(239,68,68,0.1); }
.deadline-ok     { background:linear-gradient(135deg,#faf5ff,#ede9fe); border:2px solid #c4b5fd; border-left:5px solid #7c3aed; border-radius:14px; padding:1.2rem 1.5rem; margin-bottom:0.8rem; box-shadow:0 2px 8px rgba(124,58,237,0.08); }
.deadline-name { font-weight:700; font-size:0.95rem; margin-bottom:0.4rem; color:#4c1d95; }
.deadline-days { font-size:2rem; font-weight:700; color:#7c3aed; font-family:'DM Serif Display',serif; }
.alert-high   { background:linear-gradient(135deg,#fff1f2,#fee2e2); border-left:5px solid #ef4444; border-radius:0 12px 12px 0; padding:1rem 1.2rem; margin-bottom:0.6rem; color:#991b1b; font-size:0.9rem; box-shadow:0 2px 8px rgba(239,68,68,0.1); }
.alert-medium { background:linear-gradient(135deg,#fffbeb,#fef3c7); border-left:5px solid #f59e0b; border-radius:0 12px 12px 0; padding:1rem 1.2rem; margin-bottom:0.6rem; color:#92400e; font-size:0.9rem; box-shadow:0 2px 8px rgba(245,158,11,0.1); }
.alert-ok     { background:linear-gradient(135deg,#f0fdfa,#ccfbf1); border-left:5px solid #14b8a6; border-radius:0 12px 12px 0; padding:1rem 1.2rem; margin-bottom:0.6rem; color:#134e4a; font-size:0.9rem; box-shadow:0 2px 8px rgba(20,184,166,0.1); }
.monitor-stat { background:linear-gradient(135deg,#f0fdfa,#ccfbf1); border:2px solid #99f6e4; border-radius:16px; padding:1.5rem; text-align:center; box-shadow:0 4px 12px rgba(20,184,166,0.1); }
.monitor-stat .stat-val { font-size:2rem; font-weight:700; color:#0f766e; font-family:'DM Serif Display',serif; }
.monitor-stat .stat-lbl { font-size:0.8rem; color:#5eead4; margin-top:0.2rem; text-transform:uppercase; letter-spacing:1px; }
.stat-box { background:white; border:1px solid #e8edf5; border-radius:12px; padding:1.2rem; text-align:center; box-shadow:0 2px 8px rgba(15,35,82,0.05); }
.stat-box .stat-value { font-size:2rem; font-weight:700; color:#0f2352; font-family:'DM Serif Display',serif; }
.stat-box .stat-label { font-size:0.8rem; color:#6b7a99; margin-top:0.2rem; }
.timeline-wrap { position:relative; padding-left:2rem; }
.timeline-wrap::before { content:''; position:absolute; left:12px; top:0; bottom:0; width:3px; background:linear-gradient(180deg,#0f2352,#7c3aed,#059669,#d97706); border-radius:99px; }
.tl-item { position:relative; margin-bottom:1.5rem; padding:1.5rem 1.5rem 1.5rem 2rem; border-radius:16px; color:white; box-shadow:0 6px 20px rgba(0,0,0,0.12); }
.tl-item::before { content:''; position:absolute; left:-2.5rem; top:1.5rem; width:16px; height:16px; border-radius:50%; border:3px solid white; box-shadow:0 0 0 3px currentColor; }
.tl-foundation { background:linear-gradient(135deg,#0f2352,#1d4ed8); } .tl-foundation::before { color:#1d4ed8; }
.tl-skills     { background:linear-gradient(135deg,#4c1d95,#7c3aed); } .tl-skills::before     { color:#7c3aed; }
.tl-advanced   { background:linear-gradient(135deg,#065f46,#059669); } .tl-advanced::before   { color:#059669; }
.tl-apply      { background:linear-gradient(135deg,#78350f,#d97706); } .tl-apply::before      { color:#d97706; }
.tl-period { font-size:0.75rem; opacity:0.8; text-transform:uppercase; letter-spacing:2px; margin-bottom:0.3rem; }
.tl-title  { font-size:1.2rem; font-weight:700; margin-bottom:1rem; font-family:'DM Serif Display',serif; }
.tl-task { background:rgba(255,255,255,0.15); border-radius:8px; padding:0.5rem 0.8rem; margin-bottom:0.4rem; font-size:0.88rem; display:flex; align-items:center; gap:0.5rem; }
.tl-task::before { content:'✓'; font-weight:700; opacity:0.9; }
[data-testid="stSidebar"] { background:#f7f9fd !important; }
</style>
""", unsafe_allow_html=True)


# ===== HELPERS =====
def score_color(score):
    if score >= 85: return "#22c55e"
    if score >= 70: return "#f59e0b"
    return "#ef4444"

def readiness_score(result):
    top   = result.get("top_programs", [])
    gaps  = result.get("gaps", [])
    match = top[0]["match_score"] if top else 0
    return int(max(0, min(100, match - len(gaps) * 8)))


# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### 🎓 StudyBuddy DK")
    st.markdown("---")
    page = st.radio("Navigate",
        ["🔍 Program Finder", "📊 Program Explorer", "📖 Preparation Guide", "⚙️ System Status"],
        label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**17 programs** from 6 universities")
    st.markdown("**Live** exchange rates daily")
    st.markdown("**AI-powered** gap analysis")
    st.markdown("---")
    st.caption("MLOps Assignment · Alina Shrestha · April 2026")


# ===== HERO =====
st.markdown("""
<div class="hero">
    <div class="flag-row">🇩🇰</div>
    <h1>StudyBuddy DK</h1>
    <p>AI-powered Danish master's program finder for international students</p>
</div>""", unsafe_allow_html=True)


# ===== CONSTANTS =====
CREDIT_SYSTEMS = {
    "ECTS (European — already correct)": 1.0,
    "Nepal / India — Credit Hours (×2)": 2.0,
    "US Credit Hours (×1.5)": 1.5,
    "UK Credits (÷2)": 0.5,
    "Australian Credit Points (÷1.5)": 0.667,
    "Pakistani Credit Hours (×2)": 2.0,
    "Bangladesh Credit Hours (×2)": 2.0,
    "Sri Lanka Credit Hours (×2)": 2.0,
}
SUBJECT_HINTS = {
    "Business / Management": "Courses like Accounting, Finance, Marketing, Strategy, HRM, Operations",
    "Quantitative / Math":   "Courses like Statistics, Mathematics, Econometrics, Operations Research",
    "Programming / CS":      "Courses like Python, Java, Databases, Data Structures, IT, Computer Science",
    "Research / Thesis":     "Final year project, dissertation, research methods, thesis credits",
}


# ===== PAGE 1: PROGRAM FINDER =====
if page == "🔍 Program Finder":

    if not api_ok():
        if PIPELINE_ERROR:
            st.error(f"⚠️ Pipeline import failed: {PIPELINE_ERROR}")
        else:
            st.error("⚠️ API offline — run `python api.py` first, then refresh.")
        st.stop()

    st.markdown("#### Step 1 — Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        name    = st.text_input("Full Name", placeholder="e.g. Alina Shrestha")
        degree  = st.text_input("Bachelor's Degree", placeholder="e.g. BBA Finance")
        country = st.selectbox("Country", ["Nepal","India","Bangladesh","Pakistan","Sri Lanka","Germany","France","Other"])
        eu_flag = st.checkbox("EU Citizen (tuition-free)?", value=False)
    with col2:
        ielts = st.slider("IELTS Score", 0.0, 9.0, 6.5, 0.5)
        st.markdown(f"**IELTS {ielts}** — {'✅ Meets most requirements (6.5+)' if ielts >= 6.5 else '⚠️ Below minimum for most programs (need 6.5)'}")
        st.markdown("---")
        credit_system = st.selectbox("🌍 Your university's credit system", list(CREDIT_SYSTEMS.keys()))
        factor = CREDIT_SYSTEMS[credit_system]
        if factor != 1.0:
            st.info(f"ℹ️ Conversion: your credits × {factor:.2f} = ECTS")

    st.markdown("---")
    st.markdown("#### Step 2 — ECTS Calculator")

    with st.expander("🤖 Auto-fill from transcript photo (AI-powered)", expanded=False):
        st.markdown("Upload a photo of your transcript and AI will read it and fill in your credits automatically.")
        st.caption("Supports Nepali, Indian, Pakistani, Bangladeshi and most Asian university transcripts.")
        uploaded = st.file_uploader("Upload transcript image", type=["jpg","jpeg","png"], key="transcript_upload")
        if uploaded is not None:
            import base64, json as _json
            col_img, col_btn = st.columns([2,1])
            with col_img:
                st.image(uploaded, caption="Your transcript", use_container_width=True)
            with col_btn:
                st.markdown("<br>", unsafe_allow_html=True)
                extract_btn = st.button("🔍 Extract Credits with AI", type="primary", use_container_width=True)
            if extract_btn:
                with st.spinner("🤖 AI is reading your transcript…"):
                    try:
                        img_bytes = uploaded.read()
                        img_b64   = base64.b64encode(img_bytes).decode("utf-8")
                        ext  = uploaded.name.split(".")[-1].lower()
                        mime = "image/jpeg" if ext in ["jpg","jpeg"] else "image/png"
                        prompt = """You are an academic credit analyser. Look at this university transcript carefully.
Extract ALL courses and categorise them into exactly these 4 areas:
1. business_credits
2. quant_credits
3. programming_credits
4. research_credits
Respond ONLY with valid JSON:
{"degree_name":"...","university_name":"...","credit_system":"...","total_credits":0,"cgpa":"...","business_credits":0,"quant_credits":0,"programming_credits":0,"research_credits":0,"courses_found":0,"confidence":"high/medium/low","notes":"..."}"""
                        response = __import__("requests").post(
                            "https://api.anthropic.com/v1/messages",
                            headers={"Content-Type": "application/json"},
                            json={"model":"claude-sonnet-4-6","max_tokens":1000,"messages":[{"role":"user","content":[{"type":"image","source":{"type":"base64","media_type":mime,"data":img_b64}},{"type":"text","text":prompt}]}]},
                            timeout=30
                        )
                        if response.status_code == 200:
                            raw_text  = response.json()["content"][0]["text"].strip().replace("```json","").replace("```","").strip()
                            extracted = _json.loads(raw_text)
                            st.success("✅ Transcript read successfully!")
                            st.session_state["ai_business"]    = float(extracted.get("business_credits", 0))
                            st.session_state["ai_quant"]       = float(extracted.get("quant_credits", 0))
                            st.session_state["ai_programming"] = float(extracted.get("programming_credits", 0))
                            st.session_state["ai_research"]    = float(extracted.get("research_credits", 0))
                            e1,e2,e3,e4,e5 = st.columns(5)
                            for col,label,val in [(e1,"Total",extracted.get("total_credits",0)),(e2,"Business",extracted.get("business_credits",0)),(e3,"Quant",extracted.get("quant_credits",0)),(e4,"Programming",extracted.get("programming_credits",0)),(e5,"Research",extracted.get("research_credits",0))]:
                                with col:
                                    st.markdown(f'<div class="stat-box"><div class="stat-value">{val}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)
                            conf = extracted.get("confidence","")
                            conf_color = "alert-ok" if conf=="high" else ("alert-medium" if conf=="medium" else "alert-high")
                            st.markdown(f'<div class="{conf_color}">Confidence: <b>{conf}</b> · CGPA: <b>{extracted.get("cgpa","")}</b> · {extracted.get("notes","")}</div>', unsafe_allow_html=True)
                            st.info("✅ Credits filled below — review and adjust if needed, then click Analyse.")
                        else:
                            st.error(f"API error {response.status_code} — fill in credits manually below.")
                    except _json.JSONDecodeError:
                        st.error("Could not parse AI response — please fill in credits manually below.")
                    except Exception as e:
                        st.error(f"Error: {e} — please fill in credits manually below.")

    st.markdown("Enter your credits **per subject area** from your transcript. We convert them to ECTS automatically.")
    default_b = st.session_state.get("ai_business", 0.0)
    default_q = st.session_state.get("ai_quant", 0.0)
    default_p = st.session_state.get("ai_programming", 0.0)
    default_r = st.session_state.get("ai_research", 0.0)

    rows = []
    for subject, hint, default_val in zip(list(SUBJECT_HINTS.keys()), list(SUBJECT_HINTS.values()), [default_b,default_q,default_p,default_r]):
        c1,c2,c3,c4 = st.columns([3,2,2,3])
        with c1:
            st.markdown(f"**{subject}**"); st.caption(hint)
        with c2:
            raw = st.number_input(f"Credits ({subject[:4]})", min_value=0.0, max_value=500.0, value=float(default_val), step=1.0, key=f"raw_{subject}", label_visibility="collapsed")
        with c3:
            ects_val = round(raw * factor, 1); st.metric("ECTS", ects_val, label_visibility="visible")
        with c4:
            st.caption(f"= {raw} × {factor:.2f}")
        rows.append(ects_val)

    ects_b,ects_q,ects_p,ects_r = rows[0],rows[1],rows[2],rows[3]
    total = ects_b+ects_q+ects_p+ects_r
    ct1,ct2,ct3,ct4,ct5 = st.columns(5)
    for col,val,lbl in [(ct1,f"{total:.0f}","Total ECTS"),(ct2,f"{ects_b:.0f}","Business"),(ct3,f"{ects_q:.0f}","Quant"),(ct4,f"{ects_p:.0f}","Programming"),(ct5,f"{ects_r:.0f}","Research")]:
        with col:
            st.markdown(f'<div class="stat-box"><div class="stat-value">{val}</div><div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📖 What counts as ECTS in each area? (click to see examples)"):
        st.markdown("""
| Subject Area | Examples |
|---|---|
| **Business / Management** | Accounting, Finance, Marketing, Strategy, HRM |
| **Quantitative / Math**   | Statistics, Mathematics, Econometrics, Calculus |
| **Programming / CS**      | Python, Java, Databases, Data Structures |
| **Research / Thesis**     | Final Year Project, Dissertation, Research Methods |

**Conversion:** Nepal/India 3-credit course → 3 × 2 = **6 ECTS** · US 3-credit → 3 × 1.5 = **4.5 ECTS**
        """)

    st.markdown("#### Step 3 — Analyse")
    if st.button("🚀 Analyse My Profile", use_container_width=True, type="primary"):
        if not name or not degree:
            st.error("Please fill in name and degree.")
        else:
            with st.spinner("Running pipeline…"):
                try:
                    payload = {"name":name,"degree":degree,"ects_business":float(ects_b),"ects_quantitative":float(ects_q),"ects_programming":float(ects_p),"ects_research":float(ects_r),"ielts":float(ielts),"country":country,"eu_student":eu_flag,"known_skills":[]}
                    if PIPELINE_DIRECT:
                        raw = run_pipeline(payload)
                        top3    = raw.get("top3_matches",[])
                        monitor = raw.get("monitoring",{})
                        alerts  = monitor.get("alerts",[]) if isinstance(monitor,dict) else []
                        result  = {"student_name":raw.get("student_name"),"top_programs":top3,"gaps":raw.get("gaps",[]),"recommendations":raw.get("recommendations",[]),"costs":raw.get("costs",{}),"deadlines":raw.get("deadlines",[]),"monitoring_alerts":alerts,"runtime_seconds":float(raw.get("run_duration_s",0)),"timestamp":datetime.now().isoformat()}
                    else:
                        resp = requests.post(f"{API_URL}/analyse", json=payload, timeout=30)
                        if resp.status_code != 200:
                            st.error(f"API error {resp.status_code}: {resp.text}"); st.stop()
                        result = resp.json()

                    st.success("✅ Analysis complete!")
                    top_programs    = result.get("top_programs",[])
                    gaps            = result.get("gaps",[])
                    recommendations = result.get("recommendations",[])
                    costs_raw       = result.get("costs",{})
                    costs           = costs_raw if isinstance(costs_raw,dict) else (costs_raw[0] if costs_raw else {})
                    deadlines       = result.get("deadlines",[])
                    alerts          = result.get("monitoring_alerts",[])
                    readiness       = readiness_score(result)

                    s1,s2,s3,s4 = st.columns(4)
                    top_score = top_programs[0].get("match_score",0) if top_programs else 0
                    days      = deadlines[0].get("days_left", deadlines[0].get("days_remaining",0)) if deadlines else 0
                    cost_val  = costs.get("tuition_dkk",0)
                    for col,val,lbl in [(s1,f"{top_score:.0f}%","Top Match Score"),(s2,len(gaps),"Skill Gaps Found"),(s3,f"{int(cost_val):,}","DKK / Year"),(s4,days,"Days to Deadline")]:
                        with col:
                            st.markdown(f'<div class="stat-box"><div class="stat-value">{val}</div><div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    t1,t2,t3,t4,t5 = st.tabs(["🏆 Top Matches","🎯 Gap Analysis","💰 Costs","📅 Deadlines","📈 Monitoring"])

                    with t1:
                        if not top_programs: st.info("No programs found.")
                        for i,p in enumerate(top_programs[:3],1):
                            score = p.get("match_score",0)
                            elig  = p.get("eligibility",{})
                            is_el = elig.get("eligible",False) if isinstance(elig,dict) else bool(elig)
                            color = score_color(score)
                            pill  = '<span class="pill-eligible">✅ Eligible</span>' if is_el else '<span class="pill-gaps">⚠️ Gaps found</span>'
                            st.markdown(f"""<div class="program-card"><div class="rank-badge">{i}</div>
                                <div class="program-name">{p.get('program_name','')}</div>
                                <div class="university-name">{p.get('university_full',p.get('university',''))} · {p.get('location','')}</div>
                                <div class="score-row"><div class="score-label">Match</div>
                                    <div class="score-bar-bg"><div class="score-bar-fill" style="width:{score}%;background:{color}"></div></div>
                                    <div class="score-value" style="color:{color}">{score:.0f}%</div></div>
                                {pill}
                                <div style="margin-top:0.5rem;font-size:0.8rem;color:#6b7a99;">
                                    📅 Deadline: {p.get('deadline','')} &nbsp;·&nbsp; 💰 {int(p.get('tuition_dkk',0)):,} DKK/year (non-EU)
                                </div></div>""", unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        _,rc2,_ = st.columns([1,1,1])
                        with rc2:
                            st.markdown(f'<div class="readiness-circle"><div class="pct">{readiness}%</div><div class="label">Readiness</div></div><p style="text-align:center;color:#6b7a99;font-size:0.85rem;">Overall readiness for your top match</p>', unsafe_allow_html=True)

                    with t2:
                        if not gaps:
                            st.success("🎉 No skill gaps — you meet all requirements!")
                        else:
                            st.markdown(f"**{len(gaps)} gap(s) found.** Here's what to work on:")
                            for gap in gaps:
                                skill   = gap.get("area", gap.get("skill",""))
                                have    = gap.get("have", gap.get("have_ects",0))
                                need    = gap.get("need", gap.get("need_ects",0))
                                missing = gap.get("missing", need-have)
                                icon    = "🔴" if gap.get("priority","medium")=="high" else "🟡"
                                sub     = f"Your IELTS: {have} · Required: {need} · Gap: {missing:.1f} points" if gap.get("type","")=="ielts" else f"You have {have} ECTS · Need {need} ECTS · Gap: {missing} ECTS"
                                st.markdown(f'<div class="gap-card"><div class="gap-title">{icon} {skill}</div><div class="gap-sub">{sub}</div></div>', unsafe_allow_html=True)
                                st.markdown("<br>", unsafe_allow_html=True)
                        if recommendations:
                            st.markdown("---")
                            st.markdown("**📚 Recommended courses to fill your gaps:**")
                            for rec in recommendations:
                                gap_name = rec.get("gap","")
                                courses  = rec.get("courses",[])
                                if "course_name" in rec: courses=[rec]; gap_name=rec.get("skill","")
                                if gap_name: st.markdown(f"**For {gap_name}:**")
                                chips = ""
                                for c in courses:
                                    cost_str = c.get("cost",c.get("cost_dkk","Free"))
                                    free_tag = '<span class="free-tag">FREE</span>' if "free" in str(cost_str).lower() else str(cost_str)
                                    rating   = c.get("rating","")
                                    chips   += f'<span class="course-chip">📚 <a href="{c.get("url","#")}" target="_blank" style="color:inherit;text-decoration:none">{c.get("course_name",c.get("name",""))}</a> · {c.get("platform","")} · {free_tag} {"⭐ "+str(rating) if rating else ""}</span>'
                                st.markdown(chips, unsafe_allow_html=True)
                                st.markdown("<br>", unsafe_allow_html=True)

                    with t3:
                        if not costs: st.info("No cost data available.")
                        else:
                            dkk  = costs.get("tuition_dkk",0); npr=costs.get("tuition_npr",0)
                            inr  = costs.get("tuition_inr",0); usd=costs.get("tuition_usd",0)
                            date = costs.get("rate_date",costs.get("exchange_rate_date","today"))
                            cc1,cc2,cc3,cc4 = st.columns(4)
                            for col,currency,amount,flag,cls in [(cc1,"DKK / Year",f"{int(dkk):,}","🇩🇰","cost-card cost-card-dkk"),(cc2,"NPR / Year",f"{int(npr):,}","🇳🇵","cost-card cost-card-npr"),(cc3,"INR / Year",f"{int(inr):,}","🇮🇳","cost-card cost-card-inr"),(cc4,"USD / Year",f"{int(usd):,}","🇺🇸","cost-card cost-card-usd")]:
                                with col:
                                    st.markdown(f'<div class="{cls}"><div class="currency">{flag} {currency}</div><div class="amount">{amount}</div><div class="per-year">Tuition only</div></div>', unsafe_allow_html=True)
                            st.markdown(f"<br><p style='color:#6b7a99;font-size:0.85rem;text-align:center'>Exchange rates as of <b>{date}</b> · fetched daily via GitHub Actions</p>", unsafe_allow_html=True)
                            st.markdown("#### Visual Comparison")
                            st.bar_chart(pd.DataFrame({"Currency":["DKK","NPR (÷100)","INR (÷100)","USD"],"Amount":[dkk,npr/100,inr/100,usd]}).set_index("Currency"))

                    with t4:
                        if not deadlines: st.info("No deadline data available.")
                        else:
                            for d in deadlines:
                                pname  = d.get("program",d.get("program_name",""))
                                days_r = d.get("days_left",d.get("days_remaining",0))
                                dl     = d.get("deadline","TBD")
                                univ   = d.get("university","")
                                card   = "deadline-urgent" if days_r<100 else "deadline-ok"
                                emoji  = "🔴" if days_r<100 else "✅"
                                st.markdown(f'<div class="{card}"><div class="deadline-name">{emoji} {pname} — {univ}</div><div><span class="deadline-days">{days_r}</span><span style="color:#6b7a99;font-size:0.85rem"> days remaining · {dl}</span></div></div>', unsafe_allow_html=True)

                    with t5:
                        runtime = result.get("runtime_seconds",0)
                        ts      = result.get("timestamp","")[:10]
                        m1,m2 = st.columns(2)
                        with m1: st.markdown(f'<div class="monitor-stat"><div class="stat-val">{runtime:.2f}s</div><div class="stat-lbl">Pipeline Runtime</div></div>', unsafe_allow_html=True)
                        with m2: st.markdown(f'<div class="monitor-stat"><div class="stat-val">{ts}</div><div class="stat-lbl">Run Date</div></div>', unsafe_allow_html=True)
                        st.markdown("<br>**Monitoring Alerts**", unsafe_allow_html=True)
                        if not alerts:
                            st.markdown('<div class="alert-ok">✅ All systems operational — no alerts</div>', unsafe_allow_html=True)
                        else:
                            for a in alerts:
                                sev  = str(a.get("severity","")).upper() if isinstance(a,dict) else "INFO"
                                msg  = a.get("message",str(a)) if isinstance(a,dict) else str(a)
                                cls  = "alert-high" if sev=="HIGH" else ("alert-medium" if sev=="MEDIUM" else "alert-ok")
                                icon = "🔴" if sev=="HIGH" else ("🟡" if sev=="MEDIUM" else "🟢")
                                st.markdown(f'<div class="{cls}">{icon} {msg}</div>', unsafe_allow_html=True)
# ── User Feedback ──────────────────────────────
                    st.markdown("---")
                    st.markdown("#### Was this recommendation helpful?")
                    with st.form("feedback_form"):
                        feedback_comment = st.text_input("Any comments? (optional)")
                        col1, col2 = st.columns(2)
                        with col1:
                            positive = st.form_submit_button("👍 Yes, helpful", use_container_width=True)
                        with col2:
                            negative = st.form_submit_button("👎 Not helpful", use_container_width=True)
                        if positive:
                            from database import save_feedback
                            save_feedback("positive", feedback_comment)
                            st.success("Thank you for your feedback!")
                        if negative:
                            from database import save_feedback
                            save_feedback("negative", feedback_comment)
                            st.info("Thanks — we will use this to improve.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {e}")
                except Exception as e:
                    st.error(f"Error: {e}")


# ===== PAGE 2: PROGRAM EXPLORER =====
elif page == "📊 Program Explorer":
    st.markdown("## All 17 Danish Programs")
    try:
        if PIPELINE_DIRECT:
            conn = get_connection(); cursor = conn.cursor()
            cursor.execute("SELECT * FROM programs")
            columns = [d[0] for d in cursor.description]
            programs = [dict(zip(columns,row)) for row in cursor.fetchall()]
            conn.close()
        else:
            resp = requests.get(f"{API_URL}/programs", timeout=10)
            programs = resp.json().get("programs",[]) if resp.status_code==200 else []
        if programs:
            df   = pd.DataFrame(programs)
            unis = st.multiselect("Filter by University", df["university"].unique().tolist(), default=df["university"].unique().tolist())
            filtered = df[df["university"].isin(unis)]
            display_cols = [c for c in ["name","university","ects_required","ielts_min","tuition_non_eu_dkk"] if c in filtered.columns]
            st.dataframe(filtered[display_cols], use_container_width=True)
            st.caption(f"{len(filtered)} programs shown")
        else:
            st.warning("No programs found")
    except Exception as e:
        st.error(f"Error: {e}")


# ===== PAGE 3: PREPARATION GUIDE =====
elif page == "📖 Preparation Guide":
    st.markdown("## 🗺️ Your Journey to Denmark")
    st.markdown("A personalised roadmap to get you fully ready for your Danish master's application.")
    st.markdown("""
    <div class="timeline-wrap">
      <div class="tl-item tl-foundation">
        <div class="tl-period">Month 0 – 1</div><div class="tl-title">🏗️ Foundation Building</div>
        <div class="tl-task">Take practice IELTS tests to identify your weak areas</div>
        <div class="tl-task">Enroll in foundational courses — Python, Statistics basics</div>
        <div class="tl-task">Review syllabi and entry requirements of your target programs</div>
        <div class="tl-task">Build a detailed weekly study schedule and stick to it</div>
      </div>
      <div class="tl-item tl-skills">
        <div class="tl-period">Month 1 – 3</div><div class="tl-title">⚡ Skill Development</div>
        <div class="tl-task">Focus on IELTS writing and speaking — these take longest to improve</div>
        <div class="tl-task">Complete core courses — Python, SQL, Machine Learning basics</div>
        <div class="tl-task">Practice with real datasets and build 1-2 small projects</div>
        <div class="tl-task">Retake IELTS if needed — target score 6.5 or above</div>
      </div>
      <div class="tl-item tl-advanced">
        <div class="tl-period">Month 3 – 6</div><div class="tl-title">🚀 Advanced Topics</div>
        <div class="tl-task">Deepen knowledge in your specialisation area</div>
        <div class="tl-task">Complete a capstone project or real-world case study</div>
        <div class="tl-task">Join online communities — Reddit, Discord, LinkedIn groups</div>
        <div class="tl-task">Draft your personal statement and motivation letter</div>
      </div>
      <div class="tl-item tl-apply">
        <div class="tl-period">Month 6+</div><div class="tl-title">📬 Application & Submission</div>
        <div class="tl-task">Submit completed applications before the January 15 deadline</div>
        <div class="tl-task">Prepare for potential interviews with real project examples</div>
        <div class="tl-task">Arrange official transcripts, reference letters, and documents</div>
        <div class="tl-task">Track your application status and respond promptly</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💡 Pro Tips from Students Who Made It")
    tips = [
        ("🎯","Consistency beats intensity","Study 1 hour every day rather than 8 hours once a week. Small steps compound."),
        ("📝","Mock tests are everything","Take a full IELTS mock test every 2 weeks. Track your score. Adjust your weak areas."),
        ("💻","Build real projects","A GitHub profile with 2-3 real projects is worth more than any certificate alone."),
        ("🤝","Community matters","Join Facebook groups and Discord servers for international students applying to Denmark."),
        ("⏸️","Rest is part of the plan","Burnout kills momentum. Schedule rest days and protect your mental energy."),
    ]
    c1,c2 = st.columns(2)
    for i,(icon,title,desc) in enumerate(tips):
        col = c1 if i%2==0 else c2
        with col:
            st.markdown(f'<div style="background:white;border-radius:14px;padding:1.2rem;margin-bottom:1rem;border-left:4px solid #7c3aed;box-shadow:0 2px 8px rgba(124,58,237,0.08);"><div style="font-size:1.5rem;margin-bottom:0.3rem">{icon}</div><div style="font-weight:700;color:#4c1d95;margin-bottom:0.3rem">{title}</div><div style="color:#6b7a99;font-size:0.88rem">{desc}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📚 Useful Resources")
    r1,r2,r3,r4 = st.columns(4)
    resources = [("🎓","IELTS Practice","ielts.org","https://www.ielts.org"),("💻","Free Courses","Coursera.org","https://www.coursera.org"),("🇩🇰","Study in Denmark","studyindenmark.dk","https://www.studyindenmark.dk"),("🏫","CBS Programs","cbs.dk","https://www.cbs.dk/en/study/graduate")]
    for col,(icon,label,site,url) in zip([r1,r2,r3,r4],resources):
        with col:
            st.markdown(f'<div style="background:linear-gradient(135deg,#f0fdfa,#ccfbf1);border-radius:14px;padding:1.2rem;text-align:center;border:1px solid #99f6e4;"><div style="font-size:1.8rem">{icon}</div><div style="font-weight:700;color:#0f766e;margin:0.3rem 0 0.2rem">{label}</div><a href="{url}" target="_blank" style="color:#14b8a6;font-size:0.8rem">{site}</a></div>', unsafe_allow_html=True)


# ===== PAGE 4: SYSTEM STATUS =====
elif page == "⚙️ System Status":
    from datetime import date as dt_date

    st.markdown("## System Status & Live Data")

    st.markdown("### 🟢 Services")
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        try:
            ok = requests.get(f"{API_URL}/health", timeout=5).status_code == 200
            st.markdown(f'<div class="{"alert-ok" if ok else "alert-high"}">{"✅ API Running" if ok else "❌ API Offline"}</div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="alert-high">❌ API Offline</div>', unsafe_allow_html=True)
    with c2:
        try:
            n = requests.get(f"{API_URL}/programs", timeout=5).json().get("count",0)
            st.markdown(f'<div class="stat-box"><div class="stat-value">{n}</div><div class="stat-label">Programs Loaded</div></div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="stat-box"><div class="stat-value">–</div><div class="stat-label">Programs Loaded</div></div>', unsafe_allow_html=True)
    with c3:
        try:
            n = requests.get(f"{API_URL}/courses", timeout=5).json().get("count",0)
            st.markdown(f'<div class="stat-box"><div class="stat-value">{n}</div><div class="stat-label">Courses Available</div></div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="stat-box"><div class="stat-value">–</div><div class="stat-label">Courses Available</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="stat-box"><div class="stat-value" style="font-size:1.2rem">{dt_date.today().strftime("%d %b %Y")}</div><div class="stat-label">Today\'s Date</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💱 Live Exchange Rates (fetched daily)")

    # Try API first, fall back to database directly (for Streamlit Cloud)
    rates = {}
    rate_source = "API"
    try:
        rates_resp = requests.get(f"{API_URL}/exchange-rates", timeout=8)
        if rates_resp.status_code == 200:
            rates = rates_resp.json().get("latest_rates", {})
            rate_source = "API"
    except:
        pass

    # Fallback: read directly from database when API is offline
    if not rates and PIPELINE_DIRECT:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM exchange_rates ORDER BY date DESC LIMIT 1")
            columns = [d[0] for d in cursor.description]
            row = cursor.fetchone()
            conn.close()
            if row:
                rates = dict(zip(columns, row))
                rate_source = "Database"
        except:
            pass

    if rates:
        rate_date = rates.get("date", "today")
        st.caption(f"Last updated: **{rate_date}** · Source: frankfurter.app + open.er-api.com · Updated daily via GitHub Actions · _{rate_source}_")
        r1,r2,r3,r4,r5 = st.columns(5)
        for col,(label,key) in zip([r1,r2,r3,r4,r5],[("🇳🇵 NPR","dkk_to_npr"),("🇮🇳 INR","dkk_to_inr"),("🇺🇸 USD","dkk_to_usd"),("🇪🇺 EUR","dkk_to_eur"),("🇬🇧 GBP","dkk_to_gbp")]):
            val = rates.get(key, 0)
            with col:
                st.markdown(f'<div class="stat-box"><div class="stat-value" style="font-size:1.4rem">{val:.4f}</div><div class="stat-label">{label}</div><div style="font-size:0.7rem;color:#9ca3af;margin-top:4px">1 DKK =</div></div>', unsafe_allow_html=True)

        st.markdown("<br>**Example: MSc Finance @ CBS (85,000 DKK/year)**", unsafe_allow_html=True)
        ex1,ex2,ex3 = st.columns(3)
        npr_val = rates.get("dkk_to_npr", 0)
        inr_val = rates.get("dkk_to_inr", 0)
        usd_val = rates.get("dkk_to_usd", 0)
        with ex1:
            st.markdown(f'<div class="cost-card cost-card-npr"><div class="currency">🇳🇵 Nepali Rupee</div><div class="amount">{int(85000*npr_val):,}</div><div class="per-year">NPR / year</div></div>', unsafe_allow_html=True)
        with ex2:
            st.markdown(f'<div class="cost-card cost-card-inr"><div class="currency">🇮🇳 Indian Rupee</div><div class="amount">{int(85000*inr_val):,}</div><div class="per-year">INR / year</div></div>', unsafe_allow_html=True)
        with ex3:
            st.markdown(f'<div class="cost-card cost-card-usd"><div class="currency">🇺🇸 US Dollar</div><div class="amount">{int(85000*usd_val):,}</div><div class="per-year">USD / year</div></div>', unsafe_allow_html=True)
    else:
        st.warning("Exchange rates not available — run `python pipeline.py` first to fetch rates.")

    st.markdown("---")
    st.markdown("### ⏳ Application Deadline Countdown")
    st.caption("All deadlines are January 15, 2027 — calculated live from today's date")
    PROGRAMS_DEADLINES = [
        ("MSc Finance — CBS","2027-01-15"),("MSc Business Admin & Data Science — CBS","2027-01-15"),
        ("MSc Accounting Strategy — CBS","2027-01-15"),("MSc Data Science — DTU","2027-01-15"),
        ("MSc AI and Data — DTU","2027-01-15"),("MSc Data Science — AAU","2027-03-01"),
        ("MSc AI — AAU","2027-03-01"),("MSc Business Intelligence — AU","2027-02-01"),
    ]
    today = dt_date.today()
    d1,d2 = st.columns(2)
    for i,(prog,dl_str) in enumerate(PROGRAMS_DEADLINES):
        deadline  = dt_date.fromisoformat(dl_str)
        days_left = (deadline-today).days
        urgency   = "🔴" if days_left<100 else ("🟡" if days_left<200 else "✅")
        card_cls  = "deadline-urgent" if days_left<100 else "deadline-ok"
        col = d1 if i%2==0 else d2
        with col:
            st.markdown(f'<div class="{card_cls}"><div class="deadline-name">{urgency} {prog}</div><div><span class="deadline-days">{days_left}</span><span style="color:#6b7a99;font-size:0.85rem"> days · {deadline.strftime("%d %b %Y")}</span></div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔄 Recent Pipeline Runs")
    runs = []
    try:
        runs = requests.get(f"{API_URL}/pipeline-runs", timeout=10).json().get("runs",[])
    except:
        pass
    if not runs and PIPELINE_DIRECT:
        try:
            conn = get_connection(); cursor = conn.cursor()
            cursor.execute("SELECT * FROM pipeline_runs ORDER BY created_at DESC LIMIT 20")
            columns = [d[0] for d in cursor.description]
            runs = [dict(zip(columns,row)) for row in cursor.fetchall()]
            conn.close()
        except:
            pass
    if runs: st.dataframe(pd.DataFrame(runs), use_container_width=True)
    else: st.info("No pipeline runs yet — click 'Analyse My Profile' to create one.")

    st.markdown("### 🚨 Monitoring Alerts")
    alerts = []
    try:
        alerts = requests.get(f"{API_URL}/monitoring-alerts", timeout=10).json().get("alerts",[])
    except:
        pass
    if not alerts and PIPELINE_DIRECT:
        try:
            conn = get_connection(); cursor = conn.cursor()
            cursor.execute("SELECT * FROM monitoring_alerts ORDER BY timestamp DESC LIMIT 10")
            columns = [d[0] for d in cursor.description]
            alerts = [dict(zip(columns,row)) for row in cursor.fetchall()]
            conn.close()
        except:
            pass
    if not alerts:
        st.markdown('<div class="alert-ok">✅ No alerts — all data is stable</div>', unsafe_allow_html=True)
    else:
        for a in alerts[:5]:
            sev  = a.get("severity","").upper()
            cls  = "alert-high" if sev=="HIGH" else ("alert-medium" if sev=="MEDIUM" else "alert-ok")
            icon = "🔴" if sev=="HIGH" else ("🟡" if sev=="MEDIUM" else "🟢")
            st.markdown(f'<div class="{cls}">{icon} <b>{a.get("alert_type","")}</b> — {a.get("message","")}</div>', unsafe_allow_html=True)

    st.markdown("### 💬 User Feedback")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_feedback ORDER BY created_at DESC LIMIT 10")
        columns = [d[0] for d in cursor.description]
        feedback = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        if feedback:
            st.dataframe(pd.DataFrame(feedback), use_container_width=True)
        else:
            st.info("No feedback yet.")
    except:
        st.info("No feedback yet.")
# ===== FOOTER =====
st.markdown("---")
st.markdown("<p style='text-align:center;color:#9ca3af;font-size:0.8rem;'>StudyBuddy DK © 2026 · MLOps Assignment · Alina Shrestha · API: <code>127.0.0.1:8000</code> · Docs: <code>127.0.0.1:8000/docs</code></p>", unsafe_allow_html=True)