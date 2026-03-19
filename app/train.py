import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import json

def preprocess(df):
    df = df.drop(columns=["PassengerId", "Name", "Ticket", "Cabin"])
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Embarked"] = df["Embarked"].fillna("S")

    df["Sex"] = df["Sex"].map({"male": 0, "female": 1})
    df["Embarked"] = df["Embarked"].map({"S": 0, "C": 1, "Q": 2})

    return df

def train():
    df = pd.read_csv("data/titanic.csv")
    df = preprocess(df)

    X = df.drop("Survived", axis=1).values
    y = df["Survived"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    history = model.fit(
        X_train, y_train,
        epochs=50,
        validation_data=(X_test, y_test),
        verbose=1
    )

    # metrics save
    final_acc = history.history["val_accuracy"][-1]

    with open("metrics.json", "w") as f:
        json.dump({"val_accuracy": float(final_acc)}, f)

    # plot loss
    plt.figure()
    plt.plot(history.history["loss"], label="train_loss")
    plt.plot(history.history["val_loss"], label="val_loss")
    plt.legend()
    plt.savefig("loss.png")

if __name__ == "__main__":
    train()
