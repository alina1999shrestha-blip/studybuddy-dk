import mlflow
import json
import os
from datetime import datetime

# Set MLflow tracking location — saves inside your project folder
MLFLOW_DIR = os.path.join(os.getcwd(), "mlflow_tracking")
mlflow.set_tracking_uri(f"file:///{MLFLOW_DIR}")
mlflow.set_experiment("studybuddy_dk")


def log_pipeline_run_mlflow(student_input: dict, results: dict):
    """
    Logs a complete pipeline run to MLflow.
    Saves parameters, metrics and artifacts.
    """
    with mlflow.start_run(run_name=f"pipeline_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"):

        # ── Parameters (inputs) ───────────────────────────────────────
        mlflow.log_param("student_name",        student_input.get("name"))
        mlflow.log_param("degree",              student_input.get("degree"))
        mlflow.log_param("country",             student_input.get("country"))
        mlflow.log_param("ielts_score",         student_input.get("ielts_score"))
        mlflow.log_param("ects_total",          results["profile"]["ects_total"])
        mlflow.log_param("ects_business",       student_input.get("ects_business"))
        mlflow.log_param("ects_quant",          student_input.get("ects_quant"))
        mlflow.log_param("ects_programming",    student_input.get("ects_programming"))
        mlflow.log_param("eu_student",          student_input.get("eu_student"))
        mlflow.log_param("target_field",        student_input.get("target_field"))

        # ── Metrics (outputs) ─────────────────────────────────────────
        top = results["top3_matches"][0]
        mlflow.log_metric("top_match_score",    top["match_score"])
        mlflow.log_metric("total_gaps",         len(results["gaps"]))
        mlflow.log_metric("courses_recommended",len(results["recommendations"]))
        mlflow.log_metric("tuition_dkk",        results["costs"].get("tuition_dkk", 0))
        mlflow.log_metric("tuition_npr",        results["costs"].get("tuition_npr", 0))
        mlflow.log_metric("tuition_inr",        results["costs"].get("tuition_inr", 0))
        mlflow.log_metric("days_until_deadline",
            results["deadlines"][0]["days_left"] if results["deadlines"] else 0)
        mlflow.log_metric("monitoring_alerts",
            len(results["monitoring"]["alerts"]))
        mlflow.log_metric("pipeline_duration_s",results["run_duration_s"])

        # ── Tags ──────────────────────────────────────────────────────
        mlflow.set_tag("top_program",   top["program_name"])
        mlflow.set_tag("university",    top["university"])
        mlflow.set_tag("run_date",      datetime.utcnow().strftime("%Y-%m-%d"))
        mlflow.set_tag("pipeline_version", "1.0")

        # ── Artifacts (save full results as JSON files) ───────────────
        os.makedirs("mlflow_artifacts", exist_ok=True)

        # Save student profile
        with open("mlflow_artifacts/student_profile.json", "w") as f:
            json.dump(results["profile"], f, indent=2)
        mlflow.log_artifact("mlflow_artifacts/student_profile.json")

        # Save top 3 matches
        with open("mlflow_artifacts/program_matches.json", "w") as f:
            json.dump(results["top3_matches"], f, indent=2)
        mlflow.log_artifact("mlflow_artifacts/program_matches.json")

        # Save gaps and recommendations
        with open("mlflow_artifacts/gaps_and_courses.json", "w") as f:
            json.dump({
                "gaps": results["gaps"],
                "recommendations": [
                    {
                        "gap": r["gap"],
                        "courses": r["courses"]
                    }
                    for r in results["recommendations"]
                ]
            }, f, indent=2)
        mlflow.log_artifact("mlflow_artifacts/gaps_and_courses.json")

        # Save costs
        with open("mlflow_artifacts/costs.json", "w") as f:
            json.dump(results["costs"], f, indent=2)
        mlflow.log_artifact("mlflow_artifacts/costs.json")

        # Save monitoring alerts
        with open("mlflow_artifacts/monitoring_alerts.json", "w") as f:
            json.dump(results["monitoring"]["alerts"], f, indent=2)
        mlflow.log_artifact("mlflow_artifacts/monitoring_alerts.json")

        print(f"\n✅ MLflow run logged successfully")
        print(f"   Experiment: studybuddy_dk")
        print(f"   Top match:  {top['program_name']} ({top['match_score']}%)")
        print(f"   Gaps:       {len(results['gaps'])}")
        print(f"   Artifacts:  5 files saved")
        print(f"   View UI:    mlflow ui --backend-store-uri mlflow_tracking")


def log_monitoring_run_mlflow(monitoring_result: dict):
    """Log a standalone monitoring run to MLflow."""
    with mlflow.start_run(run_name=f"monitoring_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"):
        alerts = monitoring_result.get("alerts", [])
        high   = monitoring_result.get("high_alerts", [])

        mlflow.log_metric("total_alerts",      len(alerts))
        mlflow.log_metric("high_alerts",       len(high))
        mlflow.log_metric("rates_updated",     int(monitoring_result.get("rates_updated", False)))
        mlflow.set_tag("run_type",  "monitoring")
        mlflow.set_tag("run_date",  datetime.utcnow().strftime("%Y-%m-%d"))
        mlflow.set_tag("status",    "alerts_found" if high else "clean")

        os.makedirs("mlflow_artifacts", exist_ok=True)
        with open("mlflow_artifacts/monitoring_run.json", "w") as f:
            json.dump(alerts, f, indent=2)
        mlflow.log_artifact("mlflow_artifacts/monitoring_run.json")

        print(f"✅ Monitoring run logged to MLflow")