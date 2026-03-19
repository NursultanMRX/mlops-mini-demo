# app/train_tune.py
import pandas as pd
import tensorflow as tf
import mlflow
import optuna
from sklearn.model_selection import train_test_split
from app.preprocess import preprocess

df = pd.read_csv("data/adult11.csv")
X, y = preprocess(df)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

EPOCHS = 10  # small trial

def create_model(lr, dropout):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(dropout),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(lr),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

def objective(trial):
    # MLflow uchun har bir trialga alohida sessiya (run) ochamiz
    with mlflow.start_run(run_name=f"trial_{trial.number}"):
        lr = trial.suggest_float("lr", 1e-4, 1e-2, log=True)
        dropout = trial.suggest_float("dropout", 0.1, 0.5)
        
        model = create_model(lr, dropout)
        history = model.fit(X_train, y_train, validation_data=(X_val, y_val),
                            epochs=EPOCHS, batch_size=32, verbose=0)
        
        val_acc = history.history["val_accuracy"][-1]
        
        # Endi param va metrikalar shu ochiq run ichiga yoziladi
        mlflow.log_params({"lr": lr, "dropout": dropout})
        mlflow.log_metrics({"val_acc": val_acc})
        
        return val_acc

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=5)

import json
with open("best_params.json", "w") as f:
    json.dump(study.best_params, f)
