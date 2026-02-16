from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Load JSON data
# This looks in the same folder as the script itself
FILE_PATH = os.path.join(os.path.dirname(__file__), "telemetry_pings.json")

@app.post("/api/telemetry")
async def calculate_metrics(regions: list = Body(...), threshold_ms: int = Body(...)):
    # Read the JSON file into a DataFrame
    # If the JSON is a simple list of records, pd.read_json works perfectly
    df = pd.read_json(FILE_PATH)
    
    results = {}
    
    for region in regions:
        region_df = df[df['region'] == region]
        
        if region_df.empty:
            continue
            
        results[region] = {
            "avg_latency": float(region_df['latency_ms'].mean()),
            "p95_latency": float(region_df['latency_ms'].quantile(0.95)),
            "avg_uptime": float(region_df['uptime_pct'].mean()),
            "breaches": int((region_df['latency_ms'] > threshold_ms).sum())
        }
        
    return results
