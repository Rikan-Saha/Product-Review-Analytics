# 📊 AI Product Review Analytics System

AI-powered product review analytics platform using React, FastAPI, NLP, Sentence Transformers, and clustering techniques to analyze customer reviews and generate actionable product insights.

---

# 🚀 Project Overview

This project builds an end-to-end AI analytics pipeline to process large-scale product reviews and transform raw customer feedback into meaningful business intelligence.

The system integrates:

- React-based interactive frontend
- FastAPI backend APIs
- NLP & Machine Learning techniques
- Sentence Transformer embeddings
- K-Means clustering
- AI-driven recommendation generation

The platform enables organizations to automatically discover customer pain points, sentiment trends, and actionable product improvement opportunities.

---

# 🎯 Business Objective

To analyze customer reviews and automatically:

- Classify sentiment (Positive, Negative, Neutral)
- Detect spam reviews
- Identify recurring product issues
- Cluster customer pain points
- Generate AI-powered improvement recommendations
- Provide interactive analytics dashboards

---

# 🏗️ Project Architecture

```text
User Upload (CSV/XLSX)
          ↓
React Frontend Dashboard
          ↓
FastAPI REST APIs
          ↓
Data Cleaning & NLP Processing
          ↓
Sentiment Analysis
          ↓
Sentence Transformer Embeddings
          ↓
K-Means Clustering
          ↓
AI Recommendation Engine
          ↓
Interactive Visualization Dashboard
```

---

# 📂 Project Structure

```text
AI-Product-Review-System/
│
├── backend/
│   ├── main.py
│   │
│   └── src/
│       ├── load_data.py
│       ├── sentiment.py
│       ├── embedding.py
│       ├── clustering.py
│       └── agent.py
│
├── frontend_react/
│   │
│   ├── public/
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── BarChart.jsx
│   │   │   ├── SentimentChart.jsx
│   │   │   └── RecommendationCard.jsx
│   │   │
│   │   ├── pages/
│   │   │   └── Dashboard.jsx
│   │   │
│   │   ├── styles/
│   │   │   └── dashboard.css
│   │   │
│   │   ├── App.js
│   │   └── index.js
│   │
│   └── package.json
│
├── images/
│
└── README.md
```

---

# 🔥 Key Features

- CSV/XLSX review ingestion
- Automated data cleaning pipeline
- Spam review detection
- NLP-based sentiment analysis
- Sentence Transformer embeddings
- K-Means clustering for customer issue grouping
- AI-generated improvement recommendations
- Dynamic React dashboard
- Interactive charts using Chart.js
- REST API architecture using FastAPI
- Modular and scalable frontend/backend design

---

# 🖥️ Dashboard Screenshots

## File Upload and No. of Clusters

![Dashboard](https://github.com/Rikan-Saha/Product-Review-Analytics/blob/main/images/File_upload.png)

---

## Cluster Analytics

![Charts](https://github.com/Rikan-Saha/Product-Review-Analytics/blob/main/images/Dashboard.png)

---

## AI Recommendations: Below are plceholders.

![Recommendations](https://github.com/Rikan-Saha/Product-Review-Analytics/blob/main/images/Recommendation.png)

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Rikan-Saha/Product-Review-Analytics.git

cd AI-Product-Review-System
```

---

# ⚙️ Backend Setup

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv env1

env1\Scripts\activate
```

---

## 3️⃣ Install Backend Dependencies

```bash
pip install fastapi uvicorn pandas scikit-learn sentence-transformers openpyxl python-multipart
```

---

## 4️⃣ Run FastAPI Backend

```bash
uvicorn backend.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

---

# ⚙️ Frontend Setup

## 5️⃣ Navigate to React Frontend

```bash
cd frontend_react
```

---

## 6️⃣ Install Frontend Dependencies

```bash
npm install
```

---

## 7️⃣ Install Chart.js Packages

```bash
npm install chart.js react-chartjs-2
```

---

## 8️⃣ Run React Frontend

```bash
npm start
```

Frontend runs at:

```text
http://localhost:3000
```

---

# 🧠 NLP & AI Workflow

## Step 1 — Data Ingestion
- Upload CSV/XLSX review dataset

## Step 2 — Data Cleaning
- Remove spam reviews
- Normalize review text

## Step 3 — Sentiment Analysis
- Positive
- Neutral
- Negative classification

## Step 4 — Text Embedding
- Generate semantic embeddings using Sentence Transformers

## Step 5 — Clustering
- Group similar customer pain points using K-Means clustering

## Step 6 — AI Recommendation Generation
- Generate actionable product improvement suggestions

## Step 7 — Visualization
- Display insights in interactive React dashboards

---

# 💻 Tech Stack

## Frontend
- React
- JavaScript
- CSS
- Chart.js

## Backend
- FastAPI
- Python

## Machine Learning / NLP
- Scikit-Learn
- Sentence Transformers
- K-Means Clustering
- Pandas

---

# 💼 Business Impact

- Identifies major customer pain points automatically
- Enables data-driven product improvement
- Improves customer satisfaction analysis
- Accelerates review intelligence workflows
- Reduces manual review analysis effort
- Provides actionable AI-driven recommendations

---

# 🚀 Future Enhancements

- Authentication & Role-Based Access
- Cloud deployment (AWS / Azure)
- Advanced LLM summarization
- Real-time review streaming
- Vector database integration
- RAG-based review intelligence system
- Advanced analytics & forecasting
- Exportable PDF/Excel reports

---

# 📌 Resume Project Summary

AI-powered product review analytics system using React, FastAPI, NLP, Sentence Transformers, and K-Means clustering to analyze customer reviews, identify pain points, perform sentiment analysis, and generate AI-driven product improvement recommendations through interactive dashboards.

---

# 🙏 Acknowledgment

Thank you for reviewing this project.
