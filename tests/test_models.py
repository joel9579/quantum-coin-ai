import os
import joblib
from src.models.train_models import train_and_save_model

def test_model_training_and_save():
    coin = "coin_bitcoin"
    model_path = f"models/{coin}_prophet_model.pkl"

    train_and_save_model(coin)

    assert os.path.exists(model_path), f"Model file not saved at {model_path}"

    model = joblib.load(model_path)
    assert hasattr(model, "predict"), "Loaded model does not have a predict method"
