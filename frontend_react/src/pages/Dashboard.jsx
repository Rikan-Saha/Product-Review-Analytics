import { useState } from "react";

import BarChart from "../components/BarChart";

import SentimentChart from "../components/SentimentChart";

import RecommendationCard from "../components/RecommendationCard";

import "../styles/dashboard.css";

export default function Dashboard() {

    // ==========================================
    // STATES
    // ==========================================

    const [file, setFile] =
        useState(null);

    const [clusters, setClusters] =
        useState(3);

    const [loading, setLoading] =
        useState(false);

    const [dashboardData, setDashboardData] =
        useState(null);

    const [recommendations, setRecommendations] =
        useState([]);

    // ==========================================
    // ANALYZE
    // ==========================================

    async function handleAnalyze() {

        if (!file) {

            alert("Please upload file");

            return;
        }

        setLoading(true);

        try {

            // ======================================
            // FORM DATA
            // ======================================

            const formData =
                new FormData();

            formData.append(
                "file",
                file
            );

            // ======================================
            // LOAD DATA
            // ======================================

            let response =
                await fetch(
                    "http://127.0.0.1:8000/load_data",
                    {
                        method: "POST",

                        body: formData
                    }
                );

            const loadedData =
                await response.json();

            // ======================================
            // CLEAN DATA
            // ======================================

            response =
                await fetch(
                    "http://127.0.0.1:8000/clean_ds",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify(
                            loadedData
                        )
                    }
                );

            const cleanedData =
                await response.json();

            // ======================================
            // CLUSTERING
            // ======================================

            response =
                await fetch(
                    "http://127.0.0.1:8000/cluster_summarizer",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            cleaned_data:
                                cleanedData,

                            num_clusters:
                                clusters
                        })
                    }
                );

            const clusterData =
                await response.json();

            // ======================================
            // RECOMMENDATIONS
            // ======================================

            response =
                await fetch(
                    "http://127.0.0.1:8000/generate_improvement_plans",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify(
                            clusterData.summaries
                        )
                    }
                );

            const recommendationData =
                await response.json();

            setRecommendations(
                recommendationData.suggestions
            );

            // ======================================
            // CHART DATA
            // ======================================

            const clusterCounts =
                clusterData.cluster_counts;

            const summarization =
                clusterData.summaries;

            const barChart = {

                labels:
                    Object.keys(clusterCounts)
                        .map(
                            x =>
                                `Cluster-${parseInt(x)+1}`
                        ),

                values:
                    Object.values(clusterCounts)
            };

            const sentimentCharts =
                Object.entries(summarization)
                    .map(
                        ([clusterId, clusterInfo]) => ({

                            clusterId,

                            labels:
                                Object.keys(
                                    clusterInfo.sentiment_dist
                                ),

                            values:
                                Object.values(
                                    clusterInfo.sentiment_dist
                                )
                        })
                    );

            setDashboardData({

                barChart,

                sentimentCharts
            });

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);
        }
    }

    // ==========================================
    // UI
    // ==========================================

    return (

        <div className="main-container">

            <div className="dashboard-title">
                AI Product Review Dashboard
            </div>

            {/* Upload Section */}

            <div className="chart-box">

                <h2>
                    Upload Review Dataset
                </h2>

                <input
                    type="file"

                    accept=".csv,.xlsx"

                    onChange={(e) =>
                        setFile(
                            e.target.files[0]
                        )
                    }
                />

                <br />
                <br />

                <label>

                    Number of Clusters:
                    {clusters}

                </label>

                <br />

                <input
                    type="range"

                    min="2"

                    max="20"

                    value={clusters}

                    onChange={(e) =>
                        setClusters(
                            e.target.value
                        )
                    }
                />

                <br />
                <br />

                <button
                    onClick={handleAnalyze}
                >
                    Analyze Reviews
                </button>

            </div>

            {/* Loading */}

            {loading && (

                <h2>
                    Processing Reviews...
                </h2>
            )}

            {/* Dashboard */}

            {dashboardData && (

                <>
                    <BarChart
                        data={dashboardData.barChart}
                    />

                    <div className="charts">

                        {dashboardData.sentimentCharts.map(
                            (chart, idx) => (

                                <SentimentChart
                                    key={idx}
                                    chart={chart}
                                />
                            )
                        )}

                    </div>

                    <div className="recommendations-section">

                        {recommendations.map(
                            (rec, idx) => (

                                <RecommendationCard
                                    key={idx}
                                    rec={rec}
                                />
                            )
                        )}

                    </div>
                </>
            )}

        </div>
    );
}