#test 1
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

#test 2
from pathlib import Path
import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "model.joblib"


def test_model_loads():
    model = joblib.load(MODEL_PATH)

    assert model is not None
    assert hasattr(model, "predict_proba")

# Test 3: Invalid input is rejected
def test_invalid_input():
    response = client.post(
        "/predict",
        json={
            "tenure_months": "banana",
            "monthly_charges": 95.0,
            "contract": "Month-to-month",
            "internet_service": "Fiber optic",
            "support_calls": 5,
        },
    )

    assert response.status_code == 422


# Test 4: Zero tenure is accepted
def test_zero_tenure():
    response = client.post(
        "/predict",
        json={
            "tenure_months": 0,
            "monthly_charges": 95.0,
            "contract": "Month-to-month",
            "internet_service": "Fiber optic",
            "support_calls": 5,
        },
    )

    assert response.status_code == 200
    assert "churn_probability" in response.json()  
# Test 5: Same input produces the same prediction
def test_deterministic_prediction():
    customer = {
        "tenure_months": 4,
        "monthly_charges": 95.0,
        "contract": "Month-to-month",
        "internet_service": "Fiber optic",
        "support_calls": 5,
    }

    response1 = client.post("/predict", json=customer)
    response2 = client.post("/predict", json=customer)

    assert response1.status_code == 200
    assert response2.status_code == 200

    assert (
        response1.json()["churn_probability"]
        == response2.json()["churn_probability"]
    )  