from pathlib import Path

from catboost import CatBoostClassifier
from imblearn.over_sampling import SMOTE
import joblib
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

DATA_PATH = Path("data/processed/processed_railway.csv")
MODEL_PATH = Path("models/catboost_railway_model.joblib")
TARGET_COL = "label__Refund Request"
THRESHOLD = 0.35
RANDOM_STATE = 42


def main():
    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    imputer = SimpleImputer(strategy="median")
    X_train_clean = pd.DataFrame(
        imputer.fit_transform(X_train),
        columns=X_train.columns,
        index=X_train.index,
    )

    smote = SMOTE(sampling_strategy=0.3, random_state=RANDOM_STATE)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train_clean, y_train)

    best_model = Pipeline([
        (
            "clf",
            CatBoostClassifier(
                depth=10,
                iterations=200,
                l2_leaf_reg=1,
                learning_rate=0.05,
                random_state=RANDOM_STATE,
                verbose=0,
                thread_count=-1,
            ),
        ),
    ])
    best_model.fit(X_train_resampled, y_train_resampled)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    artifact = {
        "model": best_model,
        "imputer": imputer,
        "threshold": THRESHOLD,
        "features": list(X.columns),
    }
    joblib.dump(artifact, MODEL_PATH)
    print(f"Saved model artifact to: {MODEL_PATH}")


if __name__ == "__main__":
    main()