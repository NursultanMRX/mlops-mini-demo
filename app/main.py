# app/main.py
from fastapi import FastAPI
import joblib

app = FastAPI()
model = joblib.load("app/model.pkl")

@app.get("/predict")
def predict():
    return {"pred": int(model.predict([[5.1,3.5,1.4,0.2]])[0])}
