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

    no_of_clusters = st.slider("How many cluster you want?", 0, 200, 3)
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
                json={
                    "cleaned_data": cleaned_data,
                    "num_clusters": no_of_clusters
                }
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
            sentiment_distribution = {}
            dashboard_data = {

                "barChart": {
                    "labels": [f"Cluster-{int(i)+1}" for i in df_chart["Cluster"].tolist()],
                    "values": df_chart["Count"].tolist()
                },
            }

            for idx, (cluster_id, cluster_data) in enumerate(summarization.items(), start=1):

                dashboard_data[f"sentimentChart{idx}"] = {

                    "labels": list(
                        cluster_data["sentiment_dist"].keys()
                    ),

                    "values": list(
                        cluster_data["sentiment_dist"].values()
                    )
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

                    <h2 class="center-heading">
                        Cluster Distribution
                    </h2>

                    <canvas id="barChart"></canvas>

                </div>

                <br> </br>
            """
            html_code_1 += """
            <div class="charts">
            """

            for idx, cluster_id in enumerate(summarization.keys(), start=1):

                html_code_1 += f"""
                <div class="chart-box">

                    <h2 class="center-heading">
                        Sentiment Distribution - Cluster {int(cluster_id) + 1}
                    </h2>

                    <canvas id="sentimentChart{idx}"></canvas>

                </div>
                """

            html_code_1 += """
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