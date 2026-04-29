# 📊 AI Product Review Analytics System

---

## 🚀 Project Overview

This project builds an end-to-end analytics pipeline to analyze product reviews and generate actionable insights using Natural Language Processing (NLP) techniques.

The system integrates **FastAPI (backend)**, **Streamlit (frontend)**, and **Machine Learning (NLP & Clustering)** to transform raw customer feedback into meaningful business insights.

---

## 🎯 Business Objective

To analyze customer reviews and automatically:

- Classify sentiment (Positive, Negative, Neutral)
- Identify recurring product issues
- Generate product improvement strategies
- Provide interactive visualization for better decision-making

---

## 🏗️ Project Architecture

```
User Upload (CSV)
        ↓
Data Ingestion & Cleaning (Python)
        ↓
Sentiment Analysis
        ↓
Text Embedding (TF-IDF)
        ↓
Clustering (KMeans)
        ↓
Insight Generation (AI Agent)
        ↓
FastAPI Backend
        ↓
Streamlit Dashboard
```

---

## 📂 Project Structure

```
Project3/
│
├── backend/
│ ├── main.py
│ └── src/
│       ├── load_data.py
│       ├── sentiment.py
│       ├── embedding.py
│       ├── clustering.py
│       └── agent.py
│
├── frontend/
│ └── app.py
│
└── README.md
```
---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Rikan-Saha/Product-Review-Analytics.git
cd Project3
```
### 2️⃣ Create Virtual Environment
``` 
python -m venv env1
env1\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies
```
pip install fastapi uvicorn pandas scikit-learn streamlit requests plotly
```

### ▶️ How to Run the Project
```
Step 1: Run Backend (FastAPI)
python -m uvicorn backend.main:app --reload

Backend will run at:
http://127.0.0.1:8000

Step 2: Run Frontend (Streamlit)

Open a new terminal and run:

streamlit run frontend/app.py

Frontend will open at:
http://localhost:8501

```

## 🔥 Key Highlights

* End-to-end pipeline from raw review data to interactive dashboard  
* Automated ingestion, sentiment analysis, clustering, and insight generation  
* Integration of ML outputs into a user-friendly Streamlit application  
* Interactive and intuitive visualization using Plotly  

---

## 💼 Business Impact

* Identifies key customer pain points from large-scale reviews  
* Helps improve product quality and customer experience  
* Enables data-driven product and business decisions  
* Provides actionable insights for continuous product improvement  

---

## 🚀 Future Enhancements

* Integrate transformer-based sentiment models (BERT, RoBERTa)
* Use LLMs for advanced and contextual recommendations  
* Store results in a database (PostgreSQL / MongoDB)  
* Deploy application on cloud platforms (AWS / Azure)  
* Add real-time review streaming and monitoring  

---
## 🙏 Acknowledgment

Thank you for reviewing this project.

---