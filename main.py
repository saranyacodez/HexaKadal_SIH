import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="HexaKadal - SIH Production Architecture")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FreightRequest(BaseModel):
    origin_port: str
    discharge_port: str
    cargo_volume: float
    commodity_type: str = "Crude oil, average"

@app.get("/")
def serve_frontend():
    # Try multiple common paths for index.html during cloud deployment
    for path in ["index.html", "./index.html", os.path.join(os.path.dirname(__file__), "index.html")]:
        if os.path.exists(path):
            return FileResponse(path)
    return {"status": "HexaKadal Backend Running Successfully", "files_in_dir": os.listdir(".")}