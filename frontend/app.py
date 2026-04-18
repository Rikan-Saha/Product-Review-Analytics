import streamlit as st
import requests
import plotly.express as px
import pandas as pd

API_URL = "http://127.0.0.1:8000/analyze_csv"

st.set_page_config(page_title="Review Analyzer", layout="wide")

st.title("📊 AI Product Review Analyzer")

uploaded_file = st.file_uploader("Upload CSV with 'review' column", type=["csv"])

if uploaded_file:
    if st.button("Analyze Reviews"):

        with st.spinner("Processing..."):
            response = requests.post(
                API_URL,
                files={"file": uploaded_file}
            )

        if response.status_code == 200:
            data = response.json()

            # ---------------------------
            # 📊 INTERACTIVE CHART
            # ---------------------------
            st.subheader("📊 Sentiment Distribution")

            sentiments = data["sentiment_counts"]

            df_chart = pd.DataFrame({
                "Sentiment": list(sentiments.keys()),
                "Count": list(sentiments.values())
            })

            fig = px.bar(
                df_chart,
                x="Sentiment",
                y="Count",
                # text="Count",
                title="Sentiment Overview",
            )

            st.plotly_chart(fig, use_container_width=True)

            # ---------------------------
            # 💡 RECOMMENDATIONS
            # ---------------------------
            st.subheader("💡 Product Improvement Insights")

            for rec in data["recommendations"]:
                st.success(rec)

        else:
            st.error("Error processing file")