from fastapi import APIRouter
from app.schemas import DashboardStatsResponse
from app.services.cv_service import cv_service
from app.services.nlp_service import nlp_service
from app.services.chatbot_service import chatbot_service

router = APIRouter(prefix="/dashboard", tags=["Analytics Dashboard"])

@router.get("/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats():
    """
    Get aggregated real-time statistics for the frontend web dashboard.
    Returns customer visit logs, sentiment distribution, product categories, and chatbot intents.
    """
    total_visits = len(cv_service.visit_logs)
    sentiment_breakdown = nlp_service.sentiment_counts
    product_category_counts = cv_service.product_classification_counts
    top_chatbot_intents = chatbot_service.intent_counts
    recent_visits = cv_service.visit_logs[:10]
    
    return {
        "total_visits": total_visits,
        "sentiment_breakdown": sentiment_breakdown,
        "product_category_counts": product_category_counts,
        "top_chatbot_intents": top_chatbot_intents,
        "recent_visits": recent_visits
    }
