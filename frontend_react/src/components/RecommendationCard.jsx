export default function RecommendationCard({
    rec
}) {

    return (

        <div className="recommendation-card">

            <h3>
                🚀 {rec.customer_problem}
            </h3>

            <div className="recommendation-info">

                {rec.proposed_solution}

            </div>

        </div>
    );
}