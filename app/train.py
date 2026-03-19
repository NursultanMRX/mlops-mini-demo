import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import json
import matplotlib.pyplot as plt

def preprocess(df):
    # Drop useless columns
    df = df.drop(columns=["PassengerId", "Name", "Ticket", "Cabin"])

    # Fill missing values
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Embarked"] = df["Embarked"].fillna("S")

    # Encode categorical
    df["Sex"] = df["Sex"].map({"male": 0, "female": 1})
    df["Embarked"] = df["Embarked"].map({"S": 0, "C": 1, "Q": 2})

    return df

def train():
    df = pd.read_csv("data/titanic.csv")

    df = preprocess(df)

    X = df.drop("Survived", axis=1)
    y = df["Survived"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    # save model
    joblib.dump(model, "app/model.pkl")

    # save metrics
    with open("metrics.json", "w") as f:
        json.dump({"accuracy": float(acc)}, f)

    # plot
    plt.figure()
    plt.bar(["accuracy"], [acc])
    plt.savefig("metrics.png")

if __name__ == "__main__":
    train()
