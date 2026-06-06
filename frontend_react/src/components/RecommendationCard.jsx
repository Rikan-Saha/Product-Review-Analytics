export default function RecommendationCard({ rec }) {
  return (
    <div className="recommendation-card">

      <div className="recommendation-header">
        <h3>🚀 {rec.title}</h3>

        <span className="category-badge">
          {rec.category}
        </span>
      </div>

      <div className="recommendation-section">
        <h4>❗ Customer Problem</h4>
        <p>{rec.customer_problem}</p>
      </div>

      <div className="recommendation-section">
        <h4>✅ Proposed Solution</h4>
        <p>{rec.proposed_solution}</p>
      </div>

      {rec.expected_impact && (
        <div className="recommendation-section">
          <h4>📈 Expected Impact</h4>
          <p>{rec.expected_impact}</p>
        </div>
      )}

      <div className="recommendation-metrics">
        <span>Priority: {rec.priority_score}</span>

        {rec.business_value_score && (
          <span>Business Value: {rec.business_value_score}</span>
        )}

        {rec.confidence_score && (
          <span>
            Confidence: {(rec.confidence_score * 100).toFixed(0)}%
          </span>
        )}
      </div>

    </div>
  );
}