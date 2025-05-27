import os
import pandas as pd
import joblib
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

PROCESSED_DATA = "C:\\Users\\mugesh\\Downloads\\Project - Joel\\crypto-forecast-app\\data\\processed\\combined_dataset.feather"
MODEL_DIR = "C:\\Users\\mugesh\\Downloads\\Project - Joel\\crypto-forecast-app\\src\\models"

def evaluate_model(coin_name="coin_bitcoin", lookback_days=90):
    # Load data
    df = pd.read_feather(PROCESSED_DATA)
    df = df[df['coin'] == coin_name][['date', 'close']].dropna()
    df.rename(columns={"date": "ds", "close": "y"}, inplace=True)

    # Only use last N days
    df = df.sort_values("ds").tail(lookback_days)

    # Load model
    model_path = os.path.join(MODEL_DIR, f"{coin_name}_prophet_model.pkl")
    if not os.path.exists(model_path):
        print("Model not found.")
        return

    model: Prophet = joblib.load(model_path)
    forecast = model.predict(df[['ds']])

    # Merge actual and predicted
    merged = df.copy()
    merged["yhat"] = forecast["yhat"].values

    # Metrics
    mse = mean_squared_error(merged["y"], merged["yhat"])
    mae = mean_absolute_error(merged["y"], merged["yhat"])
    rmse = np.sqrt(mse)

    print(f"Evaluation for {coin_name} (last {lookback_days} days):")
    print(f" MAE : {mae:.2f}")
    print(f" MSE : {mse:.2f}")
    print(f" RMSE: {rmse:.2f}")

if __name__ == "__main__":
    evaluate_model("coin_bitcoin", 90)
