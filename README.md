# AI-Powered Smart Retail & Customer Intelligence Platform

A production-grade, integrated AI solution for retail and e-commerce businesses. The platform combines Computer Vision (biometric face check-in & 5-class product classification), Natural Language Processing (customer feedback sentiment analysis & hybrid FAQ support chatbot), MLOps (unified model pipeline & FastAPI gateway), and an Interactive Streamlit Dashboard.

---

## 📐 1. System Architecture

```
Client Layer (Streamlit Dashboard / Postman / Mobile / Web Feed)
       |
       | REST API Calls (HTTP / Base64 / JSON)
       v
FastAPI Gateway (Port 8000)
├── POST /recognize-face       -> Customer Recognition & Visit Logger
├── POST /classify-product     -> 5-Class Product Category Classifier
├── POST /analyze-sentiment    -> Customer Review Sentiment Engine
├── POST /chatbot              -> Hybrid FAQ & Intent Support Bot
└── GET  /dashboard/stats      -> Real-Time Retail Intelligence Telemetry
       |
       +------------------------------------+------------------------------------+
       |                                    |                                    |
       v                                    v                                    v
Computer Vision Module               NLP Module                           Chatbot Module
- OpenCV frame preprocessing        - Lowercasing, punctuation,          - Rule-based exact keyword match
- 128D HOG/landmark face encodings   stopword filtering                   - TF-IDF + LogisticRegression
- Cosine distance matching          - TF-IDF vectorization                 ML intent classification fallback
- MobileNetV2 product classifier    - Logistic Regression sentiment      - FAQ intent knowledgebase
       |                                    |                                    |
       +------------------------------------+------------------------------------+
                                            |
                                            v
                               Storage & Model Artifacts
                  (face_db.pkl, product_classifier.pkl, sentiment_model.pkl,
                   chatbot_model.pkl, customer_visits.json, intents.json)
```

---

## 📸 2. Live Application Modules & UI Screenshots

### 👤 Module A: Customer Recognition & Visit Logger
Biometric face check-in system extracting 128D HOG facial encodings, matching against registered profiles (`face_db.pkl`), and logging persistent store visits with timestamps and VIP loyalty tiers.

![Customer Recognition & Visit Logger](assets/screenshots/face_recognition.png)

---

### 💬 Module B: Customer Feedback Sentiment NLP Engine
TF-IDF + Calibrated Logistic Regression NLP pipeline categorizing customer feedback into Positive 😄, Neutral 😐, or Negative 😞 with sharp confidence probability breakdowns.

![Customer Feedback Sentiment Engine](assets/screenshots/sentiment_analysis_2.png)

---

### 🤖 Module B: AI Retail Customer Support Assistant
Dual-Phase Hybrid Support Chatbot combining high-precision Rule-Based FAQ pattern matching (Phase 1) with an ML Intent Classifier fallback (Phase 2).

![AI Retail Support Chatbot Assistant](assets/screenshots/chatbot_assistant.png)

---

### 📊 Module C: Executive Retail Intelligence & Telemetry Dashboard
Real-time executive dashboard monitoring total store visits, registered VIP customers, chatbot query volume, feedback sentiment breakdown, and top FAQ inquiries.

![Executive Retail Intelligence Dashboard](assets/screenshots/executive_dashboard.png)

---

## 📚 3. Syllabus & Module Mapping

| Syllabus Topic | Project Module Implementation | Deliverable / File |
| :--- | :--- | :--- |
| **OpenCV Basics** | Frame preprocessing, grayscale, resizing, Gaussian blur, Canny edge detection, Haar face bounding box | `app/services/cv_utils.py` |
| **Image Classification** | PyTorch MobileNetV2 Deep Transfer Learning for 5 retail categories (Shoes, Clothing, Electronics, Bags, Groceries) | `app/services/cv_service.py` |
| **Face Recognition** | Facial feature extraction, 128D encodings, database comparison, customer visit logging | `face_db.pkl`, `cv_service.py` |
| **Text Preprocessing** | Lowercasing, punctuation removal, stopword filtering, tokenization | `nlp_service.py` |
| **Sentiment Analysis** | Customer feedback classifier (Positive / Neutral / Negative + confidence) | `sentiment_model.pkl`, `vectorizer.pkl` |
| **Chatbot Basics** | Hybrid FAQ bot (Rule-based exact matching + ML intent fallback) | `intents.json`, `chatbot_model.pkl` |
| **ML Pipelines** | Unified model engine loading all models once at startup | `app/pipeline.py` |
| **Model Serialization** | Joblib / Pickle serialization of models, vectorizers, and face databases | `app/models/` |
| **Flask / FastAPI** | High-performance REST API gateway with Pydantic request/response validation | `app/main.py`, `app/routers/` |
| **API Deployment** | Docker containerization, multi-service docker-compose, GitHub Actions CI/CD | `Dockerfile`, `docker-compose.yml`, `deploy.yml` |

---

## ⚡ 4. Quick Start & Setup Guide

### Step 1: Clone Repository & Install Dependencies
```bash
git clone https://github.com/shaurya3000/smart-retail-ai.git
cd smart-retail-ai
pip install -r requirements.txt
python scripts/train_all_models.py
```

### Step 2: Run FastAPI REST Gateway (Port 8000)
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Access interactive Swagger API Docs at: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

### Step 3: Run Streamlit Interactive Dashboard (Port 8501)
```bash
python -m streamlit run dashboard.py
```
Access live visual web app at: **[http://localhost:8501](http://localhost:8501)**

---

## 🧪 5. Running Automated Tests

Run the comprehensive 8/8 unit test suite:
```bash
python tests/run_tests.py
```

---

## 🐳 6. Docker Deployment

Deploy containerized services using Docker Compose:
```bash
docker-compose up --build
```

---

## 🔐 7. Ethics, Data Privacy & Bias in Retail Facial Recognition

- **100% Explicit Opt-In**: Biometric check-in operates on an explicit opt-in basis. Unregistered visitors remain anonymous guests (`GUEST_3682`).
- **Zero Raw Image Storage**: Raw photos are discarded immediately after feature extraction — ONLY 128D mathematical hash vectors are stored in `face_db.pkl`.
- **GDPR & CCPA Compliance**: Aligns with GDPR Article 9 and CCPA biometric protections.
- **Demographic Bias Mitigation**: Strict similarity distance thresholds (0.85) and fallback guest check-in routes minimize false acceptance rates across diverse demographics.

---

## 📁 8. Repository Structure

```
smart-retail-ai/
├── app/
│   ├── main.py                  # FastAPI Gateway Entrypoint & Middleware
│   ├── config.py                # Configuration Settings & Security
│   ├── schemas.py               # Pydantic Data Validation Schemas
│   ├── pipeline.py              # Unified Model Engine (Startup loader)
│   ├── routers/                 # Vision, NLP, Chatbot API Routers
│   ├── services/                # OpenCV, Sentiment, Chatbot business logic
│   └── models/                  # Serialized Model Artifacts (.pkl)
├── assets/screenshots/          # Live UI Application Screenshots
├── dashboard.py                 # Streamlit Interactive Dashboard UI
├── notebooks/                   # Training & EDA Jupyter Notebooks
├── data/                        # Datasets (reviews.csv, intents.json)
├── tests/                       # Automated Test Suite (run_tests.py)
├── scripts/                     # Automated model training script
├── Dockerfile                   # Docker build instructions
├── docker-compose.yml           # Service orchestration
└── README.md                    # Project Documentation & Screenshots
```
