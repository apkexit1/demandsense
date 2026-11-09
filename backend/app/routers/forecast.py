import io
import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List

# Import your actual Prophet forecasting function from services
from app.services.forecasting import predict_demand

# 1. Initialize the API router 
router = APIRouter(
    prefix="/forecast", # Adds a common prefix to all routes in this file 
    tags=["Forecast"]   # Groups endpoints nicely in FastAPI's Swagger DOCs (/docs)
)

# Define your Pydantic request body models
class SalesRecord(BaseModel):
    date: str
    units_sold: float

class ForecastRequest(BaseModel):
    sales_data: List[SalesRecord]
    periods: int = 30

# 2. Define endpoint for JSON payloads using the Prophet model
@router.post("/")
def get_demand_forecast(payload: ForecastRequest):
    try:
        # Convert Pydantic models to a list of dictionaries
        data_dicts = [item.dict() for item in payload.sales_data]
        
        # Call your actual Prophet function
        forecast_results = predict_demand(data_dicts, periods=payload.periods)
        
        return {
            "status": "success",
            "periods_forecasted": payload.periods,
            "forecast": forecast_results
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# 3. Define endpoint for CSV file uploads
@router.post("/upload-csv/")
async def forecast_from_csv(file: UploadFile = File(...), periods: int = 30):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")
    
    try:
        # Read uploaded CSV file into memory
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Ensure required column headers exist
        if 'date' not in df.columns or 'units_sold' not in df.columns:
            raise HTTPException(
                status_code=400, 
                detail="CSV file must contain 'date' and 'units_sold' column headers."
            )
        
        # Convert dataframe to list of dictionaries
        sales_data = df.to_dict(orient='records')
        
        # Run through your Prophet forecasting function
        forecast_results = predict_demand(sales_data, periods=periods)
        
        return {
            "status": "success",
            "filename": file.filename,
            "periods_forecasted": periods,
            "forecast": forecast_results
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# 4. Status check endpoint
@router.get("/status")
def forecast_status():
    return {"status": "Forecast service is active"}