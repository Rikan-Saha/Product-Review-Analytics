import {

    Bar

} from "react-chartjs-2";

import {

    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Tooltip,
    Legend

} from "chart.js";

ChartJS.register(

    CategoryScale,
    LinearScale,
    BarElement,
    Tooltip,
    Legend
);

export default function BarChart({ data }) {

    return (

        <div className="chart-box">

            <h2 className="center-heading">
                Cluster Distribution
            </h2>

            <Bar
                data={{
                    labels: data.labels,

                    datasets: [
                        {
                            data: data.values,

                            backgroundColor: [

                                "#3b82f6",
                                "#10b981",
                                "#8b5cf6",
                                "#f59e0b",
                                "#ef4444"
                            ],

                            borderRadius: 10
                        }
                    ]
                }}

                options={{
                    responsive: true,

                    maintainAspectRatio: false,

                    plugins: {

                        legend: {

                            display: false
                        }
                    },

                    scales: {

                        y: {

                            beginAtZero: true
                        }
                    }
                }}
            />

        </div>
    );
}