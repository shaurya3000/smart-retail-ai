from fastapi import APIRouter, HTTPException, status
from app.schemas import ChatbotRequest, ChatbotResponse
from app.pipeline import pipeline

router = APIRouter(prefix="", tags=["Retail Support Chatbot"])

@router.post("/chatbot", response_model=ChatbotResponse, summary="Query hybrid FAQ & retail support chatbot")
async def chatbot_endpoint(payload: ChatbotRequest):
    """
    Accepts customer query message.
    Executes hybrid matching: Rule-based FAQ exact match -> ML Intent Classifier fallback.
    Returns matched intent tag, bot reply, confidence score, and matching strategy.
    """
    if not payload.message or not payload.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field 'message' cannot be empty."
        )
        
    try:
        res = pipeline.process_chat(payload.message, payload.customer_id)
        return res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing chatbot service: {str(e)}"
        )
