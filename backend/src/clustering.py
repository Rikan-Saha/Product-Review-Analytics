# backend/src/clustering.py

from sklearn.cluster import KMeans

def cluster_reviews(embeddings, k=3):
    model = KMeans(n_clusters=k, random_state=42)
    labels = model.fit_predict(embeddings)
    return labels