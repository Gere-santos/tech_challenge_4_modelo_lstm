from fastapi import FastAPI, HTTPException, BackgroundTasks, Header
from app.schemas import PredictionRequest, PredictionResponse
from app.predictor import predict_stock_price
from app.database import SessionLocal, Base, engine
from app.monitoring import PredictionLog, PredictionFeedback
import pandas as pd
from sqlalchemy import func
from datetime import datetime, timezone, timedelta
from app.date_utils import next_business_day
import math
from scripts.feedback_pipeline import run_pipeline
import os
from dotenv import load_dotenv
from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST
)


from fastapi import Response
import time

load_dotenv()

senha_pura = os.getenv("tc_fiap_4") 




app = FastAPI(
    title="BB Market Predictor",
    version="1.0.0"
)

REQUEST_COUNT = Counter("api_requests_total", "Total de requisições")
REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Tempo de resposta")

MODEL_MAE = Gauge("model_mae", "Mean Absolute Error do modelo")
MODEL_RMSE = Gauge("model_rmse", "Root Mean Squared Error do modelo")
MODEL_MAPE = Gauge("model_mape", "Mean Absolute Percentage Error do modelo")

@app.get("/metrics")
def prometheus_metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.middleware("http")
async def metrics_middleware(request, call_next):

    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    REQUEST_COUNT.inc()
    REQUEST_LATENCY.observe(duration)

    return response


MODEL_VERSION = "lstm_v1"


@app.get("/health", summary="Verificar status da API",
    description="Endpoint para validar se a API está online e identificar a versão do modelo em uso.")

def health():
    
    return {
        "status": "ok",
        "model_version": MODEL_VERSION
    }
from fastapi import HTTPException
from datetime import datetime
import pandas as pd
import time
import uuid

@app.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Realizar previsão de preço de ação",
    description="Recebe dados históricos de uma ação e retorna a previsão do próximo valor de fechamento utilizando o modelo treinado."
)
def predict(request: PredictionRequest):

    db = SessionLocal()

    start_time = time.time()
    status = "success"
    error_message = None
    prediction = None

    try:
        input_df = pd.DataFrame([item.dict() for item in request.historical_data])

    # 🔥 VALIDAÇÃO 1 — vazio
        if input_df.empty:
            raise HTTPException(status_code=400, detail="Historical data is empty")

    # 🔥 VALIDAÇÃO 2 — quantidade mínima
        if len(request.historical_data) < 10:
            raise HTTPException(
                status_code=400,
                detail="At least 10 data points are required"
            )

    
        if input_df.isnull().values.any():
            raise HTTPException(
                status_code=400,
                detail="Input contains null values"
            )

    
        prediction = predict_stock_price(input_df)

        today = datetime.now().date()
        #two_days_ago = today - timedelta(days=2)
        target = next_business_day(today)

    except Exception as e:
        status = "error"
        error_message = str(e)
        db.rollback()
        raise HTTPException(status_code=500, detail=error_message)

    finally:
        latency_ms = (time.time() - start_time) * 1000

        print("Local:", datetime.now())
        print("UTC:", datetime.now(timezone.utc))
        log = PredictionLog(
            prediction_id=str(uuid.uuid4()),    
            company=request.company,
            prediction=float(prediction) if prediction else None,
            model_version=MODEL_VERSION,
            request_size=len(request.historical_data),
            prediction_date= datetime.now().date(),
            target_date=target if prediction else None,
            latency_ms=latency_ms,
            status=status,
            error_message=error_message
        )
        
        db.add(log)
        db.commit()
        db.refresh(log)
        db.close()

    return {
        "prediction_id": log.id,
        "company": request.company,
        "prediction": float(prediction),
        "model_version": MODEL_VERSION,
        'target': target
    }

@app.get("/monitor/summary", 
         summary="Resumo geral do modelo",
    description="Retorna uma visão consolidada do desempenho do modelo, incluindo total de previsões, erro médio e data da última predição.")
def monitor_summary():
    db = SessionLocal()

    total_predictions = db.query(PredictionLog).count()

    last_prediction = db.query(PredictionLog).order_by(
        PredictionLog.created_at.desc()
    ).first()

    avg_error = db.query(func.avg(PredictionFeedback.absolute_error)).scalar()

    return {
        "total_predictions": total_predictions,
        "average_error": float(avg_error) if avg_error else None,
        "last_prediction_at": last_prediction.created_at if last_prediction else None,
        "model_version": MODEL_VERSION
    }

from sqlalchemy import Boolean

from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    prediction_log_id: int
    actual_value: float


@app.post("/monitor/feedback",
          summary="Registrar valor real da previsão",
    description="Recebe o valor real observado de uma previsão anterior e calcula o erro absoluto, armazenando o resultado para monitoramento do modelo.")
def register_feedback(request: FeedbackRequest):
    db = SessionLocal()

    try:
        log = db.query(PredictionLog).filter(
            PredictionLog.id == request.prediction_log_id
        ).first()

        if not log:
            raise HTTPException(status_code=404, detail="Prediction not found")

        # 👇 AQUI
        existing_feedback = db.query(PredictionFeedback).filter(
            PredictionFeedback.prediction_log_id == log.id
        ).first()

        if existing_feedback:
            raise HTTPException(status_code=400, detail="Feedback already registered")

    
        absolute_error = abs(log.prediction - request.actual_value)

        feedback = PredictionFeedback(
            prediction_log_id=log.id,
            predicted_value=log.prediction,
            actual_value=request.actual_value,
            absolute_error=absolute_error
        )

        db.add(feedback)
        db.commit()

        return {
            "prediction_log_id": log.id,
            "absolute_error": absolute_error
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()



@app.get("/monitor/metrics",
         summary="Métricas de desempenho do modelo",
    description="Calcula e retorna métricas de avaliação do modelo, com base nos feedbacks registrados."
)
def metrics():
    db = SessionLocal()

    feedbacks = db.query(PredictionFeedback).all()

    if not feedbacks:
        return {
            "mae": None,
            "rmse": None,
            "mape": None,
            "count": 0
        }

    errors = [(f.predicted_value - f.actual_value) for f in feedbacks]

    mae = sum(abs(e) for e in errors) / len(errors)
    rmse = math.sqrt(sum(e**2 for e in errors) / len(errors))

    mape = sum(
        abs((f.actual_value - f.predicted_value) / f.actual_value)
        for f in feedbacks if f.actual_value != 0
    ) / len(feedbacks)
    
    MODEL_MAE.set(mae)
    MODEL_RMSE.set(rmse)
    MODEL_MAPE.set(mape)

    return {
        "mae": mae,
        "rmse": rmse,
        "mape": mape,
        "count": len(feedbacks)
    }




API_KEY = os.getenv("SENHA_FEEDBACK")
@app.post("/run-feedback",
           summary="Atualização dos dados reais.",
    description="Captura os dados reais na API Yfinance para comparação com dados preditos.")
def run_feedback(background_tasks: BackgroundTasks, x_api_key: str = Header(None)):
    
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")

    background_tasks.add_task(run_pipeline)
    return {"status": "processing"}
