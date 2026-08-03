import os

class Settings:
    PROJECT_NAME: str = "Smart Retail & Customer Intelligence Platform"
    VERSION: str = "1.0.0"
    API_PREFIX: str = ""
    
    # Base paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    APP_DIR: str = os.path.join(BASE_DIR, "app")
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    MODELS_DIR: str = os.path.join(APP_DIR, "models")
    
    # Model Paths
    PRODUCT_MODEL_PATH: str = os.path.join(MODELS_DIR, "product_classifier.pkl")
    PRODUCT_CATEGORIES_PATH: str = os.path.join(MODELS_DIR, "product_categories.json")
    FACE_DB_PATH: str = os.path.join(MODELS_DIR, "face_db.pkl")
    SENTIMENT_MODEL_PATH: str = os.path.join(MODELS_DIR, "sentiment_model.pkl")
    SENTIMENT_VECTORIZER_PATH: str = os.path.join(MODELS_DIR, "vectorizer.pkl")
    CHATBOT_MODEL_PATH: str = os.path.join(MODELS_DIR, "chatbot_model.pkl")
    CHATBOT_VECTORIZER_PATH: str = os.path.join(MODELS_DIR, "chatbot_vectorizer.pkl")
    
    # Data Paths
    REVIEWS_CSV_PATH: str = os.path.join(DATA_DIR, "reviews.csv")
    INTENTS_JSON_PATH: str = os.path.join(DATA_DIR, "intents.json")
    CUSTOMER_VISITS_PATH: str = os.path.join(DATA_DIR, "customer_visits.json")
    
    # Security
    API_KEY_NAME: str = "X-API-Key"
    API_KEY: str = os.getenv("RETAIL_API_KEY", "smart-retail-secret-key-2026")
    REQUIRE_API_KEY: bool = False  # Set True in strict production environments

settings = Settings()
