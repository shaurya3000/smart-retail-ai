from fastapi import APIRouter, HTTPException, status
from app.schemas import SentimentRequest, SentimentResponse
from app.pipeline import pipeline

router = APIRouter(prefix="", tags=["Natural Language Processing"])

@router.post("/analyze-sentiment", response_model=SentimentResponse, summary="Analyze sentiment of customer feedback or review")
async def analyze_sentiment(payload: SentimentRequest):
    """
    Accepts text review or feedback snippet.
    Executes text cleaning (lowercasing, punctuation, stopword filtering) and predicts
    sentiment (Positive / Neutral / Negative) with confidence probability breakdown.
    """
    if not payload.text or not payload.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field 'text' cannot be empty."
        )
        
    try:
        res = pipeline.analyze_sentiment(payload.text)
        return res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing sentiment: {str(e)}"
        )
