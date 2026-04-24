import pandas as pd
import xgboost as xgb
import mlflow
import mlflow.xgboost
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

# DB Connection
DB_URL = "postgresql://admin:password@localhost:5432/warehouse"
engine = create_engine(DB_URL)

def train_model():
    # 1. Fetch Data from Warehouse
    query = "SELECT * FROM transactions_processed LIMIT 10000"
    df = pd.read_sql(query, engine)
    
    if df.empty:
        print("No data in warehouse yet. Skipping training.")
        return

    # 2. Preprocessing
    X = df[['amount', 'avg_amount_10m']] # Simplified features
    y = df['is_fraud']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. MLflow Tracking
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("Fraud_Detection")

    with mlflow.start_run():
        model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
        model.fit(X_train, y_train)

        # 4. Evaluation
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds)
        rec = recall_score(y_test, preds)

        # 5. Log to MLflow
        mlflow.log_params({"max_depth": 3, "n_estimators": 100})
        mlflow.log_metrics({"accuracy": acc, "precision": prec, "recall": rec})
        mlflow.xgboost.log_model(model, "model")
        
        print(f"Model trained. Accuracy: {acc:.4f}, Precision: {prec:.4f}")

if __name__ == "__main__":
    train_model()
