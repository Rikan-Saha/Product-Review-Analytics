# backend/main.py

from fastapi import FastAPI, UploadFile, File
import pandas as pd

from backend.src.ingestion import load_csv, clean_reviews
from backend.src.sentiment import apply_sentiment
from backend.src.embedding import generate_embeddings
from backend.src.clustering import cluster_reviews
from backend.src.agent import generate_recommendations

app = FastAPI()


@app.get("/")
def home():
    return {"message": "API Running 🚀"}


@app.post("/analyze_csv")
async def analyze_csv(file: UploadFile = File(...)):
    
    df = pd.read_csv(file.file)

    # Step 1: Clean
    df = clean_reviews(df)

    # Step 2: Sentiment
    df = apply_sentiment(df)

    # Step 3: Embedding
    embeddings = generate_embeddings(df["review"])

    # Step 4: Clustering
    df["cluster"] = cluster_reviews(embeddings)

    # Step 5: Recommendations
    recommendations = generate_recommendations(df)

    # Sentiment counts
    sentiment_counts = df["sentiment"].value_counts().to_dict()

    return {
        "sentiment_counts": sentiment_counts,
        "recommendations": recommendations
    }