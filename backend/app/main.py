from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models  # Ensures SQLAlchemy registers your models for table creation
from app.routers import forecast

# Automatically creates SQLite/PostgreSQL database tables on startup 
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DemandSense API",
    description="Smart Inventory & Sales Forecasting Platform",
    version="1.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the forecast router
app.include_router(forecast.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Demandsense API- Inventory & Sales Forecasting"}