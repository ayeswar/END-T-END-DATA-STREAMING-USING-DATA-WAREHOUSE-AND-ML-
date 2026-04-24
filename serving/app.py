from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc
import redis
import json

app = FastAPI(title="Fraud Detection Inference API")

# Setup Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

# Load Model from MLflow
# Note: In production, you'd pull by tag 'Production'
MODEL_URI = "models:/Fraud_Detection_Model/Production"
try:
    model = mlflow.pyfunc.load_model(MODEL_URI)
except Exception as e:
    print(f"Warning: Could not load model from MLflow ({e}). Using dummy model.")
    model = None

class Transaction(BaseModel):
    user_id: str
    amount: float
    location: str

@app.post("/predict")
async def predict(tx: Transaction):
    # 1. Fetch real-time feature from Redis
    avg_amount_key = f"user:{tx.user_id}:avg_amount_10m"
    avg_amount_10m = r.get(avg_amount_key)
    
    if avg_amount_10m is None:
        avg_amount_10m = tx.amount # Fallback if no history
    else:
        avg_amount_10m = float(avg_amount_10m)

    # 2. Inference
    if model:
        # Prepare input for XGBoost
        features = [[tx.amount, avg_amount_10m]]
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]
    else:
        # Dummy logic for demo
        probability = 0.99 if tx.amount > 4500 else 0.05
        prediction = 1 if probability > 0.5 else 0

    return {
        "user_id": tx.user_id,
        "is_fraud": int(prediction),
        "fraud_probability": float(probability),
        "features_used": {
            "amount": tx.amount,
            "avg_amount_10m": avg_amount_10m
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
