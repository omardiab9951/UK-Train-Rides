from datetime import datetime, time, timedelta
from pathlib import Path

import joblib
import pandas as pd
import numpy as np
import streamlit as st
import traceback


from src import preprocessor
from src.preprocessor import build_preprocessor_pipeline

MODEL_PATH = Path("models/catboost_railway_model.joblib")
CLEANED_DATA_PATH = Path("data/cleaned/cleaned_railway.csv")

st.set_page_config(page_title="Railway Refund Predictor", page_icon="🚆", layout="wide")

st.markdown("""
    <style>
    .stSelectbox, .stNumberInput, .stRadio {
        transition: all 0.3s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚆 Railway Ticket Refund Prediction System", anchor=False)
st.markdown(
    "A smooth interactive interface to input journey details and predict the likelihood of a **Refund Request**."
)
st.divider()


@st.cache_resource
def load_model_and_preprocessor(model_path: Path, cleaned_path: Path):
    artifact = joblib.load(model_path)
    if isinstance(artifact, dict):
        model = artifact["model"]
        threshold = float(artifact.get("threshold", 0.35))
        expected_features = artifact.get("features", [])
    else:
        model = artifact
        threshold = 0.35
        expected_features = []

    processor = build_preprocessor_pipeline()
    if cleaned_path.exists():
        ref_df = pd.read_csv(cleaned_path)
        processor.fit(ref_df)

    return model, processor, threshold, expected_features


try:
    model, processor, threshold, expected_features = load_model_and_preprocessor(
        MODEL_PATH, CLEANED_DATA_PATH
    )
except Exception as e:
    st.error(f"Failed to load model or initialize preprocessor: {e}")
    st.stop()


def build_raw_input(
    purchase_dt: datetime,
    journey_dt: datetime,
    expected_arrival_t: time,
    actual_arrival_dt: datetime,
    purchase_type: str,
    payment_method: str,
    ticket_type: str,
    price: float,
    railcard: str,
    departure_station: str,
    arrival_destination: str,
    journey_status: str,
    reason_for_delay: str,
) -> pd.DataFrame:
    return pd.DataFrame([{
        "Purchase Type": purchase_type,
        "Payment Method": payment_method,
        "Railcard": railcard,
        "Ticket Type": ticket_type,
        "Price": float(price),
        "Departure Station": departure_station,
        "Arrival Destination": arrival_destination,
        "Arrival Time": expected_arrival_t.strftime("%H:%M:%S"),
        "Actual Arrival Time": actual_arrival_dt.strftime("%H:%M:%S"),
        "Journey Status": journey_status,
        "Reason for Delay": reason_for_delay,
        "Refund Request": 0,
        "Purchase Datetime": purchase_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "Journey Datetime": journey_dt.strftime("%Y-%m-%d %H:%M:%S"),
    }])

def transform_for_model(
    raw_df: pd.DataFrame, proc, feature_cols: list[str]
) -> pd.DataFrame:
    transformed = proc.transform(raw_df)

    if hasattr(proc, "named_steps") and "preprocessor" in proc.named_steps:
        col_names = list(proc.named_steps["preprocessor"].get_feature_names_out())
    elif hasattr(proc, "get_feature_names_out"):
        col_names = list(proc.get_feature_names_out())
    else:
        col_names = [f"col_{i}" for i in range(transformed.shape[1])]

    X_proc = pd.DataFrame(transformed, columns=col_names)

    if "label__Refund Request" in X_proc.columns:
        X_proc = X_proc.drop(columns=["label__Refund Request"])

    if feature_cols:
        missing_cols = [col for col in feature_cols if col not in X_proc.columns]
        if missing_cols:
            missing_df = pd.DataFrame(0.0, index=X_proc.index, columns=missing_cols)
            X_proc = pd.concat([X_proc, missing_df], axis=1)

        X_proc = X_proc[feature_cols]

    for col in X_proc.columns:
        X_proc[col] = pd.to_numeric(X_proc[col], errors="coerce").astype(np.float64)

    return X_proc

st.subheader("Ticket & Route Details", anchor=False)

r1_col1, r1_col2, r1_col3, r1_col4 = st.columns(4)
with r1_col1:
    purchase_type = st.selectbox("Purchase Type", ["Online", "Station"])
with r1_col2:
    payment_method = st.selectbox("Payment Method", ["Contactless", "Credit Card", "Debit Card"])
with r1_col3:
    ticket_type = st.selectbox("Ticket Type", ["Advance", "Off-Peak", "Anytime"])
with r1_col4:
    price = st.number_input("Price (£)", min_value=1, value=25, step=1)

rc_col1, rc_col2, _ = st.columns([1, 1.5, 1.5])
with rc_col1:
    has_railcard = st.radio("Railcard?", ["No", "Yes"], horizontal=True)
with rc_col2:
    if has_railcard == "Yes":
        railcard = st.selectbox("Railcard Type", ["Adult", "Senior", "Disabled"])
    else:
        st.selectbox("Railcard Type", ["No Railcard"], disabled=True)
        railcard = "No Railcard"

st_col1, st_col2 = st.columns(2)
ALL_STATIONS = [
    "Birmingham New Street",
    "Bristol Temple Meads",
    "Cardiff Central",
    "Coventry",
    "Crewe",
    "Didcot",
    "Doncaster",
    "Durham",
    "Edinburgh Waverley",
    "Leeds",
    "Leicester",
    "Liverpool Lime Street",
    "London Euston",
    "London Kings Cross",
    "London Paddington",
    "London St Pancras",
    "London Waterloo",
    "Manchester Piccadilly",
    "Nottingham",
    "Nuneaton",
    "Oxford",
    "Peterborough",
    "Reading",
    "Sheffield",
    "Stafford",
    "Swindon",
    "Tamworth",
    "Wakefield",
    "Warrington",
    "Wolverhampton",
    "York"
]

with st_col1:
    departure_station = st.selectbox("Departure Station", ALL_STATIONS, index=0)
with st_col2:
    arrival_options = [s for s in ALL_STATIONS if s != departure_station]
    arrival_destination = st.selectbox("Arrival Destination", arrival_options, index=0)

st.divider()

st.subheader("Purchase & Journey Timings", anchor=False)

t_col1, t_col2, t_col3, t_col4, t_col5 = st.columns(5)
with t_col1:
    purchase_date = st.date_input("Purchase Date", value=datetime(2024, 4, 15))
with t_col2:
    purchase_time = st.time_input("Purchase Time", value=time(10, 30))
with t_col3:
    journey_date = st.date_input("Journey Date", value=datetime(2024, 4, 20))
with t_col4:
    departure_time = st.time_input("Departure Time", value=time(14, 0))
with t_col5:
    expected_arrival_time = st.time_input("Expected Arrival", value=time(16, 15))

purchase_datetime = datetime.combine(purchase_date, purchase_time)
journey_datetime = datetime.combine(journey_date, departure_time)


st.divider()

st.subheader("Journey Status & Delays", anchor=False)

delay_reasons_list = [
    "Signal Failure", "Technical Issue", "Weather Conditions",
    "Staff Shortage", "Traffic"
]

s_col1, s_col2, s_col3 = st.columns([1, 1.5, 1.5])

with s_col1:
    is_cancelled_input = st.radio("Cancelled?", ["No", "Yes"], horizontal=True)

expected_arrival_dt = datetime.combine(journey_date, expected_arrival_time)
if expected_arrival_dt < journey_datetime:
    expected_arrival_dt += timedelta(days=1)

if is_cancelled_input == "Yes":
    journey_status = "Cancelled"
    actual_arrival_dt = expected_arrival_dt
    reason_for_delay = st.selectbox("Reason for Cancellation", delay_reasons_list)

    with s_col2:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        st.info(f"Reason: **{reason_for_delay}**")

    with s_col3:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        st.error("🚫 **Status:** Cancelled")

else:
    with s_col2:
        sub_c1, sub_c2 = st.columns([1, 1.3])
        with sub_c1:
            delay_minutes = st.number_input("Delay (Mins)", min_value=0, value=0, step=5)
        with sub_c2:
            if delay_minutes > 0:
                reason_for_delay = st.selectbox("Reason for Delay", delay_reasons_list)
            else:
                st.selectbox("Reason for Delay", ["No Delay"], disabled=True)
                reason_for_delay = "No Delay"

    actual_arrival_dt = expected_arrival_dt + timedelta(minutes=int(delay_minutes))
    actual_arrival_display = actual_arrival_dt.strftime("%H:%M:%S")

    with s_col3:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if delay_minutes > 0:
            journey_status = "Delayed"
            st.warning(f"⚠️ **Status:** Delayed | **Arrival:** {actual_arrival_display}")
        else:
            journey_status = "On Time"
            st.success(f"✅ **Status:** On Time | **Arrival:** {actual_arrival_display}")

st.divider()

if st.button("Predict Refund", type="primary", use_container_width=True):
    if purchase_datetime > journey_datetime:
        st.error("Logical Error: Purchase date and time cannot be after the journey departure time!")
    else:
        raw_input_df = build_raw_input(
            purchase_dt=purchase_datetime,
            journey_dt=journey_datetime,
            expected_arrival_t=expected_arrival_time,
            actual_arrival_dt=actual_arrival_dt,
            purchase_type=purchase_type,
            payment_method=payment_method,
            ticket_type=ticket_type,
            price=price,
            railcard=railcard,
            departure_station=departure_station,
            arrival_destination=arrival_destination,
            journey_status=journey_status,
            reason_for_delay=reason_for_delay,
        )

        try:
            X_processed = transform_for_model(raw_input_df, processor, expected_features)
            proba = float(model.predict_proba(X_processed)[0, 1])
            pred = int(proba >= threshold)

            st.subheader("📊 Prediction Result")
            m1, m2, m3 = st.columns(3)
            m1.metric("Refund Probability", f"{proba * 100:.1f}%")
            m2.metric("Decision Threshold", f"{threshold:.2f}")
            m3.metric("Predicted Class", "1 (Refund Likely)" if pred == 1 else "0 (No Refund)")

            if pred == 1:
                st.warning(
                    f"🔔 **Likely Refund Request** (Probability ≥ Threshold)."
                )
            else:
                st.success(
                    f"✅ **No Refund Expected** (Probability < Threshold)."
                )

            with st.expander("Raw Input Sent to Preprocessor"):
                st.dataframe(raw_input_df, use_container_width=True)

            with st.expander("Processed Features Sent to Model"):
                st.dataframe(X_processed, use_container_width=True)

        except Exception as e:
            st.error(f"Error type: {type(e).__name__} — {e}")
            st.code(traceback.format_exc(), language="python")