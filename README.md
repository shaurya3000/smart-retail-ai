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
- Random Forest product classifier  - Logistic Regression sentiment      - FAQ intent knowledgebase
       |                                    |                                    |
       +------------------------------------+------------------------------------+
                                            |
                                            v
                               Storage & Model Artifacts
                  (face_db.pkl, product_classifier.pkl, sentiment_model.pkl,
                   chatbot_model.pkl, customer_visits.json, intents.json)
```

---

## 📚 2. Syllabus & Module Mapping

| Syllabus Topic | Project Module Implementation | Deliverable / File |
| :--- | :--- | :--- |
| **OpenCV Basics** | Frame preprocessing, grayscale, resizing, Gaussian blur, Canny edge detection, Haar face bounding box | `app/services/cv_utils.py` |
| **Image Classification** | 5-class product classifier (Clothing, Shoes, Electronics, Bags, Groceries) | `product_classifier.pkl` |
| **Face Recognition** | Facial feature extraction, 128D encodings, database comparison, customer visit logging | `face_db.pkl`, `cv_service.py` |
| **Text Preprocessing** | Lowercasing, punctuation removal, stopword filtering, tokenization | `nlp_service.py` |
| **Sentiment Analysis** | Customer feedback classifier (Positive / Neutral / Negative + confidence) | `sentiment_model.pkl`, `vectorizer.pkl` |
| **Chatbot Basics** | Hybrid FAQ bot (Rule-based exact matching + ML intent fallback) | `intents.json`, `chatbot_model.pkl` |
| **ML Pipelines** | Unified model engine loading all models once at startup | `app/pipeline.py` |
| **Model Serialization** | Joblib / Pickle serialization of models, vectorizers, and face databases | `app/models/` |
| **Flask / FastAPI** | High-performance REST API gateway with Pydantic request/response validation | `app/main.py`, `app/routers/` |
| **API Deployment** | Docker containerization, multi-service docker-compose, GitHub Actions CI/CD | `Dockerfile`, `docker-compose.yml`, `deploy.yml` |

---

## ⚡ 3. Quick Start & Setup Guide

### Prerequisites
- Python 3.9+ installed
- Docker (optional, for containerized run)

### Step 1: Clone Repository & Create Virtual Environment
```bash
git clone https://github.com/your-org/smart-retail-ai.git
cd smart-retail-ai
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### Step 2: Install Dependencies & Train Models
```bash
pip install -r requirements.txt
python scripts/train_all_models.py
```

### Step 3: Run FastAPI REST Gateway
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Access interactive Swagger API Docs at: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

### Step 4: Run Streamlit Interactive Dashboard
In a new terminal window:
```bash
streamlit run dashboard.py
```
Open your browser at: **[http://localhost:8501](http://localhost:8501)**

---

## 🧪 4. Running Automated Tests

Run the comprehensive unit test suite:
```bash
python tests/run_tests.py
```
*(Tests cover pipeline initialization, CV product classification, face recognition, NLP sentiment analysis, chatbot rule/ML fallback matching, and aggregate dashboard telemetry).*

---

## 🐳 5. Docker Deployment

Deploy the entire platform (API + Streamlit UI) using Docker Compose:
```bash
docker-compose up --build
```
- API Gateway running on: `http://localhost:8000`
- Streamlit Dashboard running on: `http://localhost:8501`

---

## 🔐 6. Ethics, Data Privacy & Bias in Retail Facial Recognition

Facial recognition technology in retail environments offers significant operational efficiency and customer personalization benefits, but it also demands strict ethical safeguards, data privacy compliance, and bias mitigation strategies.

### A. Informed Consent & Biometric Privacy Compliance
- **Opt-In Requirement**: Facial check-in MUST operate on an explicit opt-in basis. Retail customers must proactively register and consent before their biometric data is processed.
- **No Raw Image Storage**: The system stores ONLY mathematical vector encodings (128-dimensional floating point hash vectors) in `face_db.pkl`. Raw facial images captured at store check-in counters are discarded immediately after feature extraction.
- **Regulatory Adherence**: Designed to align with **GDPR (Article 9 - Processing of Special Categories of Data)** and **CCPA/CPRA (Biometric Information Protection)**. Customers retain the right to request full deletion of their biometric encodings at any time.

### B. Algorithmic Bias & Demographic Fairness
- **Demographic Parity**: Facial recognition algorithms can exhibit accuracy variance across demographics (age, gender, ethnicity) if trained on non-representative datasets.
- **Mitigation Protocols**:
  1. Enforcing strict similarity distance thresholds (`threshold = 0.85`) to minimize False Acceptance Rates (FAR).
  2. Providing fallback standard guest check-in routes whenever facial matching confidence falls below acceptable thresholds.
  3. Routine auditing of false-match rates across diverse customer demographics.

---

## 📁 7. Repository Structure

```
smart-retail-ai/
├── app/
│   ├── main.py                  # FastAPI Application Entrypoint & Middleware
│   ├── config.py                # Configuration Settings & Security
│   ├── schemas.py               # Pydantic Data Validation Schemas
│   ├── pipeline.py              # Unified Model Engine (Startup loader)
│   ├── routers/                 # Vision, NLP, Chatbot API Routers
│   ├── services/                # OpenCV, Sentiment, Chatbot business logic
│   └── models/                  # Serialized Model Artifacts (.pkl)
├── dashboard.py                 # Streamlit Interactive Dashboard UI
├── notebooks/                   # Training & EDA Jupyter Notebooks
├── data/                        # Datasets (reviews.csv, intents.json)
├── tests/                       # Automated Test Suites
├── scripts/                     # Automated model training script
├── Dockerfile                   # Docker build instructions
├── docker-compose.yml           # Service orchestration
└── README.md                    # Project Documentation
```
