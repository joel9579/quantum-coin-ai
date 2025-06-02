import os
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO
import base64
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import openpyxl

MODEL_DIR = "src/models"
FORECAST_DIR = "reports/forecast"
UNPACKED_DIR = "data/unpacked"
PROCESSED_DIR = "data/processed"
STATIC_LOGO_PATH = "src/app/static/logo.png"
os.makedirs(FORECAST_DIR, exist_ok=True)


def predict_coin_price(coin: str, target_year: int):
    # Try both .parquet and .csv formats
    parquet_path = os.path.join(PROCESSED_DIR, f"{coin}.parquet")
    base_path = os.path.join(UNPACKED_DIR, f"{coin}.csv")
    alt_path = os.path.join(UNPACKED_DIR, f"coin_{coin}.csv")

    if os.path.exists(parquet_path):
        df = pd.read_parquet(parquet_path)
        if "date" not in df.columns or "close" not in df.columns:
            raise ValueError("Parquet file must contain 'date' and 'close' columns")
    elif os.path.exists(base_path):
        df = pd.read_csv(base_path)
    elif os.path.exists(alt_path):
        df = pd.read_csv(alt_path)
    else:
        raise FileNotFoundError(f"No historical data found for {coin}")

    # Prepare DataFrame
    df = df.rename(columns={"Date": "ds", "Close": "y"})
    df["ds"] = pd.to_datetime(df["ds"])
    df = df[["ds", "y"]].dropna()

    # Train model
    model = Prophet(daily_seasonality=True)
    model.fit(df)

    # Forecast to target year
    future_end = pd.to_datetime(f"{target_year}-01-01")
    days = (future_end - df["ds"].max()).days
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)
    forecast_filtered = forecast[forecast["ds"] >= datetime.now()]
    forecast_result = forecast_filtered[["ds", "yhat"]].tail(365)

    # Base forecast chart
    fig1 = model.plot(forecast)
    buf1 = BytesIO()
    plt.savefig(buf1, format="png")
    plt.close(fig1)
    buf1.seek(0)
    chart_base64 = base64.b64encode(buf1.read()).decode("utf-8")

    # Overlay chart (actual vs predicted)
    fig2, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["ds"], df["y"], label="Actual", color="gray")
    ax.plot(forecast["ds"], forecast["yhat"], label="Forecast", color="blue")
    ax.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], color="lightblue", alpha=0.3)
    ax.set_title(f"{coin.replace('coin_', '').capitalize()} Actual vs Predicted")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    ax.grid(True)
    buf2 = BytesIO()
    plt.savefig(buf2, format="png")
    plt.close(fig2)
    buf2.seek(0)
    overlay_base64 = base64.b64encode(buf2.read()).decode("utf-8")

    # Save forecast to CSV
    csv_path = os.path.join(FORECAST_DIR, f"{coin}_forecast.csv")
    forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_csv(csv_path, index=False)

    # Save forecast to Excel (with logo)
    excel_path = os.path.join(FORECAST_DIR, f"{coin}_forecast.xlsx")
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        forecast.to_excel(writer, sheet_name="Forecast", index=False)
        ws = writer.sheets["Forecast"]
        ws.insert_rows(0, 4)
        ws["A1"] = f"{coin.replace('coin_', '').capitalize()} Forecast Report ({target_year})"
        try:
            img = openpyxl.drawing.image.Image(STATIC_LOGO_PATH)
            img.width = 100
            img.height = 50
            ws.add_image(img, "G1")
        except:
            pass

    # Save PDF report
    pdf_path = os.path.join(FORECAST_DIR, f"{coin}_forecast.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = [
        Image(STATIC_LOGO_PATH, width=100, height=50),
        Spacer(1, 12),
        Paragraph(f"{coin.replace('coin_', '').capitalize()} Forecast Report", styles["Title"]),
        Paragraph(f"Forecast up to year {target_year}", styles["Normal"]),
        Spacer(1, 12),
        Paragraph(f"Minimum Forecast: ${forecast_result['yhat'].min():.2f}", styles["Normal"]),
        Paragraph(f"Maximum Forecast: ${forecast_result['yhat'].max():.2f}", styles["Normal"]),
        Paragraph(f"Average Forecast: ${forecast_result['yhat'].mean():.2f}", styles["Normal"]),
    ]
    doc.build(story)

    return {
        "forecast": forecast_result.to_dict(orient="records"),
        "chart": chart_base64,
        "overlay_chart": overlay_base64,
        "csv": csv_path,
        "excel": excel_path,
        "pdf": pdf_path
    }




