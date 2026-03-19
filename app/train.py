import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import json
import joblib

def train():
    df = pd.read_csv("data/titanic.csv")

    # example: last column = target
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    # save model
    joblib.dump(model, "app/model.pkl")

    # save metrics
    metrics = {"accuracy": float(acc)}
    with open("metrics.json", "w") as f:
        json.dump(metrics, f)

    # plot (simple)
    plt.figure()
    plt.bar(["accuracy"], [acc])
    plt.savefig("metrics.png")

if __name__ == "__main__":
    train()
