import pytest
from fastapi.testclient import TestClient
import io
from PIL import Image
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"

def test_sentiment_endpoint():
    payload = {"text": "I love these shoes, super comfortable and stylish!"}
    response = client.post("/analyze-sentiment", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "positive"
    assert "confidence" in data

def test_chatbot_endpoint():
    payload = {"message": "What is your return policy?"}
    response = client.post("/chatbot", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "return_policy"
    assert "bot_reply" in data

def test_classify_product_endpoint():
    img = Image.new('RGB', (224, 224), color=(80, 180, 90))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)
    
    response = client.post(
        "/classify-product",
        files={"file": ("test_prod.jpg", buf, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "predicted_category" in data
    assert "confidence" in data

def test_recognize_face_endpoint():
    img = Image.new('RGB', (300, 300), color=(200, 120, 80))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)
    
    response = client.post(
        "/recognize-face",
        files={"file": ("face.jpg", buf, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["recognized", "unrecognized"]

def test_dashboard_stats_endpoint():
    response = client.get("/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_customer_visits" in data
    assert "sentiment_summary" in data
