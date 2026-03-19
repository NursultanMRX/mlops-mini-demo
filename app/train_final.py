# app/train_final.py
import pandas as pd
import tensorflow as tf
import mlflow
from sklearn.model_selection import train_test_split
from app.preprocess import preprocess
import json

df = pd.read_csv("data/adult11.csv")
X, y = preprocess(df)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

with open("best_params.json") as f:
    best_params = json.load(f)

EPOCHS = 50  # full training
BATCH_SIZE = 32

model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(best_params["dropout"]),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer=tf.keras.optimizers.Adam(best_params["lr"]),
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train, y_train, validation_data=(X_test, y_test),
                    epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1)

# MLflow logging
mlflow.log_params(best_params)
mlflow.log_metrics({"final_val_acc": history.history["val_accuracy"][-1]})
mlflow.keras.log_model(model, artifact_path="final_model")

# Save locally for artifact
model.save("app/final_model.keras")
