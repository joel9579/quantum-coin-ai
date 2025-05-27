import os
import pandas as pd
from prophet import Prophet
import joblib

UNPACKED_DIR = "C:\\Users\\mugesh\\Downloads\\Project - Joel\\crypto-forecast-app\\data\\unpacked"
MODEL_DIR = "C:\\Users\\mugesh\\Downloads\\Project - Joel\\crypto-forecast-app\\src\\models"
os.makedirs(MODEL_DIR, exist_ok=True)

for file in os.listdir(UNPACKED_DIR):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(UNPACKED_DIR, file))

        if "Date" not in df.columns or "Close" not in df.columns:
            print(f"Skipping {file} — required columns missing")
            continue

        df = df.rename(columns={"Date": "ds", "Close": "y"})
        df['ds'] = pd.to_datetime(df['ds'])
        df = df[["ds", "y"]].dropna()

        coin = os.path.splitext(file)[0]
        model = Prophet(daily_seasonality=True)
        model.fit(df)

        joblib.dump(model, os.path.join(MODEL_DIR, f"{coin}_prophet_model.pkl"))
        print(f"[✓] Model trained for {coin}")
