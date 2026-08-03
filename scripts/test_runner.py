import os
import sys
import io
from PIL import Image

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi.testclient import TestClient

try:
    from app.main import app
    client = TestClient(app)

    def create_dummy_image_bytes():
        img = Image.new("RGB", (100, 100), color="blue")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        return buf.getvalue()

    print("[1/6] Testing /health endpoint...")
    res = client.get("/health")
    assert res.status_code == 200 and res.json()["status"].lower() == "healthy"
    print(" -> PASSED!")

    print("[2/6] Testing /dashboard/stats endpoint...")
    res = client.get("/dashboard/stats")
    data = res.json()
    assert res.status_code == 200 and ("total_visits" in data or "total_customer_visits" in data)
    print(" -> PASSED!")

    print("[3/6] Testing /analyze-sentiment endpoint...")
    res = client.post("/analyze-sentiment", json={"text": "Amazing quality and fast delivery!"})
    assert res.status_code == 200
    print(" -> PASSED!")

    print("[4/6] Testing /chatbot endpoint...")
    res = client.post("/chatbot", json={"message": "What is your return policy?"})
    assert res.status_code == 200
    print(" -> PASSED!")

    print("[5/6] Testing /recognize-face endpoint...")
    img_bytes = create_dummy_image_bytes()
    res = client.post("/recognize-face", files={"file": ("face.jpg", img_bytes, "image/jpeg")})
    assert res.status_code == 200
    print(" -> PASSED!")

    print("[6/6] Testing /classify-product endpoint...")
    res = client.post("/classify-product", files={"file": ("prod.jpg", img_bytes, "image/jpeg")})
    assert res.status_code == 200
    print(" -> PASSED!")

    print("\nALL 6 ENDPOINT & MODEL TESTS PASSED SUCCESSFULLY!")

except Exception as e:
    import traceback
    print(f"\nTEST FAILED WITH ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
