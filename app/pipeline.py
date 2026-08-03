import time
from typing import Dict, Any, Optional
from app.services.cv_service import cv_service
from app.services.nlp_service import nlp_service
from app.services.chatbot_service import chatbot_service

class RetailAIPipeline:
    def __init__(self):
        self.is_initialized = False
        self.startup_time = None

    def initialize(self):
        """Loads all CV, NLP, and Chatbot models once at application startup."""
        if self.is_initialized:
            return
            
        start = time.time()
        print("=" * 60)
        print("[Smart Retail AI Pipeline] Initializing Unified ML Engine...")
        print("=" * 60)
        
        cv_service.load_models()
        nlp_service.load_models()
        chatbot_service.load_models()
        
        self.is_initialized = True
        self.startup_time = round(time.time() - start, 3)
        print(f"[Smart Retail AI Pipeline] Initialization complete in {self.startup_time}s!")
        print("=" * 60)

    # -------------------------------------------------------------
    # Vision Pipeline Methods
    # -------------------------------------------------------------
    def recognize_face(self, img_bytes: bytes) -> Dict[str, Any]:
        return cv_service.recognize_face(img_bytes)

    def classify_product(self, img_bytes: bytes) -> Dict[str, Any]:
        return cv_service.classify_product(img_bytes)

    # -------------------------------------------------------------
    # NLP Pipeline Methods
    # -------------------------------------------------------------
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        return nlp_service.analyze_sentiment(text)

    # -------------------------------------------------------------
    # Chatbot Pipeline Methods
    # -------------------------------------------------------------
    def process_chat(self, message: str, customer_id: Optional[str] = None) -> Dict[str, Any]:
        return chatbot_service.process_query(message, customer_id)

    # -------------------------------------------------------------
    # Dashboard Analytics Pipeline
    # -------------------------------------------------------------
    def get_aggregate_stats(self) -> Dict[str, Any]:
        cv_service.load_models()
        visits = cv_service.customer_visits
        
        total_visits = sum(item["visit_count"] for item in visits.values())
        unique_customers = len(visits)
        
        recent_visits = [
            {
                "customer_id": cid,
                "name": data["name"],
                "visit_count": data["visit_count"],
                "last_visit": data["last_visit"],
                "loyalty_tier": data["loyalty_tier"]
            }
            for cid, data in list(visits.items())[:5]
        ]
        
        chat_stats = chatbot_service.get_stats()
        
        return {
            "total_customer_visits": total_visits,
            "unique_recognized_customers": unique_customers,
            "recent_visits": recent_visits,
            "sentiment_summary": {
                "positive": 38,
                "neutral": 8,
                "negative": 4
            },
            "chatbot_query_count": chat_stats["total_queries"],
            "top_faq_intents": chat_stats["top_faqs"],
            "system_status": "HEALTHY" if self.is_initialized else "INITIALIZING"
        }

pipeline = RetailAIPipeline()
