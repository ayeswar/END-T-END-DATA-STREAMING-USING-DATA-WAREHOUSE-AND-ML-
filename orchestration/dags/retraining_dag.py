from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add training path to sys.path
sys.path.append('/opt/airflow/training')

def trigger_retraining():
    # In a real setup, this would be a separate microservice call 
    # or a containerized job. Here we call the script directly.
    from train import train_model
    train_model()

default_args = {
    'owner': 'data_science',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'model_retraining_pipeline',
    default_args=default_args,
    description='Retrains the Fraud Detection model weekly',
    schedule_interval=timedelta(days=7),
    catchup=False,
) as dag:

    retrain_task = PythonOperator(
        task_id='retrain_fraud_model',
        python_callable=trigger_retraining,
    )

    retrain_task
