from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# Face Recognition Schemas
class FaceRecognitionResponse(BaseModel):
    status: str = Field(..., example="recognized")
    customer_id: Optional[str] = Field(None, example="CUST_1001")
    name: Optional[str] = Field(None, example="Alice Smith")
    loyalty_tier: Optional[str] = Field(None, example="Gold")
    confidence: float = Field(..., example=0.94)
    total_visits: int = Field(..., example=13)
    last_visit: str = Field(..., example="2026-08-03 17:10:00")
    consent_granted: bool = Field(..., example=True)
    message: str = Field(..., example="Welcome back, Alice Smith!")
    faces_detected: int = Field(1, example=1)

# Product Classifier Schemas
class ProductClassifierResponse(BaseModel):
    predicted_category: str = Field(..., example="clothing")
    confidence: float = Field(..., example=0.92)
    all_probabilities: Dict[str, float] = Field(
        ..., example={"clothing": 0.92, "bags": 0.04, "shoes": 0.02, "electronics": 0.01, "groceries": 0.01}
    )
    detected_objects: List[Dict[str, Any]] = Field(default_factory=list)

# Sentiment Analysis Schemas
class SentimentRequest(BaseModel):
    text: str = Field(..., example="The quality of this jacket is exceptional, highly recommend!", min_length=1)

class SentimentResponse(BaseModel):
    raw_text: str = Field(..., example="The quality of this jacket is exceptional, highly recommend!")
    cleaned_text: str = Field(..., example="quality jacket exceptional highly recommend")
    sentiment: str = Field(..., example="positive")
    confidence: float = Field(..., example=0.96)
    probabilities: Dict[str, float] = Field(
        ..., example={"positive": 0.96, "neutral": 0.03, "negative": 0.01}
    )

# Chatbot Schemas
class ChatbotRequest(BaseModel):
    message: str = Field(..., example="Where is my order?", min_length=1)
    customer_id: Optional[str] = Field(None, example="CUST_1001")

class ChatbotResponse(BaseModel):
    query: str = Field(..., example="Where is my order?")
    bot_reply: str = Field(..., example="You can track your order status in real time under My Orders.")
    intent: str = Field(..., example="order_status")
    confidence: float = Field(..., example=0.98)
    strategy_used: str = Field(..., example="Rule-based FAQ")

# Dashboard Stats Schemas
class DashboardStatsResponse(BaseModel):
    total_customer_visits: int = Field(..., example=89)
    unique_recognized_customers: int = Field(..., example=5)
    recent_visits: List[Dict[str, Any]] = Field(default_factory=list)
    sentiment_summary: Dict[str, int] = Field(
        ..., example={"positive": 35, "neutral": 8, "negative": 7}
    )
    chatbot_query_count: int = Field(..., example=142)
    top_faq_intents: List[Dict[str, Any]] = Field(default_factory=list)
    system_status: str = Field(..., example="HEALTHY")
