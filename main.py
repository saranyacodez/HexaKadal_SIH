import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files_in_current = os.listdir(current_dir)
    
    # Check current directory and parent directory
    target_path = os.path.join(current_dir, "index.html")
    if os.path.exists(target_path):
        return FileResponse(target_path)
        
    return JSONResponse(status_code=200, content={
        "error": "index.html not found",
        "current_dir": current_dir,
        "files_found": files_in_current
    })