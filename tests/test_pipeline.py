import pytest
import io
from PIL import Image
from app.services.cv_service import cv_service
from app.services.nlp_service import nlp_service
from app.services.chatbot_service import chatbot_service
from app.pipeline import pipeline

def test_pipeline_initialization():
    pipeline.initialize()
    assert pipeline.is_initialized == True

def test_nlp_sentiment_analysis():
    pipeline.initialize()
    result = pipeline.analyze_sentiment("The quality of this leather jacket is exceptional!")
    assert result["sentiment"] == "positive"
    assert result["confidence"] > 0.5
    assert "cleaned_text" in result

def test_nlp_negative_sentiment():
    pipeline.initialize()
    result = pipeline.analyze_sentiment("Battery life is terrible and the product arrived broken.")
    assert result["sentiment"] == "negative"
    assert result["confidence"] > 0.5

def test_chatbot_exact_faq_rule():
    pipeline.initialize()
    res = pipeline.process_chat("Where is my order?")
    assert res["intent"] == "order_status"
    assert "track" in res["bot_reply"].lower() or "order" in res["bot_reply"].lower()
    assert res["confidence"] > 0.90

def test_chatbot_fallback_intent():
    pipeline.initialize()
    res = pipeline.process_chat("Can I pay using PayPal?")
    assert res["intent"] == "payment_methods"

def test_cv_product_classification():
    pipeline.initialize()
    # Create sample image byte array
    img = Image.new('RGB', (224, 224), color=(100, 150, 200))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    img_bytes = buf.getvalue()
    
    res = pipeline.classify_product(img_bytes)
    assert "predicted_category" in res
    assert res["confidence"] >= 0.0
    assert "all_probabilities" in res

def test_cv_face_recognition():
    pipeline.initialize()
    img = Image.new('RGB', (300, 300), color=(150, 100, 50))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    img_bytes = buf.getvalue()
    
    res = pipeline.recognize_face(img_bytes)
    assert res["status"] in ["recognized", "unrecognized"]
    assert "total_visits" in res
