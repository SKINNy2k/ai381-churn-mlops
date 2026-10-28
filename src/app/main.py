"""Lab 1 FastAPI skeleton: serves the model you saved from the notebook.

Run it by hand (this is Round 1 of the race):
    uvicorn app.main:app --port 8000
Then send predictions with curl (see sample_request.json).
"""
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel


class Customer(BaseModel):
    tenure_months: int
    monthly_charges: float
    contract: str
    internet_service: str
    support_calls: int


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "model.joblib"
FEATURES = ["tenure_months", "monthly_charges", "contract", "internet_service", "support_calls"]


app = FastAPI(title="AI381 Lab 1 churn API")
model = joblib.load(MODEL_PATH)


@app.get("/health")
def health():
    return {"status": "ok"}



@app.post("/predict")
def predict(customer: Customer):
    customer_data = customer.model_dump()

    X = pd.DataFrame([customer_data])[FEATURES]
    p = float(model.predict_proba(X)[0, 1])

    return {"churn_probability": round(p, 3)}





