import os
import joblib

from tensorflow.keras.models import load_model

# Diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Caminhos dos arquivos
model_path = os.path.join(BASE_DIR, "notebooks", "modelo_tf")
scaler_x_path = os.path.join(BASE_DIR, "models_artifacts", "scaler_x.pkl")
scaler_y_path = os.path.join(BASE_DIR, "models_artifacts", "scaler_y.pkl")

# Carregar modelo (uma única vez)
model = load_model(model_path, compile=False)

# Carregar scalers
scaler_x = joblib.load(scaler_x_path)
scaler_y = joblib.load(scaler_y_path)
