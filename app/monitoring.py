from sqlalchemy import Column, Integer, Float, String, DateTime, Date, Boolean
from datetime import datetime
from app.database import Base
from pydantic import BaseModel
from typing import List, Optional

class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(String)
    company = Column(String)
    prediction = Column(Float)
    model_version = Column(String)
    request_size = Column(Integer)
    prediction_date = Column(Date)   
    target_date = Column(Date)     
    latency_ms = Column(Float)
    status = Column(String)  
    error_message = Column(String)

    created_at = Column(DateTime, default=datetime.now())


class PredictionFeedback(Base):
    __tablename__ = "prediction_feedback"

    id = Column(Integer, primary_key=True)
    prediction_log_id = Column(Integer)
    predicted_value = Column(Float)
    actual_value = Column(Float)
    absolute_error = Column(Float)
    created_at = Column(DateTime, default=datetime.now())

class MonitorSummary(BaseModel):
    total_predictions: int
    average_error: Optional[float]
    model_version: str
    last_prediction_at: Optional[datetime]
    accuracy_rate: float       