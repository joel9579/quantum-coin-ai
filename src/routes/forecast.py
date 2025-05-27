from fastapi import APIRouter, UploadFile, File, Form
from io import BytesIO
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import base64
from datetime import datetime

router = APIRouter()

@router.post("/upload_predict")
async def upload_and_predict(
    coin: str = Form(...),
    target_year: int = Form(...),
    file: UploadFile = File(...)
):
    # Read uploaded file
    contents = await file.read()
    df = pd.read_csv(BytesIO(contents))

    # Ensure correct format
    df = df.rename(columns={"Date": "ds", "Close": "y"})
    df["ds"] = pd.to_datetime(df["ds"])
    df = df[["ds", "y"]].dropna()

    # Train Prophet model
    model = Prophet(daily_seasonality=True)
    model.fit(df)

    # Forecast future to target year
    future_end = pd.to_datetime(f"{target_year}-01-01")
    days = (future_end - df["ds"].max()).days
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    # Filter forecasted values for the next 365 days
    forecast_filtered = forecast[forecast["ds"] >= datetime.now()]
    forecast_result = forecast_filtered[["ds", "yhat"]].tail(365)

    # Create base64 plot
    fig = model.plot(forecast)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    chart_base64 = base64.b64encode(buf.read()).decode("utf-8")

    # Return structured data
    return {
        "coin": coin,
        "year": target_year,
        "forecast": forecast_result.to_dict(orient="records"),
        "chart": chart_base64
    }
