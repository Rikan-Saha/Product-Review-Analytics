# backend/src/ingestion.py

import pandas as pd

def load_csv(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    return df

def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["review"])
    df["review"] = df["review"].str.strip().str.lower()
    return df