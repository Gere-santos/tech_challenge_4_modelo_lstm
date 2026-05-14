from pydantic import BaseModel
from typing import List
from datetime import date

class CandleData(BaseModel):
    data: str
    fechamento: float
    maxima: float
    minima: float
    abertura: float
    volume: float

class PredictionRequest(BaseModel):
    company: str
    historical_data: List[CandleData]

class PredictionResponse(BaseModel):
    prediction_id: int
    company: str
    prediction: float
    model_version: str
    target: date