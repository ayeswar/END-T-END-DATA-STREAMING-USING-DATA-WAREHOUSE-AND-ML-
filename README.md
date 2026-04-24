# 🛡️ FraudGuard: Production Real-Time Data Warehouse + ML System

A production-grade, 100% free, self-hosted MLOps platform for real-time fraud detection. Built with the Modern Data Stack.

## 🏗️ Architecture

- **Messaging**: Apache Kafka (Event Ingestion)
- **Stream Processing**: Apache Spark (Feature Engineering)
- **Warehouse**: PostgreSQL (Analytical Storage)
- **Feature Store**: Redis (Real-time Serving)
- **ML Lifecycle**: MLflow (Tracking & Registry)
- **Orchestration**: Apache Airflow (Automated Retraining)
- **Serving**: FastAPI (Low-latency Inference)
- **Monitoring**: Evidently AI (Drift Detection)
- **Dashboard**: Streamlit (Real-time Monitoring UI)

## 🚀 Quick Start

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.9+

### 2. Launch Infrastructure
```bash
docker-compose up -d --build
```
This starts Kafka, Postgres, Redis, MLflow, Airflow, the Serving API, and the Streamlit Dashboard.

### 3. Setup Virtual Environment (Local)
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 4. Start the Data Flow
1.  **Start Spark Streaming**:
    ```bash
    python processing/spark_streaming.py
    ```
2.  **Start Data Ingestion (Producer)**:
    ```bash
    python ingestion/producer.py
    ```

### 5. Access the Dashboards
- **Monitoring UI (Streamlit)**: `http://localhost:8501`
- **Inference API (FastAPI)**: `http://localhost:8000/docs`
- **MLflow Tracking**: `http://localhost:5000`
- **Airflow Orchestrator**: `http://localhost:8082`

## 🧠 ML Workflow

1.  **Ingestion**: Real-time transactions are pushed to Kafka.
2.  **Streaming ETL**: Spark calculates rolling aggregates and updates Redis/Postgres.
3.  **Retraining**: Airflow triggers `training/train.py` weekly to update the model.
4.  **Drift Check**: `monitoring_drift.py` generates a report and alerts if data distribution shifts.

## 🌐 Scalability & Optimization
- **Scale Out**: Use Kubernetes for horizontal scaling of FastAPI and Spark workers.
- **Latency**: Redis ensures sub-millisecond feature retrieval for inference.
- **Reliability**: Kafka provides persistent buffers to handle traffic spikes.

---
Built with ❤️ by a Senior Data & ML Architect.
