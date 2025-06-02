import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from src.app.routes import router as app_router
from src.routes import forecast
from src.utils.config_loader import load_config
from src.app.static.visuals_output import generate_visual_dashboard
from src.routes.forecast import router as forecast_router

# Load config files
paths = load_config("paths.yaml")
app_config = load_config("app_config.yaml")

# Initialize FastAPI app
app = FastAPI(title="Crypto Forecast API", debug=app_config.get("debug_mode", False))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static folders
app.mount("/static", StaticFiles(directory=paths["static"]), name="static")
app.mount("/visuals", StaticFiles(directory=paths["visuals"]), name="visuals")

# Include routers
app.include_router(app_router, prefix="/api")
app.include_router(forecast.router)
app.include_router(forecast_router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000)) # fallback to 10000 for local dev
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=port, reload=True)

# Set up Jinja2 templates
templates = Jinja2Templates(directory="src/app/templates")

# Load available coins from data folders
def get_all_coin_names():
    csv_dir = "data/unpacked"
    parquet_dir = "data/processed"

    coins = set()
    if os.path.exists(csv_dir):
        for file in os.listdir(csv_dir):
            if file.endswith(".csv"):
                coins.add(os.path.splitext(file)[0])

    if os.path.exists(parquet_dir):
        for file in os.listdir(parquet_dir):
            if file.endswith(".parquet"):
                coins.add(os.path.splitext(file)[0])

    return sorted(coins)

@app.get("/")
async def root():
    return RedirectResponse(url="/ui")
    
# Updated /ui route with coin/year selector
@app.get("/ui", response_class=HTMLResponse)
async def homepage(request: Request):
    coins = get_all_coin_names()
    years = list(range(2026, 2061))

    return templates.TemplateResponse("ui.html", {
        "request": request,
        "coins": coins,
        "years": years
    })

# Result prediction UI (static stub)
@app.post("/predict", response_class=HTMLResponse)
async def predict(coin: str, year: int):
    return HTMLResponse(content=f"<h2>{coin} Prediction for {year}</h2>")

# Result page using a template
@app.get("/result", response_class=HTMLResponse)
def show_result(request: Request):
    forecast_data = [
        {"ds": "2035-01-01", "yhat": 42000.50},
        {"ds": "2035-01-02", "yhat": 42120.75}
    ]
    chart_base64 = "iVBORw0KGgoAAAANSUhEUg..." # Placeholder

    return templates.TemplateResponse("results.html", {
        "request": request,
        "coin": "bitcoin",
        "target_year": 2035,
        "forecast": forecast_data,
        "chart": chart_base64
    })

# Visual dashboard route
@app.get("/visual-dashboard", response_class=HTMLResponse)
def show_dashboard():
    return generate_visual_dashboard()


