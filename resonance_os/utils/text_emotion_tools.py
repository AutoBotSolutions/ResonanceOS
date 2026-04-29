from textblob import TextBlob

def sentiment_score(text: str) -> float:
    return TextBlob(text).sentiment.polarity

def emotion_intensity(text: str) -> float:
    return abs(TextBlob(text).sentiment.polarity)
