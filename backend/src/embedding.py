# backend/src/embedding.py

from sklearn.feature_extraction.text import TfidfVectorizer

def generate_embeddings(texts):
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(texts)
    return X