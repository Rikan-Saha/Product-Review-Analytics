window.onload = function () {

    console.log("JS LOADED");

    console.log(dashboardData);

    // =====================================
    // GET CANVAS ELEMENT
    // =====================================

    const keywordCtx =
        document.getElementById("barChart");

    // =====================================
    // VALIDATION
    // =====================================

    if (!keywordCtx) {

        console.error(
            "Canvas element with id 'barChart' not found"
        );

        return;
    }

    if (
        !dashboardData ||
        !dashboardData.barChart
    ) {

        console.error(
            "dashboardData.barChart is missing"
        );

        return;
    }

    // =====================================
    // DONUT CHART
    // =====================================
    const chartList = [
        {
            id: "sentimentChart1",
            data: dashboardData.sentimentChart1
        },
        {
            id: "sentimentChart2",
            data: dashboardData.sentimentChart2
        },
        {
            id: "sentimentChart3",
            data: dashboardData.sentimentChart3
        }
    ];
    function createDoughnutChart(canvasId, chartData) {

        const ctx = document.getElementById(canvasId);

        if (!ctx) {
            console.error(`Canvas not found: ${canvasId}`);
            return;
        }

        if (!chartData) {
            console.error(`Data missing for: ${canvasId}`);
            return;
        }

        new Chart(ctx, {
            type: "doughnut",

            data: {
                labels: chartData.labels,

                datasets: [{
                    data: chartData.values,

                    backgroundColor: [
                        "#10b981",
                        "#f59e0b",
                        "#ef4444"
                    ]
                }]
            },
            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        display: false
                    },

                    tooltip: {

                        backgroundColor: "#111827",

                        titleColor: "#ffffff",

                        bodyColor: "#ffffff",

                        padding: 12
                    }
                }
            }
        });
    }

    chartList.forEach(chart => {
        createDoughnutChart(chart.id, chart.data);
    });
    // =====================================
    // BAR CHART
    // =====================================

    new Chart(keywordCtx, {

        type: "bar",

        data: {

            labels:
                dashboardData.barChart.labels,

            datasets: [{

                data:
                    dashboardData.barChart.values,

                backgroundColor:
                    dashboardData.barChart.labels.map(
                        (_, index) => {

                            const colors = [

                                "#3b82f6",
                                "#10b981",
                                "#8b5cf6",
                                "#f59e0b",
                                "#ef4444",
                                "#14b8a6",
                                "#ec4899"
                            ];

                            return colors[
                                index % colors.length
                            ];
                        }
                    ),

                borderRadius: 10,

                borderWidth: 1,

                borderColor: "#ffffff"
            }]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false
                },

                tooltip: {

                    backgroundColor: "#111827",

                    titleColor: "#ffffff",

                    bodyColor: "#ffffff",

                    padding: 12
                }
            },

            scales: {

                x: {

                    ticks: {

                        color: "#111827",

                        font: {

                            size: 14,

                            weight: "bold"
                        }
                    },

                    grid: {

                        display: false
                    }
                },

                y: {

                    beginAtZero: true,

                    ticks: {

                        color: "#111827",

                        font: {

                            size: 14
                        }
                    },

                    grid: {

                        color: "#d1d5db"
                    }
                }
            },

            animation: {

                duration: 1500
            }
        }
    });

};