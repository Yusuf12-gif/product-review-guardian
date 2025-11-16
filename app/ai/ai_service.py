# app/ai/ai_service.py

async def analyze_review_text(text: str) -> dict:
    """
    Dummy AI analysis.
    You can plug a real model here later.
    """
    # Fake sentiment calculation based on length
    length = len(text)
    sentiment = 0.5 + min(length, 100) / 200.0  # range: 0.5–1.0

    toxicity = 0.1
    spam_flag = False
    summary = text[:60] + ("..." if len(text) > 60 else "")

    return {
        "sentiment_score": float(round(sentiment, 3)),
        "toxicity_score": float(toxicity),
        "spam_flag": spam_flag,
        "ai_summary": summary,
    }
