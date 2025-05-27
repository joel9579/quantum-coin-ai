import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from src.utils.coin_loader import get_available_coins
from src.app.static.visuals_output import generate_visual_dashboard
from src.models.predict_future import predict_coin_price
from fastapi import UploadFile, File, Form
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import base64


router = APIRouter()
templates = Jinja2Templates(directory="src/app/templates")

# 1. UI Landing Page

@router.get("/ui", response_class=HTMLResponse)
def home_ui():
    return """
    <html>
        <head><title>Quantum Coin AI</title></head>
        <body style='font-family:sans-serif;padding:2rem'>
            <h1>Welcome to Quantum Coin AI</h1>
            <p>Predict global cryptocurrency trends.</p>
            <p>Try the <a href='/visual-dashboard'>Visual Dashboard</a> or <a href='/'>Main Page</a>.</p>
        </body>
    </html>
    """

def get_available_coins(parquet_dir="data/processed"):
    coins = []
    for file in os.listdir(parquet_dir):
        if file.endswith(".parquet"):
            coin_name = file.replace(".parquet", "")
            coins.append(coin_name)
    return coins

@router.get("/coins")
def list_coins():
    coins = get_available_coins()
    return {"coins": coins}

# 2. Visual Dashboard

@router.get("/visual-dashboard", response_class=HTMLResponse)
def show_dashboard(request: Request):
    return generate_visual_dashboard(request)

@router.get("/visuals", response_class=HTMLResponse)
def render_visual_dashboard(request: Request):
    return generate_visual_dashboard(request)

# 3. Forecast Result Page

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

# 4. Prediction API

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

@router.get("/coins")
def list_coins():
    return {"coins": get_available_coins()}

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
            # Add more coins dynamically later if needed
        },
        "correlation_img": "/static/reports/visuals/coin_correlation_matrix.png"
    }

@router.post("/upload_predict")
async def upload_predict(coin: str = Form(...), target_year: int = Form(...), file: UploadFile = File(...)):
    import pandas as pd
    from prophet import Prophet

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
