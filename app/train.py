from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib
import json

def train():
    data = load_iris()
    X, y = data.data, data.target

    model = RandomForestClassifier()
    model.fit(X, y)

    acc = model.score(X, y)

    # save model
    joblib.dump(model, "app/model.pkl")

    # save metrics
    with open("metrics.json", "w") as f:
        json.dump({"accuracy": acc}, f)

if __name__ == "__main__":
    train()
