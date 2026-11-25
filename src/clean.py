import pandas as pd

df = pd.read_csv("data/raw/railway.csv")
def clean_dataset(df):
    df = df.copy()

    initial_rows = len(df)
    df = df.drop_duplicates()
    if initial_rows - len(df) > 0:
        print(f"[Clean] Removed {initial_rows - len(df)} duplicate rows.")

    df["Purchase Datetime"] = df["Date of Purchase"] + " " + df["Time of Purchase"]
    df["Journey Datetime"] = df["Date of Journey"] + " " + df["Departure Time"]



    column_deleted = df.columns[df.columns.str.endswith("ID")]
    columns_to_drop = list(column_deleted) + ["Date of Purchase", "Time of Purchase", "Date of Journey", "Departure Time", "Ticket Class"]

    df.drop(columns=columns_to_drop, inplace=True)

    delay_reason_map = {
            "Signal Failure": "Signal Failure",
            "Signal failure": "Signal Failure",
            "Staff Shortage": "Staff Shortage",
            "Staffing": "Staff Shortage",
            "Weather": "Weather Conditions",
            "Technical": "Technical Issues"
        }

    df["Reason for Delay"] = df["Reason for Delay"].fillna("No Delay").str.strip().str.title().replace(delay_reason_map)
    df["Railcard"] = df["Railcard"].fillna("No Railcard")
    return df

df = clean_dataset(df)
df.to_csv("data/cleaned/cleaned_railway.csv", index=False)