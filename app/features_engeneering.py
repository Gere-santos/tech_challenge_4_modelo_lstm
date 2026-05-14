import pandas as pd


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("data")

    df['return'] = df['fechamento'].pct_change()

    df['variacao'] = df['fechamento'] - df['abertura']
    df['vol_10'] = df['return'].rolling(10).std()

    
    df['sma_5'] = df['fechamento'].rolling(5).mean()
    df['sma_10'] = df['fechamento'].rolling(10).mean()
    df['mom_5'] = df['fechamento'] - df['fechamento'].shift(5)
    df['target'] = df['fechamento'].shift(-1)

    df = df.dropna()
    if len(df) < 19:
        raise ValueError(f"Dados insuficientes. O modelo exige pelo menos 30 dias de registros históricos")
    
 
    return df