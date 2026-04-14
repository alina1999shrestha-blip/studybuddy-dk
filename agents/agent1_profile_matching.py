import json
from database import get_all_programs, log_pipeline_run
from datetime import datetime, date

def build_student_profile(student_input: dict) -> dict:
    """
    Agent 1 - Step 1: Build structured student profile from raw input.
    """
    profile = {
        "name":             student_input.get("name", "Student"),
        "degree":           student_input.get("degree", ""),
        "major":            student_input.get("major", ""),
        "university":       student_input.get("university", ""),
        "country":          student_input.get("country", ""),
        "gpa":              float(student_input.get("gpa", 0)),
        "ielts_score":      float(student_input.get("ielts_score", 0)),
        "ects_business":    float(student_input.get("ects_business", 0)),
        "ects_quant":       float(student_input.get("ects_quant", 0)),
        "ects_programming": float(student_input.get("ects_programming", 0)),
        "ects_research":    float(student_input.get("ects_research", 0)),
        "target_field":     student_input.get("target_field", ""),
        "eu_student":       student_input.get("eu_student", False),
    }
    profile["ects_total"] = (
        profile["ects_business"] +
        profile["ects_quant"] +
        profile["ects_programming"] +
        profile["ects_research"]
    )
    return profile


def calculate_match_score(profile: dict, program: dict) -> float:
    """
    Agent 1 - Step 2: Calculate match score using cosine similarity approach.
    Compares student ECTS breakdown against program requirements.
    Returns a score between 0 and 100.
    """
    score = 0
    total_weight = 0

    # ECTS total check — weight 30
    ects_required = program.get("ects_required") or 180
    ects_score = min(profile["ects_total"] / ects_required, 1.0) * 30
    score += ects_score
    total_weight += 30

    # Business ECTS match — weight 20
    biz_req = program.get("ects_business_min") or 0
    if biz_req > 0:
        biz_score = min(profile["ects_business"] / biz_req, 1.0) * 20
        score += biz_score
    else:
        score += 20
    total_weight += 20

    # Quantitative ECTS match — weight 20
    quant_req = program.get("ects_quantitative_min") or 0
    if quant_req > 0:
        quant_score = min(profile["ects_quant"] / quant_req, 1.0) * 20
        score += quant_score
    else:
        score += 20
    total_weight += 20

    # Programming ECTS match — weight 20
    prog_req = program.get("ects_programming_min") or 0
    if prog_req > 0:
        prog_score = min(profile["ects_programming"] / prog_req, 1.0) * 20
        score += prog_score
    else:
        score += 20
    total_weight += 20

    # IELTS check — weight 10
    ielts_min = program.get("ielts_min") or 0
    if ielts_min > 0 and profile["ielts_score"] > 0:
        if profile["ielts_score"] >= ielts_min:
            score += 10
    else:
        score += 10
    total_weight += 10

    return round((score / total_weight) * 100, 1)


def check_eligibility(profile: dict, program: dict) -> dict:
    """
    Agent 1 - Step 3: Check if student meets eligibility requirements.
    """
    issues = []
    passed = []

    # ECTS total
    ects_req = program.get("ects_required") or 180
    if profile["ects_total"] >= ects_req:
        passed.append(f"ECTS total: {profile['ects_total']} / {ects_req} ✅")
    else:
        issues.append(f"ECTS total: {profile['ects_total']} / {ects_req} — missing {ects_req - profile['ects_total']} ECTS")

    # IELTS
    ielts_min = program.get("ielts_min") or 0
    if ielts_min > 0:
        if profile["ielts_score"] >= ielts_min:
            passed.append(f"IELTS: {profile['ielts_score']} / {ielts_min} ✅")
        else:
            issues.append(f"IELTS: {profile['ielts_score']} — minimum required is {ielts_min}")

    # Programming requirement
    prog_req = program.get("ects_programming_min") or 0
    if prog_req > 0 and profile["ects_programming"] < prog_req:
        issues.append(f"Programming ECTS: {profile['ects_programming']} / {prog_req} — missing {prog_req - profile['ects_programming']} ECTS")

    # Deadline
    deadline_str = program.get("deadline_non_eu_september") or program.get("deadline_september")
    days_left = None
    if deadline_str:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        days_left = (deadline - date.today()).days

    return {
        "eligible": len(issues) == 0,
        "passed": passed,
        "issues": issues,
        "days_until_deadline": days_left,
        "deadline": deadline_str
    }


def run_agent1(student_input: dict) -> dict:
    """
    Main Agent 1 function.
    Input:  raw student input dictionary
    Output: profile + top matched programs + eligibility results
    """
    print("\n🤖 Agent 1 — Profile + Matching + Eligibility")
    print("-" * 45)

    # Step 1 — build profile
    profile = build_student_profile(student_input)
    print(f"✅ Profile built for {profile['name']}")
    print(f"   Degree: {profile['degree']} | ECTS total: {profile['ects_total']}")
    print(f"   IELTS: {profile['ielts_score']} | Country: {profile['country']}")

    # Step 2 — load programs and calculate match scores
    programs = get_all_programs()
    scored = []
    for p in programs:
        score = calculate_match_score(profile, p)
        eligibility = check_eligibility(profile, p)
        scored.append({
            "program_id":       p["id"],
            "program_name":     p["name"],
            "university":       p["university"],
            "university_full":  p["university_full"],
            "match_score":      score,
            "eligibility":      eligibility,
            "tuition_dkk":      p["tuition_non_eu_dkk"] if not profile["eu_student"] else p["tuition_eu_dkk"],
            "deadline":         p.get("deadline_non_eu_september") or p.get("deadline_september"),
            "location":         p["location"],
            "ielts_min":        p["ielts_min"],
            "ects_required":    p["ects_required"],
        })

    # Sort by match score
    scored.sort(key=lambda x: x["match_score"], reverse=True)
    top3 = scored[:3]

    print(f"\n✅ Top 3 program matches:")
    for i, p in enumerate(top3, 1):
        status = "✅ Eligible" if p["eligibility"]["eligible"] else "⚠️ Gaps found"
        print(f"   {i}. {p['program_name']} — {p['university']} ({p['match_score']}%) {status}")

    # Log to database
    log_pipeline_run(
        "agent1_profile_matching",
        "success",
        f"Student: {profile['name']} | Top match: {top3[0]['program_name']} ({top3[0]['match_score']}%)"
    )

    return {
        "profile":  profile,
        "matches":  scored,
        "top3":     top3
    }


if __name__ == "__main__":
    # Test with a sample student
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

    result = run_agent1(test_student)
    print("\n✅ Agent 1 complete")