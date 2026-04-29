# # backend/src/clustering.py

# from sklearn.cluster import KMeans

# def cluster_reviews(embeddings, k=3):
#     model = KMeans(n_clusters=k, random_state=42)
#     labels = model.fit_predict(embeddings)
#     return labels

from sklearn.cluster import KMeans
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from concurrent.futures import ThreadPoolExecutor

STOPWORDS = set(["the","and","is","in","on","a","an","to","for","of","with","it","this","that"])

def cluster_embeddings(embeddings: np.ndarray, n_clusters: int = 3):
    """Simple KMeans clustering placeholder. Replace with HDBSCAN/UMAP+HDBSCAN for better clusters."""
    if embeddings.shape[0] < n_clusters:
        n_clusters = max(1, embeddings.shape[0])
    km = KMeans(n_clusters=n_clusters, random_state=42)
    labels = km.fit_predict(embeddings)
    return labels

def _top_terms(texts, n=5):
    vec = CountVectorizer(stop_words=list(STOPWORDS)).fit(texts)
    X = vec.transform(texts)
    sums = np.asarray(X.sum(axis=0)).ravel()
    terms = np.array(vec.get_feature_names_out())
    top_idx = np.argsort(sums)[::-1][:n]
    return [terms[i] for i in top_idx if sums[i] > 0]

def _run_kmeans(embeddings: np.ndarray, n_clusters: int):
    """Internal function to run KMeans"""
    if embeddings.shape[0] < n_clusters:
        n_clusters = max(1, embeddings.shape[0])

    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = km.fit_predict(embeddings)

    return labels


def cluster_embeddings_thread(embeddings: np.ndarray, n_clusters: int = 3):
    """Run KMeans using ThreadPoolExecutor"""

    with ThreadPoolExecutor(max_workers=10) as executor:
        future = executor.submit(_run_kmeans, embeddings, n_clusters)
        labels = future.result()

    return labels