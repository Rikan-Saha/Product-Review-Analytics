import streamlit as st
import requests
import pandas as pd
import json
from pathlib import Path
import streamlit.components.v1 as components

# ==========================================
# API URLS
# ==========================================

LOAD_DATA_URL = "http://127.0.0.1:8000/load_data"
CLEAN_DS_URL = "http://127.0.0.1:8000/clean_ds"
CLUSTERING_URL = "http://127.0.0.1:8000/cluster_summarizer"
GENERATE_IMPR_URL = "http://127.0.0.1:8000/generate_improvement_plans"

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Review Analyzer",
    layout="wide"
)

st.title("📊 AI Product Review Analyzer")

# ==========================================
# LOAD CSS
# ==========================================

css_path = Path("frontend/style.css")

css = ""

if css_path.exists():

    css = css_path.read_text(
        encoding="utf-8"
    )

else:

    st.error("frontend/style.css not found")

# ==========================================
# LOAD JAVASCRIPT
# ==========================================

js_path = Path("frontend/dashboard.js")

js = ""

if js_path.exists():

    js = js_path.read_text(
        encoding="utf-8"
    )

else:

    st.error("frontend/dashboard.js not found")

# ==========================================
# FILE UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "Upload CSV with 'review' column",
    type=["csv", "xlsx"]
)

# ==========================================
# PROCESS
# ==========================================

if uploaded_file:

    if st.button("Analyze Reviews"):

        with st.spinner("Processing Reviews..."):

            # ==========================================
            # LOAD DATA
            # ==========================================

            response = requests.post(
                LOAD_DATA_URL,
                files={
                    "file": uploaded_file
                }
            )

            loaded_data = response.json()

            # ==========================================
            # CLEAN DATA
            # ==========================================

            response = requests.post(
                CLEAN_DS_URL,
                json=loaded_data
            )

            cleaned_data = response.json()

            # ==========================================
            # CLUSTERING + SUMMARIZATION
            # ==========================================

            response = requests.post(
                CLUSTERING_URL,
                json=cleaned_data
            )

            data = response.json()

            summarization = data["summaries"]

            cluster_counts = data["cluster_counts"]

            # ==========================================
            # CHART DATAFRAME
            # ==========================================

            df_chart = pd.DataFrame(
                list(cluster_counts.items()),
                columns=[
                    "Cluster",
                    "Count"
                ]
            ).sort_values("Cluster")

            # ==========================================
            # DASHBOARD DATA
            # ==========================================
            sentimentChart1= {
                    "labels": list(summarization["0"]["sentiment_dist"].keys()),
                    "values": list(summarization["0"]["sentiment_dist"].values())}
            print(sentimentChart1, "sentimentChart1")
            dashboard_data = {

                "barChart": {
                    "labels": df_chart["Cluster"].tolist(),
                    "values": df_chart["Count"].tolist()
                },

                "sentimentChart1": {
                    "labels": list(summarization["0"]["sentiment_dist"].keys()),
                    "values": list(summarization["0"]["sentiment_dist"].values())
                },
                "sentimentChart2": {
                    "labels": list(summarization["1"]["sentiment_dist"].keys()),
                    "values": list(summarization["1"]["sentiment_dist"].values())
                },
                "sentimentChart3": {
                    "labels": list(summarization["2"]["sentiment_dist"].keys()),
                    "values": list(summarization["2"]["sentiment_dist"].values())
                }
            }

            dashboard_json = json.dumps(
                dashboard_data
            )

            # ==========================================
            # RECOMMENDATIONS
            # ==========================================

            response = requests.post(
                GENERATE_IMPR_URL,
                json=summarization
            )

            recommendation_data = response.json()

            recommendations = recommendation_data[
                "suggestions"
            ]

            

            print(summarization, "recomendations")
            # ==========================================
            # HTML START
            # ==========================================

            html_code_1 = f"""

            <!DOCTYPE html>

            <html>

            <head>

            <meta charset="UTF-8">

            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

            <style>

            {css}

            </style>

            </head>

            <body>

            <div class="main-container">

                <div class="dashboard-title">
                    AI Product Review Dashboard
                </div>

                <div class="chart-box">

                    <h2>
                        Cluster Distribution
                    </h2>

                    <canvas id="barChart"></canvas>

                </div>

                <br> </br>

                <div class="charts">

                    <div class="chart-box">
                        <h2>Sentiment Distribution</h2>
                        <canvas id="sentimentChart1"></canvas>
                    </div>

                    <div class="chart-box">
                        <h2>Sentiment Distribution</h2>
                        <canvas id="sentimentChart2"></canvas>
                    </div>

                    <div class="chart-box">
                        <h2>Sentiment Distribution</h2>
                        <canvas id="sentimentChart3"></canvas>
                    </div>
                </div>
            """
            # ==========================================
            # HTML END
            # ==========================================

            html_code_1 += f"""

                </div>

            </div>

            <script>

            const dashboardData =
                {dashboard_json};

            </script>

            <script>

            {js}

            </script>

            </body>

            </html>

            """

            # ==========================================
            # RENDER HTML
            # ==========================================

            components.html(
                html_code_1,
                height=1000,
                scrolling=True
            )
            # ==========================================
            # DYNAMIC RECOMMENDATION CARDS
            # ==========================================

            html_code_2 = f"""
            <!DOCTYPE html>

            <html>

            <head>

            <meta charset="UTF-8">

            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

            <style>

            {css}

            </style>

            </head>

            <body>

            """
            for rec in recommendations:

                priority = rec["priority"]

                priority_class = ""

                if priority == 1:

                    priority_class = "high-priority"

                elif priority == 2:

                    priority_class = "medium-priority"

                else:

                    priority_class = "low-priority"

                html_code_2 += f"""
                <div class="recommendations-section">
                    <div class="recommendation-card">

                        <h3>
                            🚀 {rec['action']}
                        </h3>

                        <div class="priority {priority_class}">

                            Priority: {rec['priority']}

                        </div>

                        <div class="recommendation-info">

                            {rec['rationale']}

                        </div>
                    </div>
                </div>
                </body>
                </html>
                """
            components.html(
                html_code_2,
                height=1600,
                scrolling=True
            )