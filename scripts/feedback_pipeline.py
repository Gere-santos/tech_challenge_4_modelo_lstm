import yfinance as yf
from datetime import date, timedelta
from app.database import SessionLocal
from app.monitoring import PredictionLog, PredictionFeedback
import pandas as pd


def get_predictions_without_feedback(db):
    return db.query(PredictionLog).outerjoin(
        PredictionFeedback,
        PredictionLog.id == PredictionFeedback.prediction_log_id
    ).filter(
        PredictionFeedback.id == None,
        PredictionLog.target_date < date.today()
    ).all()

def get_real_price(company, target_date):
    try:
        ticker_symbol = 'BBAS3'

        if not ticker_symbol:
            print(f"Ticker não encontrado para BBAS3")
            return None

        ticker = f"{ticker_symbol}.SA"

        df = yf.download(
            ticker,
            start=target_date - timedelta(days=7),
            end=target_date + timedelta(days=1),
            progress=False,
            auto_adjust=False
        )

        if df.empty:
            return None

        
        close = df["Close"]

    
        if isinstance(close, pd.DataFrame):
            close = close.squeeze()  

        close = close.dropna()

        if close.empty:
            return None

        
        close.index = close.index.date
        close = close[close.index <= target_date]

        if close.empty:
            return None

        return float(close.iloc[-1])

    except Exception as e:
        print(f"Erro ao buscar preço para {company}: {e}")
        return None

def save_feedback(db, pred, actual_value):
    absolute_error = abs(pred.prediction - actual_value)

    feedback = PredictionFeedback(
        prediction_log_id=pred.id,
        predicted_value=pred.prediction,
        actual_value=actual_value,
        absolute_error=absolute_error
    )

    db.add(feedback)
    db.commit()


def run_pipeline():
    db = SessionLocal()

    try:
        predictions = get_predictions_without_feedback(db)

        if not predictions:
            print("Nenhuma previsão pendente.")
            return

        for pred in predictions:
            print(f"Processando ID {pred.id} - {pred.company} - {pred.target_date}")

            real_price = get_real_price(pred.company, pred.target_date)

            if real_price is None:
                print(f"Sem dado para {pred.company} em {pred.target_date}")
                continue

            save_feedback(db, pred, real_price)

            print(f"Feedback salvo | erro: {abs(pred.prediction - real_price):.4f}")

    finally:
        db.close()


if __name__ == "__main__":
    run_pipeline()