# app/train.py
import os
import json
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split
import pandas as pd
from app.preprocess import preprocess

EPOCHS = int(os.getenv("EPOCHS", 50))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 16))

def train():
    df = pd.read_csv("data/titanic.csv")
    df = preprocess(df)

    X = df.drop("Survived", axis=1).values
    y = df["Survived"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.3),

        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.3),

        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.001),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    log_dir = "logs"
    tensorboard_cb = tf.keras.callbacks.TensorBoard(log_dir=log_dir)

    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=[tensorboard_cb],
        verbose=1
    )

    # Save full history
    metrics = {
        "loss": history.history["loss"],
        "val_loss": history.history["val_loss"],
        "accuracy": history.history["accuracy"],
        "val_accuracy": history.history["val_accuracy"]
    }

    with open("metrics.json", "w") as f:
        json.dump(metrics, f)

    # Plot metrics from JSON
    plt.figure(figsize=(12,5))

    plt.subplot(1,2,1)
    plt.plot(metrics["loss"], label="train_loss", marker='o')
    plt.plot(metrics["val_loss"], label="val_loss", marker='x')
    plt.title("Loss per Epoch")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)

    plt.subplot(1,2,2)
    plt.plot(metrics["accuracy"], label="train_acc", marker='o')
    plt.plot(metrics["val_accuracy"], label="val_acc", marker='x')
    plt.title("Accuracy per Epoch")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("metrics.png")

    # Save model
    model.save("app/model_tf")

if __name__ == "__main__":
    train()
