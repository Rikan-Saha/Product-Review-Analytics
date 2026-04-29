# backend/main.py

from fastapi import FastAPI, UploadFile, File

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any

# from backend.src.ingestion import clean_reviews
from backend.src.sentiment import _is_spam, _classify_sentiment
from backend.src.embedding import embed_texts
from backend.src.clustering import _top_terms, cluster_embeddings_thread # cluster_embeddings
from backend.src.agent import propose_improvements
from backend.src.load_data import load_csv, load_xlsx

app = FastAPI()


@app.get("/")
def home():
    return {"message": "API Running"}

@app.post("/load_data")
def load_data(file: UploadFile = File(...)) -> List[Dict[str, Any]]:
    
    file_extension = Path(file.filename).suffix.lower()
    if file_extension == ".csv":
        df = load_csv(file.file)
    elif file_extension == ".xlsx":
        df = load_xlsx(file.file)
    else:
        return [{"error": "Unsupported file format"}]

    return df.to_dict(orient="records")

@app.post("/clean_ds")
def clean_ds(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

    df = pd.DataFrame(data)

    df = df.copy()
    text_col = None

    for c in df.columns:
        if c.lower() in ("text", "review", "comment", "message"):
            text_col = c
            break

    if text_col is None:
        text_col = df.columns[0]

    df["_text"] = df[text_col].astype(str)
    df["is_spam"] = df["_text"].apply(_is_spam)
    df_clean = df[~df["is_spam"]].reset_index(drop=True)
    df_clean["sentiment"] = df_clean["_text"].apply(_classify_sentiment)

    return df_clean.to_dict(orient="records")

@app.post("/cluster_summarizer")
def cluster_summarizer(cleaned_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    cleaned_df = pd.DataFrame(cleaned_data)
    texts = cleaned_df["_text"].tolist()
    embeddings = embed_texts(texts)
    labels = cluster_embeddings_thread(embeddings) # cluster_embeddings(embeddings)
    cleaned_df["cluster"] = labels
    
    # print("cleaned_df:", cleaned_df)
    cluster_counts = cleaned_df["cluster"].value_counts().to_dict()

    summaries = {}
    for lbl in sorted(cleaned_df["cluster"].unique()):
        rows = cleaned_df[cleaned_df["cluster"] == lbl]
        samples = rows["_text"].tolist()[:3]
        top_terms = _top_terms(rows["_text"].tolist(), n=5)
        summaries[int(lbl)] = {
            "count": int(len(rows)),
            "top_terms": top_terms,
            "samples": samples,
            "sentiment_dist": rows["sentiment"].value_counts(normalize=True).to_dict(),
        }
    return {"cluster_counts": cluster_counts, "summaries": summaries}

@app.post("/generate_improvement_plans")
def generate_improvement_plans(summarization: Dict[int, Dict[str, Any]]):
    print(summarization, "Summ")
    cluster_summaries = []
    for lbl, meta in summarization.items():
        cluster_summaries.append(f"Cluster {lbl}: count={meta['count']}; top_terms={', '.join(meta['top_terms'])}; samples={meta['samples']}")
    cluster_summaries_text = "\n".join(cluster_summaries)
    suggestions = propose_improvements(cluster_summaries_text)

    return {"summarization": summarization, "suggestions": suggestions}


@app.post("/embed_text")
def embed_text(texts: List[str]) -> List[List[float]]:
    print(texts)
    embeddings = embed_texts(texts)
    print(embeddings, embeddings.shape)
    return embeddings.tolist()

# @app.post("/analyze_csv")
# async def analyze_csv(file: UploadFile = File(...)):
    
#     df = pd.read_csv(file.file)

#     # Step 1: Clean
#     df = clean_reviews(df)

#     # Step 2: Sentiment
#     df = apply_sentiment(df)

#     # Step 3: Embedding
#     embeddings = generate_embeddings(df["review"])

#     # Step 4: Clustering
#     df["cluster"] = cluster_reviews(embeddings)

#     # Step 5: Recommendations
#     recommendations = generate_recommendations(df)

#     # Sentiment counts
#     sentiment_counts = df["sentiment"].value_counts().to_dict()

#     return {
#         "sentiment_counts": sentiment_counts,
#         "recommendations": recommendations
#     }