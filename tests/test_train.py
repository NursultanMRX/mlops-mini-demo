from app.train import train
import os

def test_train():
    train()
    assert os.path.exists("app/model.pkl")
    assert os.path.exists("metrics.json")
