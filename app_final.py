"""
StudyBuddy DK — Final Streamlit Dashboard
"""

import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="StudyBuddy DK",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ===== CUSTOM CSS =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

/* ── HEADER ── */
.hero {
    background: linear-gradient(135deg, #0f2352 0%, #1a3a7a 50%, #0f2352 100%);
    border-radius: 20px;
    padding: 3rem 2rem 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: -40px;
    width: 150px; height: 150px;
    background: rgba(255,255,255,0.03);
    border-radius: 50%;
}
.hero h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 3rem;
    color: white;
    margin: 0 0 0.5rem 0;
    letter-spacing: -1px;
}
.hero p {
    color: rgba(255,255,255,0.75);
    font-size: 1.1rem;
    margin: 0;
}
.hero .flag-row {
    font-size: 1.6rem;
    margin-bottom: 1rem;
    letter-spacing: 6px;
}

/* ── CARDS ── */
.program-card {
    background: white;
    border: 1px solid #e8edf5;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    transition: box-shadow 0.2s;
    box-shadow: 0 2px 8px rgba(15,35,82,0.06);
}
.program-card:hover {
    box-shadow: 0 8px 24px rgba(15,35,82,0.12);
}
.rank-badge {
    position: absolute;
    top: 1.2rem; right: 1.2rem;
    background: #0f2352;
    color: white;
    border-radius: 50%;
    width: 36px; height: 36px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.9rem;
}
.program-name {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f2352;
    margin: 0 0 0.25rem 0;
}
.university-name {
    color: #6b7a99;
    font-size: 0.9rem;
    margin: 0 0 1rem 0;
}

/* ── SCORE BAR ── */
.score-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 0.75rem;
}
.score-label {
    font-size: 0.85rem;
    color: #6b7a99;
    width: 80px;
    flex-shrink: 0;
}
.score-bar-bg {
    flex: 1;
    background: #f0f3fa;
    border-radius: 99px;
    height: 10px;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.6s ease;
}
.score-value {
    font-weight: 700;
    font-size: 0.9rem;
    width: 45px;
    text-align: right;
    flex-shrink: 0;
}

/* ── ELIGIBILITY PILL ── */
.pill-eligible {
    display: inline-block;
    background: #e8f5e9;
    color: #2e7d32;
    border: 1px solid #a5d6a7;
    border-radius: 99px;
    padding: 0.25rem 0.9rem;
    font-size: 0.8rem;
    font-weight: 600;
}
.pill-gaps {
    display: inline-block;
    background: #fff8e1;
    color: #f57f17;
    border: 1px solid #ffe082;
    border-radius: 99px;
    padding: 0.25rem 0.9rem;
    font-size: 0.8rem;
    font-weight: 600;
}

/* ── GAP CARD ── */
.gap-card {
    background: #fffbf0;
    border-left: 4px solid #f59e0b;
    border-radius: 0 12px 12px 0;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
}
.gap-card .gap-title {
    font-weight: 700;
    color: #92400e;
    font-size: 1rem;
    margin-bottom: 0.3rem;
}
.gap-card .gap-sub {
    color: #78716c;
    font-size: 0.85rem;
}

/* ── COST CARD ── */
.cost-card {
    background: linear-gradient(135deg, #0f2352, #1a3a7a);
    color: white;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
}
.cost-card .currency {
    font-size: 0.8rem;
    opacity: 0.7;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.25rem;
}
.cost-card .amount {
    font-size: 1.8rem;
    font-weight: 700;
    font-family: 'DM Serif Display', serif;
}
.cost-card .per-year {
    font-size: 0.75rem;
    opacity: 0.6;
    margin-top: 0.2rem;
}

/* ── DEADLINE ── */
.deadline-urgent {
    background: #fef2f2;
    border: 1px solid #fca5a5;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
}
.deadline-ok {
    background: #f0fdf4;
    border: 1px solid #86efac;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
}
.deadline-name {
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 0.2rem;
}
.deadline-days {
    font-size: 1.4rem;
    font-weight: 700;
}

/* ── READINESS SCORE ── */
.readiness-circle {
    background: linear-gradient(135deg, #0f2352, #2563eb);
    border-radius: 50%;
    width: 120px; height: 120px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    color: white;
    margin: 0 auto 1rem;
    box-shadow: 0 8px 24px rgba(15,35,82,0.3);
}
.readiness-circle .pct {
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
}
.readiness-circle .label {
    font-size: 0.65rem;
    opacity: 0.75;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── STAT BOX ── */
.stat-box {
    background: white;
    border: 1px solid #e8edf5;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(15,35,82,0.05);
}
.stat-box .stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #0f2352;
    font-family: 'DM Serif Display', serif;
}
.stat-box .stat-label {
    font-size: 0.8rem;
    color: #6b7a99;
    margin-top: 0.2rem;
}

/* ── COURSE CHIP ── */
.course-chip {
    display: inline-block;
    background: #f0f3fa;
    border: 1px solid #d0d8ee;
    border-radius: 8px;
    padding: 0.4rem 0.8rem;
    font-size: 0.82rem;
    margin: 0.25rem 0.25rem 0 0;
    color: #374151;
}
.course-chip .free-tag {
    color: #059669;
    font-weight: 600;
}

/* ── ALERT ── */
.alert-high {
    background: #fef2f2; border-left: 4px solid #ef4444;
    border-radius: 0 8px 8px 0; padding: 0.8rem 1rem; margin-bottom: 0.5rem;
    color: #991b1b; font-size: 0.9rem;
}
.alert-medium {
    background: #fffbeb; border-left: 4px solid #f59e0b;
    border-radius: 0 8px 8px 0; padding: 0.8rem 1rem; margin-bottom: 0.5rem;
    color: #92400e; font-size: 0.9rem;
}
.alert-ok {
    background: #f0fdf4; border-left: 4px solid #22c55e;
    border-radius: 0 8px 8px 0; padding: 0.8rem 1rem; margin-bottom: 0.5rem;
    color: #166534; font-size: 0.9rem;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #f7f9fd !important;
}
</style>
""", unsafe_allow_html=True)


# ===== HELPERS =====
def api_ok():
    try:
        return requests.get(f"{API_URL}/health", timeout=4).status_code == 200
    except:
        return False

def score_color(score):
    if score >= 85: return "#22c55e"
    if score >= 70: return "#f59e0b"
    return "#ef4444"

def readiness_score(result):
    """Calculate an overall readiness % from gaps and match score."""
    top = result.get("top_programs", [])
    gaps = result.get("gaps", [])
    match = top[0]["match_score"] if top else 0
    gap_penalty = len(gaps) * 8
    score = max(0, min(100, match - gap_penalty))
    return int(score)


# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### 🎓 StudyBuddy DK")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🔍 Program Finder", "📊 Program Explorer", "📖 Preparation Guide", "⚙️ System Status"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("**17 programs** from 6 universities")
    st.markdown("**Live** exchange rates daily")
    st.markdown("**AI-powered** gap analysis")
    st.markdown("---")
    st.caption("MLOps Assignment · Alina Shrestha · April 2026")


# ===== HERO HEADER =====
st.markdown("""
<div class="hero">
    <div class="flag-row">🇩🇰</div>
    <h1>StudyBuddy DK</h1>
    <p>AI-powered Danish master's program finder for international students</p>
</div>
""", unsafe_allow_html=True)


# ===== ECTS CONVERSION FACTORS =====
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
    "Quantitative / Math": "Courses like Statistics, Mathematics, Econometrics, Operations Research",
    "Programming / CS": "Courses like Python, Java, Databases, Data Structures, IT, Computer Science",
    "Research / Thesis": "Final year project, dissertation, research methods, thesis credits",
}

# ===== PAGE 1: PROGRAM FINDER =====
if page == "🔍 Program Finder":

    if not api_ok():
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
        credit_system = st.selectbox(
            "🌍 Your university's credit system",
            list(CREDIT_SYSTEMS.keys()),
            help="Select the credit system your university uses. We'll convert to ECTS automatically."
        )
        factor = CREDIT_SYSTEMS[credit_system]
        if factor != 1.0:
            st.info(f"ℹ️ Conversion: your credits × {factor:.2f} = ECTS")

    st.markdown("---")
    st.markdown("#### Step 2 — ECTS Calculator")

    # ── AI TRANSCRIPT READER ──
    with st.expander("🤖 Auto-fill from transcript photo (AI-powered)", expanded=False):
        st.markdown("Upload a photo of your transcript and AI will read it and fill in your credits automatically.")
        st.caption("Supports Nepali, Indian, Pakistani, Bangladeshi and most Asian university transcripts.")

        uploaded = st.file_uploader(
            "Upload transcript image",
            type=["jpg", "jpeg", "png"],
            key="transcript_upload"
        )

        if uploaded is not None:
            import base64, json as _json

            col_img, col_btn = st.columns([2, 1])
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
                        ext       = uploaded.name.split(".")[-1].lower()
                        mime      = "image/jpeg" if ext in ["jpg","jpeg"] else "image/png"

                        prompt = """You are an academic credit analyser. Look at this university transcript carefully.

Extract ALL courses and categorise them into exactly these 4 areas:
1. business_credits — Business, Management, Finance, Accounting, Marketing, HRM, Strategy, Banking, Economics, Law, Sociology
2. quant_credits — Mathematics, Statistics, Econometrics, Operations Research, Calculus
3. programming_credits — IT, Computer Science, Programming, Databases, Data Structures, Information Systems
4. research_credits — Thesis, Project, Dissertation, Research Methods, Internship, Capstone

For each area, sum up the total credit hours of courses that belong there.
Also extract: total_credits, credit_system (e.g. "Nepali Credit Hours"), cgpa, degree_name, university_name.

Respond ONLY with valid JSON, no explanation, no markdown:
{
  "degree_name": "...",
  "university_name": "...",
  "credit_system": "...",
  "total_credits": 0,
  "cgpa": "...",
  "business_credits": 0,
  "quant_credits": 0,
  "programming_credits": 0,
  "research_credits": 0,
  "courses_found": 0,
  "confidence": "high/medium/low",
  "notes": "..."
}"""

                        response = __import__("requests").post(
                            "https://api.anthropic.com/v1/messages",
                            headers={"Content-Type": "application/json"},
                            json={
                                "model": "claude-sonnet-4-6",
                                "max_tokens": 1000,
                                "messages": [{
                                    "role": "user",
                                    "content": [
                                        {"type": "image", "source": {"type": "base64", "media_type": mime, "data": img_b64}},
                                        {"type": "text",  "text": prompt}
                                    ]
                                }]
                            },
                            timeout=30
                        )

                        if response.status_code == 200:
                            raw_text = response.json()["content"][0]["text"].strip()
                            # Clean any accidental markdown
                            raw_text = raw_text.replace("```json","").replace("```","").strip()
                            extracted = _json.loads(raw_text)

                            st.success("✅ Transcript read successfully!")

                            # Store in session state so inputs below can use them
                            st.session_state["ai_business"]    = float(extracted.get("business_credits", 0))
                            st.session_state["ai_quant"]       = float(extracted.get("quant_credits", 0))
                            st.session_state["ai_programming"]  = float(extracted.get("programming_credits", 0))
                            st.session_state["ai_research"]    = float(extracted.get("research_credits", 0))
                            st.session_state["ai_total"]       = float(extracted.get("total_credits", 0))
                            st.session_state["ai_cgpa"]        = extracted.get("cgpa", "")
                            st.session_state["ai_degree"]      = extracted.get("degree_name", "")
                            st.session_state["ai_university"]  = extracted.get("university_name", "")
                            st.session_state["ai_confidence"]  = extracted.get("confidence", "")
                            st.session_state["ai_notes"]       = extracted.get("notes", "")

                            # Show summary
                            e1, e2, e3, e4, e5 = st.columns(5)
                            for col, label, val in [
                                (e1, "Total Credits",  extracted.get("total_credits",0)),
                                (e2, "Business",       extracted.get("business_credits",0)),
                                (e3, "Quant/Math",     extracted.get("quant_credits",0)),
                                (e4, "Programming",    extracted.get("programming_credits",0)),
                                (e5, "Research",       extracted.get("research_credits",0)),
                            ]:
                                with col:
                                    st.markdown(f'<div class="stat-box"><div class="stat-value">{val}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

                            st.markdown("<br>", unsafe_allow_html=True)
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

    # Use AI-extracted values if available, otherwise default to 0
    default_b = st.session_state.get("ai_business", 0.0)
    default_q = st.session_state.get("ai_quant", 0.0)
    default_p = st.session_state.get("ai_programming", 0.0)
    default_r = st.session_state.get("ai_research", 0.0)

    rows = []
    for subject, hint, default_val in zip(
        list(SUBJECT_HINTS.keys()),
        list(SUBJECT_HINTS.values()),
        [default_b, default_q, default_p, default_r]
    ):
        c1, c2, c3, c4 = st.columns([3, 2, 2, 3])
        with c1:
            st.markdown(f"**{subject}**")
            st.caption(hint)
        with c2:
            raw = st.number_input(
                f"Credits ({subject[:4]})",
                min_value=0.0, max_value=500.0, value=float(default_val), step=1.0,
                key=f"raw_{subject}",
                label_visibility="collapsed"
            )
        with c3:
            ects_val = round(raw * factor, 1)
            st.metric("ECTS", ects_val, label_visibility="visible")
        with c4:
            st.caption(f"= {raw} × {factor:.2f}")
        rows.append(ects_val)

    ects_b, ects_q, ects_p, ects_r = rows[0], rows[1], rows[2], rows[3]
    total = ects_b + ects_q + ects_p + ects_r

    # Summary bar
    col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns(5)
    with col_t1:
        st.markdown(f"""<div class="stat-box"><div class="stat-value">{total:.0f}</div><div class="stat-label">Total ECTS</div></div>""", unsafe_allow_html=True)
    with col_t2:
        st.markdown(f"""<div class="stat-box"><div class="stat-value">{ects_b:.0f}</div><div class="stat-label">Business</div></div>""", unsafe_allow_html=True)
    with col_t3:
        st.markdown(f"""<div class="stat-box"><div class="stat-value">{ects_q:.0f}</div><div class="stat-label">Quant</div></div>""", unsafe_allow_html=True)
    with col_t4:
        st.markdown(f"""<div class="stat-box"><div class="stat-value">{ects_p:.0f}</div><div class="stat-label">Programming</div></div>""", unsafe_allow_html=True)
    with col_t5:
        st.markdown(f"""<div class="stat-box"><div class="stat-value">{ects_r:.0f}</div><div class="stat-label">Research</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Typical ECTS reference
    with st.expander("📖 What counts as ECTS in each area? (click to see examples)"):
        st.markdown("""
        | Subject Area | Examples of courses that count |
        |---|---|
        | **Business / Management** | Accounting, Finance, Marketing, Strategy, HRM, Operations Mgmt, Business Law |
        | **Quantitative / Math** | Statistics, Mathematics, Econometrics, Calculus, Linear Algebra, Operations Research |
        | **Programming / CS** | Python, Java, Databases, Data Structures, Algorithms, IT Systems, Computer Science |
        | **Research / Thesis** | Final Year Project, Dissertation, Research Methods, Thesis, Capstone Project |

        **Conversion guide:**
        - Nepal/India 3-credit course → 3 × 2 = **6 ECTS**
        - US 3-credit course → 3 × 1.5 = **4.5 ECTS**
        - A full 4-year bachelor = ~240 ECTS
        - A full 3-year bachelor = ~180 ECTS
        """)

    st.markdown("#### Step 3 — Analyse")
    if st.button("🚀 Analyse My Profile", use_container_width=True, type="primary"):
        if not name or not degree:
            st.error("Please fill in name and degree.")
        else:
            with st.spinner("Running pipeline…"):
                try:
                    payload = {
                        "name": name, "degree": degree,
                        "ects_business": float(ects_b),
                        "ects_quantitative": float(ects_q),
                        "ects_programming": float(ects_p),
                        "ects_research": float(ects_r),
                        "ielts": float(ielts),
                        "country": country,
                        "eu_student": eu_flag
                    }
                    resp = requests.post(f"{API_URL}/analyse", json=payload, timeout=30)

                    if resp.status_code != 200:
                        st.error(f"API error {resp.status_code}: {resp.text}")
                        st.stop()

                    result = resp.json()
                    st.success("✅ Analysis complete!")

                    # ── NORMALISE KEYS from pipeline ──
                    top_programs  = result.get("top_programs", [])
                    gaps          = result.get("gaps", [])
                    recommendations = result.get("recommendations", [])
                    costs_raw     = result.get("costs", {})
                    costs         = costs_raw if isinstance(costs_raw, dict) else (costs_raw[0] if costs_raw else {})
                    deadlines     = result.get("deadlines", [])
                    alerts        = result.get("monitoring_alerts", [])
                    readiness     = readiness_score(result)

                    s1, s2, s3, s4 = st.columns(4)
                    with s1:
                        top_score = top_programs[0].get("match_score", 0) if top_programs else 0
                        st.markdown(f"""<div class="stat-box">
                            <div class="stat-value">{top_score:.0f}%</div>
                            <div class="stat-label">Top Match Score</div></div>""", unsafe_allow_html=True)
                    with s2:
                        st.markdown(f"""<div class="stat-box">
                            <div class="stat-value">{len(gaps)}</div>
                            <div class="stat-label">Skill Gaps Found</div></div>""", unsafe_allow_html=True)
                    with s3:
                        cost_val = costs.get("tuition_dkk", 0)
                        st.markdown(f"""<div class="stat-box">
                            <div class="stat-value">{int(cost_val):,}</div>
                            <div class="stat-label">DKK / Year</div></div>""", unsafe_allow_html=True)
                    with s4:
                        days = deadlines[0].get("days_left", deadlines[0].get("days_remaining", 0)) if deadlines else 0
                        st.markdown(f"""<div class="stat-box">
                            <div class="stat-value">{days}</div>
                            <div class="stat-label">Days to Deadline</div></div>""", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # ── TABS ──
                    t1, t2, t3, t4, t5 = st.tabs(
                        ["🏆 Top Matches", "🎯 Gap Analysis", "💰 Costs", "📅 Deadlines", "📈 Monitoring"]
                    )

                    # TAB 1 — TOP MATCHES
                    with t1:
                        if not top_programs:
                            st.info("No programs found.")
                        for i, p in enumerate(top_programs[:3], 1):
                            score  = p.get("match_score", 0)
                            elig   = p.get("eligibility", {})
                            is_eligible = elig.get("eligible", False) if isinstance(elig, dict) else bool(elig)
                            color  = score_color(score)
                            pill   = '<span class="pill-eligible">✅ Eligible</span>' if is_eligible else '<span class="pill-gaps">⚠️ Gaps found</span>'
                            # Extra program info
                            location = p.get("location", "")
                            deadline = p.get("deadline", "")
                            tuition  = p.get("tuition_dkk", 0)
                            st.markdown(f"""
                            <div class="program-card">
                                <div class="rank-badge">{i}</div>
                                <div class="program-name">{p.get('program_name','')}</div>
                                <div class="university-name">{p.get('university_full', p.get('university',''))} · {location}</div>
                                <div class="score-row">
                                    <div class="score-label">Match</div>
                                    <div class="score-bar-bg">
                                        <div class="score-bar-fill" style="width:{score}%;background:{color}"></div>
                                    </div>
                                    <div class="score-value" style="color:{color}">{score:.0f}%</div>
                                </div>
                                {pill}
                                <div style="margin-top:0.5rem;font-size:0.8rem;color:#6b7a99;">
                                    📅 Deadline: {deadline} &nbsp;·&nbsp; 💰 {int(tuition):,} DKK/year (non-EU)
                                </div>
                            </div>""", unsafe_allow_html=True)

                        # Readiness circle
                        st.markdown("<br>", unsafe_allow_html=True)
                        rc1, rc2, rc3 = st.columns([1,1,1])
                        with rc2:
                            st.markdown(f"""
                            <div class="readiness-circle">
                                <div class="pct">{readiness}%</div>
                                <div class="label">Readiness</div>
                            </div>
                            <p style="text-align:center;color:#6b7a99;font-size:0.85rem;">
                                Overall readiness for your top match
                            </p>""", unsafe_allow_html=True)

                    # TAB 2 — GAP ANALYSIS
                    with t2:
                        if not gaps:
                            st.success("🎉 No skill gaps — you meet all requirements!")
                        else:
                            st.markdown(f"**{len(gaps)} gap(s) found.** Here's what to work on:")
                            for gap in gaps:
                                # Support both key styles
                                skill    = gap.get("area", gap.get("skill", ""))
                                have     = gap.get("have", gap.get("have_ects", 0))
                                need     = gap.get("need", gap.get("need_ects", 0))
                                missing  = gap.get("missing", need - have)
                                priority = gap.get("priority", "medium")
                                gap_type = gap.get("type", "ects")
                                icon     = "🔴" if priority == "high" else "🟡"

                                if gap_type == "ielts":
                                    sub = f"Your IELTS: {have} · Required: {need} · Gap: {missing:.1f} points"
                                else:
                                    sub = f"You have {have} ECTS · Need {need} ECTS · Gap: {missing} ECTS"

                                st.markdown(f"""
                                <div class="gap-card">
                                    <div class="gap-title">{icon} {skill}</div>
                                    <div class="gap-sub">{sub}</div>
                                </div>""", unsafe_allow_html=True)
                                st.markdown("<br>", unsafe_allow_html=True)

                        # Show course recommendations (separate from gaps)
                        if recommendations:
                            st.markdown("---")
                            st.markdown(f"**📚 Recommended courses to fill your gaps:**")
                            for rec in recommendations:
                                # Each rec has {"gap": "...", "courses": [...]}
                                gap_name = rec.get("gap", "")
                                courses  = rec.get("courses", [])
                                # If it's a flat course dict instead
                                if "course_name" in rec:
                                    courses = [rec]
                                    gap_name = rec.get("skill", "")
                                if gap_name:
                                    st.markdown(f"**For {gap_name}:**")
                                chips = ""
                                for c in courses:
                                    cost_str   = c.get("cost", c.get("cost_dkk", "Free"))
                                    free_tag   = '<span class="free-tag">FREE</span>' if "free" in str(cost_str).lower() else cost_str
                                    rating     = c.get("rating", "")
                                    rating_str = f"⭐ {rating}" if rating else ""
                                    url        = c.get("url", "#")
                                    name       = c.get("course_name", c.get("name", ""))
                                    platform   = c.get("platform", "")
                                    chips += f'<span class="course-chip">📚 <a href="{url}" target="_blank" style="color:inherit;text-decoration:none">{name}</a> · {platform} · {free_tag} {rating_str}</span>'
                                st.markdown(chips, unsafe_allow_html=True)
                                st.markdown("<br>", unsafe_allow_html=True)

                    # TAB 3 — COSTS
                    with t3:
                        if not costs:
                            st.info("No cost data available.")
                        else:
                            dkk  = costs.get("tuition_dkk", 0)
                            npr  = costs.get("tuition_npr", 0)
                            inr  = costs.get("tuition_inr", 0)
                            usd  = costs.get("tuition_usd", 0)
                            date = costs.get("rate_date", costs.get("exchange_rate_date", "today"))

                            cc1, cc2, cc3, cc4 = st.columns(4)
                            for col, currency, amount, flag in [
                                (cc1,"DKK / Year", f"{int(dkk):,}","🇩🇰"),
                                (cc2,"NPR / Year",  f"{int(npr):,}","🇳🇵"),
                                (cc3,"INR / Year",  f"{int(inr):,}","🇮🇳"),
                                (cc4,"USD / Year",  f"{int(usd):,}","🇺🇸"),
                            ]:
                                with col:
                                    st.markdown(f"""
                                    <div class="cost-card">
                                        <div class="currency">{flag} {currency}</div>
                                        <div class="amount">{amount}</div>
                                        <div class="per-year">Tuition only</div>
                                    </div>""", unsafe_allow_html=True)

                            st.markdown(f"<br><p style='color:#6b7a99;font-size:0.85rem;text-align:center'>Exchange rates as of <b>{date}</b> · fetched daily via GitHub Actions</p>", unsafe_allow_html=True)

                            # Bar chart
                            st.markdown("#### Visual Comparison")
                            chart_df = pd.DataFrame({
                                "Currency": ["DKK","NPR (÷100)","INR (÷100)","USD"],
                                "Amount":   [dkk, npr/100, inr/100, usd]
                            })
                            st.bar_chart(chart_df.set_index("Currency"))

                    # TAB 4 — DEADLINES
                    with t4:
                        if not deadlines:
                            st.info("No deadline data available.")
                        else:
                            for d in deadlines:
                                # Support both key styles
                                pname  = d.get("program", d.get("program_name", ""))
                                days_r = d.get("days_left", d.get("days_remaining", 0))
                                dl     = d.get("deadline", "TBD")
                                status = d.get("status", "")
                                univ   = d.get("university", "")
                                card_class = "deadline-urgent" if days_r < 100 else "deadline-ok"
                                emoji  = "🔴" if days_r < 100 else "✅"
                                st.markdown(f"""
                                <div class="{card_class}">
                                    <div class="deadline-name">{emoji} {pname} — {univ}</div>
                                    <div>
                                        <span class="deadline-days">{days_r}</span>
                                        <span style="color:#6b7a99;font-size:0.85rem"> days remaining · {dl}</span>
                                    </div>
                                </div>""", unsafe_allow_html=True)

                    # TAB 5 — MONITORING
                    with t5:
                        runtime = result.get("runtime_seconds", 0)
                        ts      = result.get("timestamp","")[:10]

                        m1, m2 = st.columns(2)
                        with m1:
                            st.markdown(f"""<div class="stat-box">
                                <div class="stat-value">{runtime:.2f}s</div>
                                <div class="stat-label">Pipeline Runtime</div></div>""", unsafe_allow_html=True)
                        with m2:
                            st.markdown(f"""<div class="stat-box">
                                <div class="stat-value">{ts}</div>
                                <div class="stat-label">Run Date</div></div>""", unsafe_allow_html=True)

                        st.markdown("<br>**Monitoring Alerts**", unsafe_allow_html=True)
                        if not alerts:
                            st.markdown('<div class="alert-ok">✅ All systems operational — no alerts</div>', unsafe_allow_html=True)
                        else:
                            for a in alerts:
                                sev = str(a.get("severity","")).upper() if isinstance(a, dict) else "INFO"
                                msg = a.get("message", str(a)) if isinstance(a, dict) else str(a)
                                cls = "alert-high" if sev == "HIGH" else ("alert-medium" if sev == "MEDIUM" else "alert-ok")
                                icon = "🔴" if sev == "HIGH" else ("🟡" if sev == "MEDIUM" else "🟢")
                                st.markdown(f'<div class="{cls}">{icon} {msg}</div>', unsafe_allow_html=True)

                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {e}")
                except Exception as e:
                    st.error(f"Error: {e}")


# ===== PAGE 2: PROGRAM EXPLORER =====
elif page == "📊 Program Explorer":
    st.markdown("## All 17 Danish Programs")
    try:
        resp = requests.get(f"{API_URL}/programs", timeout=10)
        if resp.status_code == 200:
            programs = resp.json().get("programs", [])
            if programs:
                df = pd.DataFrame(programs)
                unis = st.multiselect("Filter by University", df["university"].unique().tolist(),
                                      default=df["university"].unique().tolist())
                filtered = df[df["university"].isin(unis)]
                display_cols = [c for c in ["name","university","ects_required","ielts_min","tuition_non_eu_dkk"] if c in filtered.columns]
                st.dataframe(filtered[display_cols], use_container_width=True)
                st.caption(f"{len(filtered)} programs shown")
        else:
            st.error("Could not fetch programs from API")
    except Exception as e:
        st.error(f"Error: {e}")


# ===== PAGE 3: PREPARATION GUIDE =====
elif page == "📖 Preparation Guide":
    st.markdown("## Your Preparation Roadmap")
    st.markdown("Follow this timeline to be fully ready for your Danish master's application.")

    phases = [
        ("Month 0–1", "Foundation", [
            "Take practice IELTS tests to identify weak areas",
            "Enroll in foundational courses (Python, Statistics)",
            "Review target program syllabi and requirements",
            "Create a detailed weekly study schedule",
        ], "#0f2352"),
        ("Month 1–3", "Skill Building", [
            "Focus on IELTS writing and speaking",
            "Complete core courses — Python, SQL, ML basics",
            "Practice with real datasets and build small projects",
            "Retake IELTS if needed (target: 6.5+)",
        ], "#1a3a7a"),
        ("Month 3–6", "Advanced Topics", [
            "Deepen knowledge in specialised areas",
            "Complete a capstone project or case study",
            "Join study groups or online communities",
            "Prepare application documents and personal statement",
        ], "#2563eb"),
        ("Month 6+", "Application", [
            "Submit completed applications before deadline",
            "Prepare for potential interviews",
            "Strengthen answers with real examples from projects",
            "Stay updated on admissions decisions",
        ], "#16a34a"),
    ]

    for period, title, tasks, color in phases:
        with st.expander(f"📅 {period} — {title}", expanded=(period == "Month 0–1")):
            for t in tasks:
                st.markdown(f"- ✔️ {t}")

    st.markdown("---")
    st.markdown("### 💡 Pro Tips")
    tips = [
        ("Consistency", "Study a little every day rather than cramming"),
        ("Practice Tests", "Take mock IELTS regularly to track progress"),
        ("Real Projects", "Apply learning by building actual projects"),
        ("Community", "Join study groups and connect with other students"),
        ("Balance", "Take regular breaks to avoid burnout"),
    ]
    for tip, desc in tips:
        st.markdown(f"**{tip}** — {desc}")


# ===== PAGE 4: SYSTEM STATUS =====
elif page == "⚙️ System Status":
    from datetime import date as dt_date

    st.markdown("## System Status & Live Data")

    # ── ROW 1: Service health ──
    st.markdown("### 🟢 Services")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        try:
            ok = requests.get(f"{API_URL}/health", timeout=5).status_code == 200
            st.markdown(f'<div class="{"alert-ok" if ok else "alert-high"}">{"✅ API Running" if ok else "❌ API Offline"}</div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="alert-high">❌ API Offline</div>', unsafe_allow_html=True)
    with c2:
        try:
            n = requests.get(f"{API_URL}/programs", timeout=5).json().get("count", 0)
            st.markdown(f'<div class="stat-box"><div class="stat-value">{n}</div><div class="stat-label">Programs Loaded</div></div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="stat-box"><div class="stat-value">–</div><div class="stat-label">Programs Loaded</div></div>', unsafe_allow_html=True)
    with c3:
        try:
            n = requests.get(f"{API_URL}/courses", timeout=5).json().get("count", 0)
            st.markdown(f'<div class="stat-box"><div class="stat-value">{n}</div><div class="stat-label">Courses Available</div></div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="stat-box"><div class="stat-value">–</div><div class="stat-label">Courses Available</div></div>', unsafe_allow_html=True)
    with c4:
        today_str = dt_date.today().strftime("%d %b %Y")
        st.markdown(f'<div class="stat-box"><div class="stat-value" style="font-size:1.2rem">{today_str}</div><div class="stat-label">Today\'s Date</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── ROW 2: Live Exchange Rates ──
    st.markdown("### 💱 Live Exchange Rates (fetched daily)")
    try:
        rates_resp = requests.get(f"{API_URL}/exchange-rates", timeout=8)
        if rates_resp.status_code == 200:
            rates = rates_resp.json().get("latest_rates", {})
            rate_date = rates.get("date", "today")
            st.caption(f"Last updated: **{rate_date}** · Source: frankfurter.app + open.er-api.com · Updated daily via GitHub Actions")

            r1, r2, r3, r4, r5 = st.columns(5)
            rate_data = [
                ("🇳🇵 NPR", "dkk_to_npr", "1 DKK"),
                ("🇮🇳 INR", "dkk_to_inr", "1 DKK"),
                ("🇺🇸 USD", "dkk_to_usd", "1 DKK"),
                ("🇪🇺 EUR", "dkk_to_eur", "1 DKK"),
                ("🇬🇧 GBP", "dkk_to_gbp", "1 DKK"),
            ]
            for col, (label, key, base) in zip([r1,r2,r3,r4,r5], rate_data):
                val = rates.get(key, 0)
                with col:
                    st.markdown(f"""
                    <div class="stat-box">
                        <div class="stat-value" style="font-size:1.4rem">{val:.4f}</div>
                        <div class="stat-label">{label}</div>
                        <div style="font-size:0.7rem;color:#9ca3af;margin-top:4px">{base} =</div>
                    </div>""", unsafe_allow_html=True)

            # Example cost conversion
            st.markdown("<br>**Example: MSc Finance @ CBS (85,000 DKK/year)**", unsafe_allow_html=True)
            ex1, ex2, ex3 = st.columns(3)
            npr_val = rates.get("dkk_to_npr", 0)
            inr_val = rates.get("dkk_to_inr", 0)
            usd_val = rates.get("dkk_to_usd", 0)
            with ex1:
                st.markdown(f'<div class="cost-card"><div class="currency">🇳🇵 Nepali Rupee</div><div class="amount">{int(85000*npr_val):,}</div><div class="per-year">NPR / year</div></div>', unsafe_allow_html=True)
            with ex2:
                st.markdown(f'<div class="cost-card"><div class="currency">🇮🇳 Indian Rupee</div><div class="amount">{int(85000*inr_val):,}</div><div class="per-year">INR / year</div></div>', unsafe_allow_html=True)
            with ex3:
                st.markdown(f'<div class="cost-card"><div class="currency">🇺🇸 US Dollar</div><div class="amount">{int(85000*usd_val):,}</div><div class="per-year">USD / year</div></div>', unsafe_allow_html=True)
        else:
            st.warning("Exchange rates not available — run `python pipeline.py` first to fetch rates.")
    except Exception as e:
        st.error(f"Could not fetch rates: {e}")

    st.markdown("---")

    # ── ROW 3: Deadline Countdown ──
    st.markdown("### ⏳ Application Deadline Countdown")
    st.caption("All deadlines are January 15, 2027 — calculated live from today's date")

    PROGRAMS_DEADLINES = [
        ("MSc Finance — CBS", "2027-01-15"),
        ("MSc Business Admin & Data Science — CBS", "2027-01-15"),
        ("MSc Accounting Strategy — CBS", "2027-01-15"),
        ("MSc Data Science — DTU", "2027-01-15"),
        ("MSc AI and Data — DTU", "2027-01-15"),
        ("MSc Data Science — AAU", "2027-03-01"),
        ("MSc AI — AAU", "2027-03-01"),
        ("MSc Business Intelligence — AU", "2027-02-01"),
    ]

    today = dt_date.today()
    d1, d2 = st.columns(2)
    for i, (prog, dl_str) in enumerate(PROGRAMS_DEADLINES):
        deadline = dt_date.fromisoformat(dl_str)
        days_left = (deadline - today).days
        urgency = "🔴" if days_left < 100 else ("🟡" if days_left < 200 else "✅")
        card_cls = "deadline-urgent" if days_left < 100 else "deadline-ok"
        col = d1 if i % 2 == 0 else d2
        with col:
            st.markdown(f"""
            <div class="{card_cls}">
                <div class="deadline-name">{urgency} {prog}</div>
                <div>
                    <span class="deadline-days">{days_left}</span>
                    <span style="color:#6b7a99;font-size:0.85rem"> days · {deadline.strftime("%d %b %Y")}</span>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── ROW 4: Recent Pipeline Runs ──
    st.markdown("### 🔄 Recent Pipeline Runs")
    try:
        runs = requests.get(f"{API_URL}/pipeline-runs", timeout=10).json().get("runs", [])
        if runs:
            st.dataframe(pd.DataFrame(runs), use_container_width=True)
        else:
            st.info("No pipeline runs yet — click 'Analyse My Profile' to create one.")
    except Exception as e:
        st.error(str(e))

    st.markdown("### 🚨 Monitoring Alerts")
    try:
        alerts = requests.get(f"{API_URL}/monitoring-alerts", timeout=10).json().get("alerts", [])
        if not alerts:
            st.markdown('<div class="alert-ok">✅ No alerts — all data is stable</div>', unsafe_allow_html=True)
        else:
            for a in alerts[:5]:
                sev = a.get("severity", "").upper()
                cls = "alert-high" if sev == "HIGH" else ("alert-medium" if sev == "MEDIUM" else "alert-ok")
                icon = "🔴" if sev == "HIGH" else ("🟡" if sev == "MEDIUM" else "🟢")
                st.markdown(f'<div class="{cls}">{icon} <b>{a.get("alert_type","")}</b> — {a.get("message","")}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(str(e))


# ===== FOOTER =====
st.markdown("---")
st.markdown("""
<p style='text-align:center;color:#9ca3af;font-size:0.8rem;'>
    StudyBuddy DK © 2026 · MLOps Assignment · Alina Shrestha ·
    API: <code>127.0.0.1:8000</code> · Docs: <code>127.0.0.1:8000/docs</code>
</p>
""", unsafe_allow_html=True)