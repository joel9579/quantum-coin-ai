import os
import pandas as pd
import joblib
from prophet import Prophet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt

MODEL_DIR = "models" # Adjust if needed
FORECAST_DIR = "reports/forecasts"
os.makedirs(FORECAST_DIR, exist_ok=True)

def plot_forecast_image(forecast, coin_name):
    """Save forecast chart to PNG for PDF export"""
    plt.figure(figsize=(10, 5))
    plt.plot(forecast['ds'], forecast['yhat'], label='Forecast')
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.2)
    plt.title(f"{coin_name} Forecast")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    chart_path = os.path.join(FORECAST_DIR, f"{coin_name}_forecast_chart.png")
    plt.savefig(chart_path)
    plt.close()
    return chart_path

def predict_future(coin_name="coin_Bitcoin", days_ahead=365):
    model_path = os.path.join(MODEL_DIR, f"{coin_name}_prophet_model.pkl")
    model = joblib.load(model_path)

    # Create future dataframe and forecast
    future = model.make_future_dataframe(periods=days_ahead)
    forecast = model.predict(future)

    # Save to Excel
    excel_path = os.path.join(FORECAST_DIR, f"{coin_name}_forecast.xlsx")
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_excel(excel_path, index=False)

    # Save PDF
    pdf_path = os.path.join(FORECAST_DIR, f"{coin_name}_forecast.pdf")
    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    story = [Paragraph(f"{coin_name} Forecast to {future['ds'].iloc[-1].date()}", styles["Title"]),
             Spacer(1, 12)]

    # Insert chart
    chart_path = plot_forecast_image(forecast, coin_name)
    story.append(Image(chart_path, width=500, height=250))

    doc.build(story)

    print(f"Saved Excel to {excel_path}")
    print(f"Saved PDF to {pdf_path}")
    return {"forecast": forecast}

if __name__ == "__main__":
    predict_future("coin_Bitcoin", 3650*5)

def get_last_date(coin_name):
    df_path = f"data/unpacked/{coin_name}.csv"
    df = pd.read_csv(df_path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df['Date'].max()
