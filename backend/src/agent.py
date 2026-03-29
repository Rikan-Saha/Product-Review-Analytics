## Currently, providing the non-AI solutions 

def generate_recommendations(df):
    recommendations = []

    negative_reviews = df[df["sentiment"] == "negative"]["review"]

    issues = {
        "quality": ["bad quality", "poor quality", "thin"],
        "packaging": ["damaged", "box", "packing"],
        "broken": ["broken", "defect"],
        "performance": ["not working", "slow", "leaking"]
    }

    found_issues = {key: 0 for key in issues}

    for review in negative_reviews:
        for issue, keywords in issues.items():
            if any(word in review for word in keywords):
                found_issues[issue] += 1

    # Generate smart recommendations
    if found_issues["quality"] > 0:
        recommendations.append("Improve product quality and material durability")

    if found_issues["packaging"] > 0:
        recommendations.append("Enhance packaging to prevent damage during delivery")

    if found_issues["broken"] > 0:
        recommendations.append("Improve quality checks to avoid defective items")

    if found_issues["performance"] > 0:
        recommendations.append("Improve product performance and reliability")

    if not recommendations:
        recommendations.append("Overall product feedback is positive. Maintain quality.")

    return recommendations