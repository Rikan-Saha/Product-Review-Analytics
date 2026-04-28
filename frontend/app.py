import streamlit as st
import requests
import plotly.express as px
import pandas as pd


LOAD_DATA_URL = "http://127.0.0.1:8000/load_data"
CLEAN_DS_URL = "http://127.0.0.1:8000/clean_ds"
CLUSTERING_URL = "http://127.0.0.1:8000/cluster_summarizer"
GENERATE_IMPR_URL = "http://127.0.0.1:8000/generate_improvement_plans"

st.set_page_config(page_title="Review Analyzer", layout="wide")

st.title("📊 AI Product Review Analyzer")

uploaded_file = st.file_uploader("Upload CSV with 'review' column", type=["csv", "xlsx"])

if uploaded_file:
    if st.button("Analyze Reviews"):

        with st.spinner("Processing..."):
            response = requests.post(
                LOAD_DATA_URL,
                files={"file": uploaded_file}
            )
            print(pd.DataFrame(response.json()))
            loaded_data = response.json()

            response = requests.post(
                CLEAN_DS_URL,
                json = loaded_data
            )
            print(pd.DataFrame(response.json()))
            cleaned_data = response.json()

            # texts = pd.DataFrame(cleaned_data)["_text"].tolist()
            # response = requests.post(
            #     EMBEDDING_URL,
            #     json = texts
            # )
            # embed_txt = response.json()

            response = requests.post(
                CLUSTERING_URL,
                json = cleaned_data
            )
            summarization = response.json()

            response = requests.post(
                GENERATE_IMPR_URL,
                json = summarization
            )
            
            print(response.json())
            












        # if response.status_code == 200:
        #     data = response.json()

        #     # ---------------------------
        #     # 📊 INTERACTIVE CHART
        #     # ---------------------------
        #     st.subheader("📊 Sentiment Distribution")

        #     sentiments = data["sentiment_counts"]

        #     df_chart = pd.DataFrame({
        #         "Sentiment": list(sentiments.keys()),
        #         "Count": list(sentiments.values())
        #     })

        #     fig = px.bar(
        #         df_chart,
        #         x="Sentiment",
        #         y="Count",
        #         # text="Count",
        #         title="Sentiment Overview",
        #     )

        #     st.plotly_chart(fig, use_container_width=True)

        #     # ---------------------------
        #     # 💡 RECOMMENDATIONS
        #     # ---------------------------
        #     st.subheader("💡 Product Improvement Insights")

        #     for rec in data["recommendations"]:
        #         st.success(rec)

        # else:
        #     st.error("Error processing file")