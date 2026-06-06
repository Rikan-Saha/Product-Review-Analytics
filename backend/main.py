from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import pandas as pd

from pathlib import Path

from typing import List, Dict, Any

# ==========================================
# IMPORTS
# ==========================================

from backend.src.sentiment import (_is_spam, _classify_sentiment)

from backend.src.embedding import (embed_texts)

from backend.src.clustering import (_top_terms,cluster_embeddings_thread)

from backend.src.agent import (propose_improvements)

from backend.src.load_data import (load_csv,load_xlsx)

# ==========================================
# FASTAPI APP
# ==========================================

app = FastAPI(title="AI Product Review Analytics API")

# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# ==========================================
# ROOT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "AI Product Review Analytics API Running"
    }

# ==========================================
# LOAD DATA
# ==========================================

@app.post("/load_data")
def load_data(file: UploadFile = File(...)) -> List[Dict[str, Any]]:

    file_extension = (Path(file.filename).suffix.lower())

    # ======================================
    # CSV
    # ======================================

    if file_extension == ".csv":
        df = load_csv(file.file)

    # ======================================
    # XLSX
    # ======================================

    elif file_extension == ".xlsx":
        df = load_xlsx(file.file)

    # ======================================
    # INVALID
    # ======================================

    else:

        return [
            {
                "error":"Unsupported file format"
            }
        ]

    return df.to_dict(orient="records")

# ==========================================
# CLEAN DATASET
# ==========================================

@app.post("/clean_ds")
def clean_ds(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

    df = pd.DataFrame(data)

    # ======================================
    # FIND TEXT COLUMN
    # ======================================

    text_col = None

    for c in df.columns:

        if c.lower() in (
            "text",
            "review",
            "comment",
            "message"
        ):

            text_col = c

            break

    # ======================================
    # DEFAULT COLUMN
    # ======================================

    if text_col is None:

        text_col = df.columns[0]

    # ======================================
    # CLEANING
    # ======================================

    df["_text"] = (df[text_col].astype(str))

    # ======================================
    # SPAM DETECTION
    # ======================================

    df["is_spam"] = (df["_text"].apply(_is_spam))

    # ======================================
    # REMOVE SPAM
    # ======================================

    df_clean = (df[~df["is_spam"]].reset_index(drop=True))

    # ======================================
    # SENTIMENT
    # ======================================

    df_clean["sentiment"] = (df_clean["_text"].apply(_classify_sentiment))

    return df_clean.to_dict(orient="records")

# ==========================================
# REQUEST MODEL
# ==========================================

class ClusterRequest(BaseModel):

    cleaned_data:List[Dict[str, Any]]

    num_clusters:int

# ==========================================
# CLUSTERING
# ==========================================

@app.post("/cluster_summarizer")
def cluster_summarizer(request: ClusterRequest) -> Dict[str, Any]:

    cleaned_df = pd.DataFrame(request.cleaned_data)

    no_of_clusters = (request.num_clusters)

    # ======================================
    # TEXTS
    # ======================================

    texts = (cleaned_df["_text"].tolist())

    # ======================================
    # EMBEDDINGS
    # ======================================

    embeddings = embed_texts(texts)

    # ======================================
    # CLUSTERING
    # ======================================

    labels = cluster_embeddings_thread(embeddings,no_of_clusters)

    cleaned_df["cluster"] = labels

    # ======================================
    # CLUSTER COUNTS
    # ======================================

    cluster_counts = (cleaned_df["cluster"].value_counts().to_dict())

    # ======================================
    # SUMMARIES
    # ======================================

    summaries = {}

    for lbl in sorted(cleaned_df["cluster"].unique()):

        rows = cleaned_df[cleaned_df["cluster"] == lbl]

        samples = (rows["_text"].tolist()[:3])

        top_terms = _top_terms(rows["_text"].tolist(),n=5)

        summaries[int(lbl)] = {
            "count": int(len(rows)),
            "top_terms": top_terms,
            "samples": samples,
            "sentiment_dist": rows["sentiment"].value_counts(normalize=True).to_dict()
        }

    return {
        "cluster_counts": cluster_counts,
        "summaries": summaries
    }

# ==========================================
# IMPROVEMENT PLANS
# ==========================================

@app.post("/generate_improvement_plans")
def generate_improvement_plans(summarization:Dict[int, Dict[str, Any]]):

    suggestions = []

    for lbl, meta in (summarization.items()):

        details = "\n\n".join(meta['samples'])
        suggestions += propose_improvements(details)
    

    print("suggestions: ", suggestions)
    return {
        "summarization": summarization,
        "suggestions": suggestions
    }

# ==========================================
# EMBEDDING API
# ==========================================

@app.post("/embed_text")
def embed_text(
    texts: List[str]
) -> List[List[float]]:

    embeddings = embed_texts(texts)

    return embeddings.tolist()