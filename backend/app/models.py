from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base 

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, nullable=False)
    current_stock = Column(Integer, default=0)
    reorder_point = Column(Integer, default=10)
    lead_time_days = Column(Integer, default=7)

    sales = relationship("SalesHistory", back_populates="product", cascade="all, delete-orphan")
    forecasts = relationship("ForecastResult", back_populates="product", cascade="all, delete-orphan")

class SalesHistory(Base):
    __tablename__ = "sales_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    units_sold = Column(Integer, nullable=False)   

    product = relationship("Product", back_populates="sales")

class ForecastResult(Base):
    __tablename__ = "forecast_results"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    ds = Column(String, nullable=False)          # Forecast date
    yhat = Column(Float, nullable=False)         # Predicted units sold
    yhat_lower = Column(Float, nullable=False)   # Lower confidence bound
    yhat_upper = Column(Float, nullable=False)   # Upper confidence bound
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="forecasts")