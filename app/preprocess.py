# app/preprocess.py
import pandas as pd

def preprocess(df):
    df = df.drop(columns=["PassengerId", "Name", "Ticket", "Cabin"])
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Embarked"] = df["Embarked"].fillna("S")

    df["Sex"] = df["Sex"].map({"male": 0, "female": 1})
    df["Embarked"] = df["Embarked"].map({"S": 0, "C": 1, "Q": 2})

    return df
