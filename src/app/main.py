from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.app.routes import router
from src.routes import forecast
from src.utils.config_loader import load_config
from src.app.static.visuals_output import generate_visual_dashboard

# Load config files
paths = load_config("paths.yaml")
app_config = load_config("app_config.yaml")

# Initialize FastAPI app
app = FastAPI(title="Crypto Forecast API", debug=app_config.get("debug_mode", False))

# Include routers
app.include_router(router)
app.include_router(forecast.router)

# Set up Jinja2 templates (adjust path as per Render's structure)
templates = Jinja2Templates(directory="src/app/templates")

# Root HTML UI
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head><title>Quantum Coin AI</title></head>
        <body style='font-family:sans-serif;padding:2rem'>
            <h2>Quantum Coin AI - Crypto Forecast API</h2>
            <p>Go to <a href='/ui'>Dashboard</a> to upload files and view predictions.</p>
            <p>Try <code>/results?coin=coin_Bitcoin&target_year=2030</code> directly.</p>
        </body>
    </html>
    """

# Result page using template
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

# Mount static folders
app.mount("/static", StaticFiles(directory=paths["static"]), name="static")
app.mount("/visuals", StaticFiles(directory=paths["visuals"]), name="visuals")
