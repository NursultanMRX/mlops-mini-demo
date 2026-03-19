# app/train_final.py
import pandas as pd
import tensorflow as tf
import mlflow
import json
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from app.preprocess import preprocess

# MLflow Tensorflow uchun avtomatik loglarni yozishni yoqamiz (har bir epoch uchun)
mlflow.tensorflow.autolog()

df = pd.read_csv("data/adult11.csv")
X, y = preprocess(df)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

with open("best_params.json") as f:
    best_params = json.load(f)

EPOCHS = 50 
BATCH_SIZE = 32

model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(best_params["dropout"]),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=best_params["lr"]),
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Final run uchun alohida sessiya ochamiz
with mlflow.start_run(run_name="final_model_training"):
    history = model.fit(X_train, y_train, validation_data=(X_test, y_test),
                        epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1)

    # --- 📊 GRAFIKLARNI CHIZISH ---
    plt.figure(figsize=(12, 5))

    # 1. Accuracy grafiki
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    # 2. Loss grafiki
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    # Rasm qilib saqlash
    plt.savefig("metrics.png")
    
    # MLflow'ga rasmni va parametrlarni biriktirish
    mlflow.log_params(best_params)
    mlflow.log_artifact("metrics.png")
    
    # Modelni saqlash
    model.save("app/final_model.keras")
