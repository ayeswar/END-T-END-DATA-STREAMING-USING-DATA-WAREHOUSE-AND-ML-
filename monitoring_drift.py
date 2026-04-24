import pandas as pd
from sqlalchemy import create_engine
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
import time

# DB Connection
DB_URL = "postgresql://admin:password@localhost:5432/warehouse"
engine = create_engine(DB_URL)

def check_drift():
    # 1. Load Reference Data (Training period)
    ref_query = "SELECT amount, avg_amount_10m, is_fraud FROM transactions_processed WHERE timestamp < '2023-10-01'"
    ref_df = pd.read_sql(ref_query, engine)

    # 2. Load Current Data (Serving period)
    curr_query = "SELECT amount, avg_amount_10m, is_fraud FROM transactions_processed WHERE timestamp >= '2023-10-01'"
    curr_df = pd.read_sql(curr_query, engine)

    if ref_df.empty or curr_df.empty:
        print("Not enough data to check for drift.")
        return

    # 3. Generate Evidently Report
    report = Report(metrics=[
        DataDriftPreset(),
        TargetDriftPreset()
    ])

    report.run(reference_data=ref_df, current_data=curr_df)
    
    # 4. Save report
    report.save_html("data_drift_report.html")
    print("Drift report generated: data_drift_report.html")

    # 5. Simple Alert Logic
    drift_share = report.as_dict()['metrics'][0]['result']['drift_share']
    if drift_share > 0.5:
        print("⚠️ HIGH DRIFT DETECTED! Triggering retraining DAG...")
        # In production: requests.post("http://airflow:8080/api/v1/dags/model_retraining_pipeline/dagRuns")

if __name__ == "__main__":
    check_drift()
