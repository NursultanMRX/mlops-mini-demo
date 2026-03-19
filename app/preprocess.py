# app/preprocess.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess(df):
    # Categorical columns
    cat_cols = ["workclass","education","marital-status","occupation",
                "relationship","race","gender","native-country","salary"]
    
    for col in cat_cols:
        df[col] = df[col].fillna("Unknown")
        df[col] = LabelEncoder().fit_transform(df[col])
    
    # Fill missing numerical values if any
    num_cols = ["age","fnlwgt","education-num","capital-gain","capital-loss","hours-per-week"]
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())
    
    X = df.drop("salary", axis=1).values
    y = df["salary"].values
    
    return X, y
