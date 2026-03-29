def analyze_sentiment(text):
    text = text.lower()

    if "not bad" in text or "not worst" in text:
        return "positive"

    positive = ["good", "great", "excellent", "amazing", "love", "nice"]
    negative = ["bad", "worst", "poor", "terrible", "hate", "broken", "damaged"]

    if any(word in text for word in positive):
        return "positive"
    elif any(word in text for word in negative):
        return "negative"
    else:
        return "neutral"


def apply_sentiment(df):
    df["sentiment"] = df["review"].apply(analyze_sentiment)
    return df