import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder


class RailwayFullPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, midnight_rollover_threshold_hours: float = -12.0):
        self.midnight_rollover_threshold_hours = midnight_rollover_threshold_hours

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()

        if {"Journey Status", "Actual Arrival Time", "Arrival Time"}.issubset(df.columns):
            same_arrival = df["Arrival Time"] == df["Actual Arrival Time"]
            df.loc[same_arrival & df["Journey Status"].isin(["Delayed", "Cancelled"]), "Journey Status"] = "On Time"
            df.loc[(~same_arrival) & (df["Journey Status"] == "On Time"), "Journey Status"] = "Delayed"

        if "Journey Datetime" in df.columns:
            df["Journey Datetime"] = pd.to_datetime(df["Journey Datetime"], errors="coerce", format="mixed")
            df["Is Weekend"] = df["Journey Datetime"].dt.dayofweek >= 5
            df["Is Night Departure"] = df["Journey Datetime"].dt.hour.isin([0, 1, 2, 3, 4, 5])

        if "Purchase Datetime" in df.columns:
            df["Purchase Datetime"] = pd.to_datetime(df["Purchase Datetime"], errors="coerce", format="mixed")

        if {"Journey Datetime", "Purchase Datetime"}.issubset(df.columns):
            lead_hours = (df["Journey Datetime"] - df["Purchase Datetime"]).dt.total_seconds() / 3600.0
            df["Lead Hours"] = np.log1p(np.clip(lead_hours, a_min=0.0, a_max=None))

        raw_delay_minutes = None
        if {"Arrival Time", "Actual Arrival Time"}.issubset(df.columns):
            sched_dt = pd.to_datetime(df["Arrival Time"], errors="coerce", format="mixed")
            actual_dt = pd.to_datetime(df["Actual Arrival Time"], errors="coerce", format="mixed")
            delay_hours = (actual_dt - sched_dt).dt.total_seconds() / 3600.0

            crossed_midnight = delay_hours < self.midnight_rollover_threshold_hours
            delay_hours = delay_hours.where(~crossed_midnight, delay_hours + 24.0)

            raw_delay_minutes = delay_hours * 60.0
            df["Delay Minutes"] = np.sqrt(np.clip(raw_delay_minutes, a_min=0.0, a_max=None))

        if {"Journey Datetime", "Arrival Time"}.issubset(df.columns) and raw_delay_minutes is not None:
            arrival_str = df["Journey Datetime"].dt.date.astype(str) + " " + df["Arrival Time"].astype(str)
            arrival_datetime = pd.to_datetime(arrival_str, errors="coerce", format="mixed")
            df["Duration Minutes"] = (
                (arrival_datetime + pd.to_timedelta(raw_delay_minutes, unit="m")) - df["Journey Datetime"]
            ).dt.total_seconds() / 60.0

        if "Price" in df.columns:
            price = pd.to_numeric(df["Price"], errors="coerce")
            df["Price"] = np.log1p(np.clip(price, a_min=0.0, a_max=None))

        return df


def build_preprocessor_pipeline():
    label_features = ["Departure Station", "Arrival Destination"]
    ohe_features = [
        "Purchase Type",
        "Payment Method",
        "Railcard",
        "Ticket Type",
        "Reason for Delay",
        "Journey Status",
    ]

    column_transformer = ColumnTransformer(
        transformers=[
            ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ohe_features),
            ("label", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), label_features),
        ],
        remainder="passthrough",
    )

    return Pipeline(
        steps=[
            ("feature_engineer", RailwayFullPreprocessor()),
            ("preprocessor", column_transformer),
        ]
    )


def preprocess_data(df):
    pipeline = build_preprocessor_pipeline()
    processed_array = pipeline.fit_transform(df)
    return processed_array, pipeline


if __name__ == "__main__":
    raw_df = pd.read_csv("data/cleaned/cleaned_railway.csv")
    processed_array, pipeline = preprocess_data(raw_df)
    joblib.dump(pipeline, "models/preprocessor.joblib")

    all_column_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
    processed_df = pd.DataFrame(processed_array, columns=all_column_names)
    processed_df.to_csv("data/processed/processed_railway.csv", index=False)