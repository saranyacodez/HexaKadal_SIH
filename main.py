# main.py - FastAPI Backend Dispatcher Engine

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ports_database import validate_vessel_route, PORTS_DATA
from model_engine import train_and_forecast

# Uvicorn idha dhaan thedudhu - "app" variable mandatory
app = FastAPI(title="HexaKadal AI Charter Engine")

# Enable Cross-Origin Resource Sharing for Interactive Frontend UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CharterInput(BaseModel):
    origin_port: str
    dest_port: str
    cargo_volume: float

@app.post("/api/charter-analytics")
def get_dashboard_data(req: CharterInput):
    hist_df, forecast_df = train_and_forecast()
    min_rate = float(forecast_df['Predicted_Freight_Rate'].min())
    max_rate = float(forecast_df['Predicted_Freight_Rate'].max())
    best_date = forecast_df.loc[forecast_df['Predicted_Freight_Rate'].idxmin()]['Date'].strftime('%d %b %Y')

    vessel_info = validate_vessel_route(req.origin_port, req.dest_port, req.cargo_volume)

    discharge_rate = PORTS_DATA[req.dest_port]['discharge_rate_pd']
    est_laytime_days = round(req.cargo_volume / discharge_rate, 2)
    idle_risk_score = "LOW" if est_laytime_days <= 3.5 else "HIGH (Demurrage Risk)"

    market_volatility = round(max_rate - min_rate, 2)
    risk_level = "CRITICAL" if market_volatility > 4.0 else "STABLE"
    
    return {
        "forecasting": {
            "min_rate": round(min_rate, 2),
            "max_rate": round(max_rate, 2),
            "best_entry_date": best_date,
            "chart_dates": forecast_df['Date'].dt.strftime('%d %b').tolist(),
            "chart_rates": forecast_df['Predicted_Freight_Rate'].round(2).tolist()
        },
        "vessel_optimization": vessel_info,
        "idle_management": {
            "est_laytime_days": est_laytime_days,
            "idle_risk": idle_risk_score,
            "recommendation": "Apply Slow-Steaming to align with berth window" if idle_risk_score == "HIGH (Demurrage Risk)" else "Optimal transit navigation"
        },
        "risk_mitigation": {
            "risk_level": risk_level,
            "market_volatility_score": market_volatility,
            "reason_code": "ERR_VOLATILITY_SPIKE: High spot rate variance" if risk_level == "CRITICAL" else "SYS_OK: Stable market window"
        }
    }