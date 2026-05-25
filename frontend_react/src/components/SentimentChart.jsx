import {

    Doughnut

} from "react-chartjs-2";

import {

    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend

} from "chart.js";

ChartJS.register(
    ArcElement,
    Tooltip,
    Legend
);

export default function SentimentChart({
    chart
}) {

    return (

        <div className="chart-box">

            <h2 className="center-heading">

                Sentiment Distribution -
                Cluster {parseInt(chart.clusterId)+1}

            </h2>

            <Doughnut
                data={{
                    labels: chart.labels,

                    datasets: [
                        {
                            data: chart.values,

                            backgroundColor: [

                                "#10b981",
                                "#f59e0b",
                                "#ef4444"
                            ]
                        }
                    ]
                }}
            />

        </div>
    );
}