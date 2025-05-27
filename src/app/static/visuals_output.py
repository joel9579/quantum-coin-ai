import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fastapi.templating import Jinja2Templates
from fastapi import Request

# Paths
BASE_DIR = os.path.dirname(__file__)
FORECAST_DIR = os.path.join(BASE_DIR, "reports/forecast")
OUTPUT_DIR = os.path.join(BASE_DIR, "reports/visuals")
UNPACKED_DIR = os.path.join(os.path.join(BASE_DIR, "../../../data/unpacked"))


# Create output folder
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Forecast Trend Line
def generate_forecast_trend(coin):
    file_path = os.path.join(FORECAST_DIR, f"{coin}_forecast.csv")
    df = pd.read_csv(file_path, parse_dates=["ds"])
    
    plt.figure(figsize=(10, 5))
    plt.plot(df["ds"], df["yhat"], label="Forecast", color="darkgreen")
    plt.fill_between(df["ds"], df["yhat_lower"], df["yhat_upper"], color="lightgreen", alpha=0.4)
    plt.title(f"{coin.replace('coin_', '')} Forecast Trend")
    plt.xlabel("Date")
    plt.ylabel("Predicted Price (USD)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"{coin}_trend.png"))
    plt.close()

# 2. Yearly Forecast Summary
def generate_yearly_summary(coin):
    file_path = os.path.join(FORECAST_DIR, f"{coin}_forecast.csv")
    df = pd.read_csv(file_path, parse_dates=["ds"])
    df["year"] = df["ds"].dt.year
    summary = df.groupby("year")["yhat"].mean().reset_index()

    plt.figure(figsize=(8, 4))
    sns.barplot(x="year", y="yhat", data=summary, palette="Blues_d")
    plt.title(f"{coin.replace('coin_', '')} Yearly Avg Forecast")
    plt.xlabel("Year")
    plt.ylabel("Average Price (USD)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"{coin}_yearly_summary.png"))
    plt.close()

# 3. Correlation Matrix from Unpacked Raw Files
def generate_correlation_matrix():
    data_frames = []
    for file in os.listdir(UNPACKED_DIR):
        if not file.endswith(".csv"):
         continue
    try:
        coin = file.replace(".csv", "")
        path = os.path.join(UNPACKED_DIR, file)
        df = pd.read_csv(path, usecols=["Date", "Close"])
        df.rename(columns={"Close": coin, "Date": "ds"}, inplace=True)
        df["ds"] = pd.to_datetime(df["ds"])
        data_frames.append(df)
    except ValueError as e:
        print(f"Skipping {file}: {e}")

    merged = data_frames[0]
    for df in data_frames[1:]:
        merged = pd.merge(merged, df, on="ds", how="outer")

    merged.set_index("ds", inplace=True)
    corr = merged.corr()

    plt.figure(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix of Cryptocurrencies")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "coin_correlation_matrix.png"))
    plt.close()

templates = Jinja2Templates(directory="src/app/templates")

def generate_visual_dashboard(request: Request):
    import os
    import re

    VISUALS_DIR = os.path.abspath("src/app/static/reports/visuals")
    files = [f for f in os.listdir(VISUALS_DIR) if f.endswith(".png")]

    coin_visuals = {}
    for f in files:
        coin = re.sub(r"_(trend|yearly_summary)\.png$", "", f)
        visual_type = "trend" if "trend" in f else "summary"
        coin_visuals.setdefault(coin, {})[visual_type] = f"/static/reports/visuals/{f}"

    correlation_img = "/static/reports/visuals/coin_correlation_matrix.png"

    return templates.TemplateResponse("visuals.html", {
        "request": request,
        "coin_visuals": coin_visuals,
        "correlation_img": correlation_img
    })

# === Main Runner ===
if __name__ == "__main__":
    coins = [f.replace("_forecast.csv", "") for f in os.listdir(FORECAST_DIR) if f.endswith(".csv")]

    for coin in coins:
        print(f"Generating visuals for: {coin}")
        generate_forecast_trend(coin)
        generate_yearly_summary(coin)

    generate_correlation_matrix()
    print(f"Visuals saved in: {OUTPUT_DIR}")
