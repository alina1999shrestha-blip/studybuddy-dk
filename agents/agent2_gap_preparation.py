import json
from datetime import datetime, date
from database import get_courses_for_skill, get_latest_exchange_rate, log_pipeline_run

KNOWN_SKILLS = ["Python", "SQL", "Machine Learning", "Statistics",
                "Linear Algebra", "Docker", "R", "Data Analysis", "IELTS"]

def analyse_gaps(profile: dict, top_program: dict) -> dict:
    """
    Agent 2 - Step 1: Find missing ECTS and skills.
    """
    gaps = []
    program = top_program

    # Check ECTS gaps
    checks = [
        ("Programming", profile["ects_programming"],
         program.get("ects_programming_min") or 0),
        ("Quantitative", profile["ects_quant"],
         program.get("ects_quantitative_min") or 0),
        ("Business",    profile["ects_business"],
         program.get("ects_business_min") or 0),
    ]
    for area, have, need in checks:
        if need > 0 and have < need:
            missing = need - have
            priority = "high" if missing > 15 else "medium"
            gaps.append({
                "type":     "ects",
                "area":     area,
                "have":     have,
                "need":     need,
                "missing":  missing,
                "priority": priority
            })

    # Check IELTS gap
    ielts_min = program.get("ielts_min") or 0
    if ielts_min > 0 and profile["ielts_score"] < ielts_min:
        gaps.append({
            "type":     "ielts",
            "area":     "English Language",
            "have":     profile["ielts_score"],
            "need":     ielts_min,
            "missing":  round(ielts_min - profile["ielts_score"], 1),
            "priority": "high"
        })

    # Check programming skills
    if profile["ects_programming"] == 0:
        for skill in ["Python", "SQL"]:
            gaps.append({
                "type":     "skill",
                "area":     skill,
                "have":     0,
                "need":     1,
                "missing":  1,
                "priority": "high"
            })

    return gaps


def recommend_courses(gaps: list) -> list:
    """
    Agent 2 - Step 2: Recommend courses for each gap.
    """
    recommendations = []
    for gap in gaps:
        if gap["type"] == "skill":
            skill = gap["area"]
            courses = get_courses_for_skill(skill)
            if courses:
                recommendations.append({
                    "gap":     gap,
                    "courses": courses[:2]
                })
        elif gap["type"] == "ielts":
            courses = get_courses_for_skill("IELTS")
            if courses:
                recommendations.append({
                    "gap":     gap,
                    "courses": courses[:1]
                })
        elif gap["type"] == "ects":
            area = gap["area"].lower()
            skill_map = {
                "programming": "Python",
                "quantitative": "Statistics",
                "business": "Data Analysis"
            }
            skill = skill_map.get(area)
            if skill:
                courses = get_courses_for_skill(skill)
                if courses:
                    recommendations.append({
                        "gap":     gap,
                        "courses": courses[:1]
                    })
    return recommendations


def calculate_costs(profile: dict, top_program: dict) -> dict:
    """
    Agent 2 - Step 3: Calculate costs in student's home currency.
    """
    # Get tuition from database — check both fields
    if not profile.get("eu_student"):
        tuition_dkk = top_program.get("tuition_non_eu_dkk") or top_program.get("tuition_dkk") or 85000
    else:
        tuition_dkk = top_program.get("tuition_eu_dkk") or 0

    rates = get_latest_exchange_rate()
    costs = {"tuition_dkk": tuition_dkk}

    if rates and tuition_dkk:
        costs["tuition_npr"] = round(tuition_dkk * (rates["dkk_to_npr"] or 0))
        costs["tuition_inr"] = round(tuition_dkk * (rates["dkk_to_inr"] or 0))
        costs["tuition_usd"] = round(tuition_dkk * (rates["dkk_to_usd"] or 0))
        costs["tuition_eur"] = round(tuition_dkk * (rates["dkk_to_eur"] or 0))
        costs["rate_date"]   = rates["date"]
    return costs


def calculate_deadlines(matches: list) -> list:
    """
    Agent 2 - Step 4: Calculate deadline countdowns.
    """
    today = date.today()
    deadlines = []
    for m in matches[:5]:
        dl_str = m.get("deadline")
        if dl_str:
            dl = datetime.strptime(dl_str, "%Y-%m-%d").date()
            days = (dl - today).days
            status = (
                "🔴 URGENT"    if days < 60  else
                "🟡 Soon"      if days < 180 else
                "✅ On track"
            )
            deadlines.append({
                "program":   m["program_name"],
                "university": m["university"],
                "deadline":  dl_str,
                "days_left": days,
                "status":    status
            })
    return deadlines


def run_agent2(agent1_result: dict) -> dict:
    """
    Main Agent 2 function.
    Input:  Agent 1 result
    Output: gaps + courses + costs + deadlines
    """
    print("\n🤖 Agent 2 — Gap Analysis + Preparation + Cost + Deadline")
    print("-" * 55)

    profile  = agent1_result["profile"]
    top3     = agent1_result["top3"]
    matches  = agent1_result["matches"]
    top      = top3[0]

    # Step 1 — gaps
    gaps = analyse_gaps(profile, top)
    print(f"✅ Gaps found: {len(gaps)}")
    for g in gaps:
        print(f"   ⚠️  {g['area']}: have {g['have']} need {g['need']} — priority {g['priority']}")

    # Step 2 — courses
    recommendations = recommend_courses(gaps)
    print(f"\n✅ Course recommendations: {len(recommendations)}")
    for r in recommendations:
        for c in r["courses"]:
            print(f"   📚 {c['course_name']} — {c['platform']} ({c['cost']})")

    # Step 3 — costs
    costs = calculate_costs(profile, top)
    print(f"\n✅ Cost estimates for {top['program_name']}:")
    print(f"   {costs.get('tuition_dkk', 0):,} DKK/year")
    if costs.get("tuition_npr"):
        print(f"   = {costs['tuition_npr']:,} NPR/year")
    if costs.get("tuition_inr"):
        print(f"   = {costs['tuition_inr']:,} INR/year")

    # Step 4 — deadlines
    deadlines = calculate_deadlines(matches)
    print(f"\n✅ Deadlines:")
    for d in deadlines[:3]:
        print(f"   {d['university']} {d['program'][:30]:<30} → {d['days_left']} days {d['status']}")

    log_pipeline_run(
        "agent2_gap_preparation",
        "success",
        f"Gaps: {len(gaps)} | Courses: {len(recommendations)}"
    )

    return {
        "gaps":            gaps,
        "recommendations": recommendations,
        "costs":           costs,
        "deadlines":       deadlines
    }


if __name__ == "__main__":
    from agents.agent1_profile_matching import run_agent1
    test_student = {
        "name":             "Alina",
        "degree":           "BBA Finance",
        "major":            "Finance",
        "university":       "Kathmandu University",
        "country":          "Nepal",
        "gpa":              3.7,
        "ielts_score":      6.5,
        "ects_business":    90,
        "ects_quant":       30,
        "ects_programming": 0,
        "ects_research":    15,
        "target_field":     "Business Data Science",
        "eu_student":       False
    }
    result1 = run_agent1(test_student)
    result2 = run_agent2(result1)
    print("\n✅ Agent 2 complete")