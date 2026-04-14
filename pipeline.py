from typing_extensions import final

from agents.agent1_profile_matching import run_agent1
from agents.agent2_gap_preparation import run_agent2
from agents.agent3_monitoring import run_agent3
from database import log_pipeline_run
from datetime import datetime

def run_pipeline(student_input: dict) -> dict:
    """
    Full StudyBuddy DK pipeline.
    Runs all 3 agents in sequence and returns complete results.
    """
    print("\n" + "=" * 55)
    print("  STUDYBUDDY DK — FULL PIPELINE RUNNING")
    print("=" * 55)
    start = datetime.utcnow()

    # Agent 1 — profile + matching + eligibility
    result1 = run_agent1(student_input)

    # Agent 2 — gaps + preparation + costs + deadlines
    result2 = run_agent2(result1)

    # Agent 3 — monitoring
    result3 = run_agent3()

    # Combine all results
    duration = (datetime.utcnow() - start).seconds
    final = {
        "student_name":    result1["profile"]["name"],
        "profile":         result1["profile"],
        "top3_matches":    result1["top3"],
        "all_matches":     result1["matches"],
        "gaps":            result2["gaps"],
        "recommendations": result2["recommendations"],
        "costs":           result2["costs"],
        "deadlines":       result2["deadlines"],
        "monitoring":      result3,
        "run_duration_s":  duration
    }

    log_pipeline_run(
        "full_pipeline",
        "success",
        f"Student: {final['student_name']} | "
        f"Top match: {result1['top3'][0]['program_name']} | "
        f"Gaps: {len(result2['gaps'])} | "
        f"Duration: {duration}s"
    )

    from mlflow_tracker import log_pipeline_run_mlflow
    log_pipeline_run_mlflow(student_input, final)

    print("\n" + "=" * 55)
    print(f"  ✅ PIPELINE COMPLETE in {duration}s")
    print("=" * 55)
    return final


if __name__ == "__main__":
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

    result = run_pipeline(test_student)

    print("\n📊 FINAL SUMMARY")
    print(f"Student:      {result['student_name']}")
    print(f"Top match:    {result['top3_matches'][0]['program_name']} "
          f"({result['top3_matches'][0]['match_score']}%)")
    print(f"Gaps found:   {len(result['gaps'])}")
    print(f"Courses rec:  {len(result['recommendations'])}")
    print(f"Cost:         {result['costs'].get('tuition_dkk', 0):,} DKK/year")
    if result['costs'].get('tuition_npr'):
        print(f"              = {result['costs']['tuition_npr']:,} NPR/year")