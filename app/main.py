from fastapi import FastAPI, Depends, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Optional

from app.config import settings
from app.pipeline import pipeline
from app.schemas import DashboardStatsResponse
from app.routers import vision, nlp, chatbot

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load ML models once into memory
    print(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}...")
    pipeline.initialize()
    yield
    # Shutdown
    print("Shutting down Smart Retail Platform API Gateway...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
### Smart Retail & Customer Intelligence Platform REST API
An end-to-end AI gateway serving Computer Vision, Natural Language Processing, and Automated Customer Support for retail environments.

**Features**:
* 👤 **Face Recognition & Visit Logger** (`/recognize-face`): Biometric customer check-in and loyalty analytics.
* 🛍️ **Product Image Classifier** (`/classify-product`): 5-class retail item classification (Clothing, Shoes, Electronics, Bags, Groceries).
* 💬 **Sentiment Analysis Engine** (`/analyze-sentiment`): Customer feedback NLP classification (Positive, Neutral, Negative).
* 🤖 **Hybrid Support Chatbot** (`/chatbot`): Rule-based FAQ matcher + ML intent fallback.
* 📊 **Executive Intelligence Dashboard** (`/dashboard/stats`): Real-time aggregate customer visit and sentiment statistics.
""",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional API Key Authentication Dependency
async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if settings.REQUIRE_API_KEY:
        if not x_api_key or x_api_key != settings.API_KEY:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing X-API-Key security header."
            )
    return x_api_key

# Include Routers
app.include_router(vision.router, dependencies=[Depends(verify_api_key)])
app.include_router(nlp.router, dependencies=[Depends(verify_api_key)])
app.include_router(chatbot.router, dependencies=[Depends(verify_api_key)])

@app.get("/dashboard/stats", response_model=DashboardStatsResponse, tags=["Executive Analytics Dashboard"], summary="Get aggregate retail intelligence metrics")
async def get_dashboard_stats():
    """
    Returns real-time aggregate retail metrics including:
    - Total Customer Visits
    - Unique Recognized Customers
    - Recent Customer Visit Logs
    - Customer Feedback Sentiment Distribution
    - Chatbot Query Volume & Top FAQ Intents
    """
    try:
        return pipeline.get_aggregate_stats()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving dashboard statistics: {str(e)}"
        )

@app.get("/health", tags=["System Health"], summary="Health check endpoint")
async def health_check():
    return {
        "status": "HEALTHY",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "pipeline_initialized": pipeline.is_initialized
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
