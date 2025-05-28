import os
from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import base64
import pandas as pd
from prophet import Prophet

from src.app.static.visuals_output import generate_visual_dashboard
from src.models.predict_future import predict_coin_price

router = APIRouter()
templates = Jinja2Templates(directory="src/app/templates")

@app.get("/", response_class=HTMLResponse)
async def landing_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
      <title>Quantum Coin AI</title>
      <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
      <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 40px; }
        h1 { color: #4B0082; }
        a { padding: 10px 20px; text-decoration: none; background-color: #4B0082; color: white; border-radius: 5px; }
        a:hover { background-color: #5D3FD3; }
      </style>
    </head>
    <body>
      <img src="/static/logo.png" alt="Quantum Coin AI" width="100">
      <h1>Welcome to Quantum Coin AI</h1>
      <p>Predict cryptocurrency trends with AI forecasting tools.</p>
      <a href="/ui">Go to Dashboard</a>
    </body>
    </html>
    """


# Load all coin names from both CSV and Parquet
def get_available_coins():
    coins = set()
    csv_dir = "data/unpacked"
    parquet_dir = "data/processed"

    if os.path.exists(csv_dir):
        for file in os.listdir(csv_dir):
            if file.endswith(".csv"):
                coins.add(os.path.splitext(file)[0])

    if os.path.exists(parquet_dir):
        for file in os.listdir(parquet_dir):
            if file.endswith(".parquet"):
                coins.add(os.path.splitext(file)[0])

    return sorted(coins)


# 1. Landing UI page
@router.get("/ui", response_class=HTMLResponse)
def home_ui(request: Request):
    coins = get_available_coins()
    years = list(range(2026, 2061))

    return templates.TemplateResponse("ui.html", {
        "request": request,
        "coins": coins,
        "years": years
    })


# 2. Coin list API (used for dynamic dropdowns)
@router.get("/coins")
def list_coins():
    return {"coins": get_available_coins()}


# 3. Visual Dashboard
@router.get("/visual-dashboard", response_class=HTMLResponse)
def show_dashboard(request: Request):
    return generate_visual_dashboard(request)


@router.get("/visuals", response_class=HTMLResponse)
def render_visual_dashboard(request: Request):
    return generate_visual_dashboard(request)


# 4. Forecast Result page (HTML)
@router.get("/results", response_class=HTMLResponse)
def show_results(request: Request, coin: str, target_year: int):
    result = predict_coin_price(coin, target_year)
    return templates.TemplateResponse("results.html", {
        "request": request,
        "coin": coin,
        "target_year": target_year,
        "forecast": result["forecast"],
        "chart": result["chart"],
        "overlay_chart": result["overlay_chart"]
    })


# 5. Prediction via JSON POST
class PredictRequest(BaseModel):
    coin: str
    target_year: int


@router.post("/predict")
async def predict(request: PredictRequest):
    result = predict_coin_price(request.coin, request.target_year)
    return {
        "coin": request.coin,
        "year": request.target_year,
        "forecast": result
    }


# 6. Visuals API for images
@router.get("/visuals-data")
def get_visuals_data():
    return {
        "coin_visuals": {
            "coin_Bitcoin": {
                "trend": "/static/reports/visuals/coin_Bitcoin_trend.png",
                "summary": "/static/reports/visuals/coin_Bitcoin_yearly_summary.png"
            },
            "coin_Ethereum": {
                "trend": "/static/reports/visuals/coin_Ethereum_trend.png",
                "summary": "/static/reports/visuals/coin_Ethereum_yearly_summary.png"
            }
            # Extend this dynamically later
        },
        "correlation_img": "/static/reports/visuals/coin_correlation_matrix.png"
    }


# 7. Upload file & predict from custom CSV
@router.post("/upload_predict")
async def upload_predict(coin: str = Form(...), target_year: int = Form(...), file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(BytesIO(contents))

    df = df.rename(columns={"Date": "ds", "Close": "y"})
    df["ds"] = pd.to_datetime(df["ds"])
    df = df[["ds", "y"]].dropna()

    model = Prophet(daily_seasonality=True)
    model.fit(df)

    future_end = pd.to_datetime(f"{target_year}-01-01")
    days = (future_end - df["ds"].max()).days
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    forecast_filtered = forecast[forecast["ds"] >= datetime.now()]
    forecast_result = forecast_filtered[["ds", "yhat"]].tail(365)

    # Plot
    fig = model.plot(forecast)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    chart_base64 = base64.b64encode(buf.read()).decode("utf-8")

    return {
        "coin": coin,
        "year": target_year,
        "forecast": forecast_result.to_dict(orient="records"),
        "chart": chart_base64
    }
