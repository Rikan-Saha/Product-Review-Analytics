import re

def _is_spam(text: str) -> bool:
    if not isinstance(text, str):
        return True
    t = text.lower()
    if len(t) < 8:
        return True
    if re.search(r"buy now|free money|click here|http|www\.|!!!|\$\$\$", t):
        return True
    # too many repeated characters
    if re.search(r"(.)\1{5,}", t):
        return True
    return False

def _classify_sentiment(text):
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


# def _classify_sentiment(df):
#     df["sentiment"] = df["review"].apply(analyze_sentiment)
#     return df