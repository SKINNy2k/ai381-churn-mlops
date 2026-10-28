
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# Find the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "churn_v2.csv"
MODEL_PATH = PROJECT_ROOT / "model.joblib"

# Define the input features
NUMERIC_FEATURES = [
    "tenure_months",
    "monthly_charges",
    "support_calls",
]

CATEGORICAL_FEATURES = [
    "contract",
    "internet_service",
]


def train_model():
    # 1. Load the dataset
    df = pd.read_csv(DATA_PATH)

    # Keep the feature name consistent with the API
    df = df.rename(columns={"monthly_fee": "monthly_charges"})

    # 2. Separate features (X) and target (y)
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df["churn"]

    # 3. Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # 4. Build the preprocessing and classification pipeline
    model = Pipeline([
        (
            "prep",
            ColumnTransformer([
                (
                    "num",
                    StandardScaler(),
                    NUMERIC_FEATURES,
                ),
                (
                    "cat",
                    OneHotEncoder(handle_unknown="ignore"),
                    CATEGORICAL_FEATURES,
                ),
            ]),
        ),
        (
            "clf",
            LogisticRegression(max_iter=1000),
        ),
    ])

    # 5. Train the model
    model.fit(X_train, y_train)

    # 6. Evaluate on the test set
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = probabilities > 0.5

    print("F1 :", round(f1_score(y_test, predictions), 3))
    print("AUC:", round(roc_auc_score(y_test, probabilities), 3))

    # 7. Save the complete fitted pipeline
    joblib.dump(model, MODEL_PATH)
    print(f"Saved model to: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()
