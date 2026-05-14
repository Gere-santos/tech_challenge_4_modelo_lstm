import numpy as np
import pandas as pd
from app.model_loader import model, scaler_x, scaler_y  # Importe o scaler_y também
from app.features_engeneering import create_features

SEQUENCE_SIZE = 5

EXPECTED_FEATURES = [
    'fechamento', 'volume', 'sma_5', 'sma_10', 'vol_10', 
    'mom_5', 'maxima', 'minima', 'variacao', 'abertura'
]

def prepare_input(historical_data):

    df = pd.DataFrame(historical_data)
    

    df = create_features(df)

    df = df[EXPECTED_FEATURES]
    

    values = df.values
    scaled = scaler_x.transform(values)
    print(df.head())
    print(df.tail())

    
    return scaled

def predict_stock_price(historical_data, steps=SEQUENCE_SIZE):
  
    X_processed = prepare_input(historical_data)
    
    if len(X_processed) < SEQUENCE_SIZE:
        raise ValueError(
            f"Dados insuficientes. O modelo exige pelo menos {SEQUENCE_SIZE} dias"
        )


    last_window = X_processed[-steps:] 

    X_matrix = np.expand_dims(last_window, axis=0)


    prediction_scaled = model.predict(X_matrix)
    

    prediction = scaler_y.inverse_transform(prediction_scaled)
    
  
    return float(prediction[0][0])
