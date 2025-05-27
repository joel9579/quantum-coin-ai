import traceback
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.app.routes import router
from src.app.templates import templates

@router.get("/results", response_class=HTMLResponse)
def show_results(request: Request, coin: str, target_year: int):
    try:
        forecast_df = predict_price(coin, target_year)
        forecast_table = forecast_df.to_html(index=False)
        return templates.TemplateResponse("results.html", {
            "request": request,
            "coin": coin,
            "target_year": target_year,
            "forecast_table": forecast_table
        })
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error:</h1><pre>{traceback.format_exc()}</pre>", status_code=500)
