"""
Placeholder AI service.
Replace the internals with actual model calls:
- run sentiment model (BERT)
- run spam model
- run toxicity model
- generate summary using LLM
"""
from typing import Dict
 
async def analyze_review_text(text: str) -> Dict:
    # Dummy implementation.
    # Replace these heuristics with real model inference or HTTP calls.
    sentiment = 0.7 if "good" in text.lower() or "love" in text.lower() else -0.2
    spam = False if len(set(text.split())) > 3 else True
    toxicity = 0.05 if any(w in text.lower() for w in ["hate","stupid","idiot"]) else 0.01
    summary = text[:120] + ("..." if len(text) > 120 else "")
    return {
        "sentiment_score": float(sentiment),
        "spam_flag": bool(spam),
        "toxicity_score": float(toxicity),
        "ai_summary": summary,
    }