export default function RecommendationCard({
    rec
}) {

    return (

        <div className="recommendation-card">

            <h3>
                🚀 {rec.action}
            </h3>

            <div className="recommendation-info">

                {rec.rationale}

            </div>

        </div>
    );
}