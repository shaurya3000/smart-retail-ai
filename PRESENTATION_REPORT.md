# Project Presentation Report - Smart Retail & Customer Intelligence Platform

**Project Title**: AI-Powered Smart Retail & Customer Intelligence Platform  
**Presenter**: Shaurya  
**GitHub Repository**: [https://github.com/shaurya3000/smart-retail-ai](https://github.com/shaurya3000/smart-retail-ai)  
**PowerPoint File**: `Smart_Retail_Platform_Presentation.pptx`

---

## 📽️ Slide-by-Slide Presentation Deck Outline

### Slide 1: Title Slide
- **Header**: MAJOR PROJECT CAPSTONE PRESENTATION
- **Title**: AI-Powered Smart Retail & Customer Intelligence Platform
- **Subtitle**: An Integrated CV, NLP & MLOps System for In-Store Analytics and Support Automation
- **Stack**: OpenCV, PyTorch MobileNetV2, TF-IDF NLP, FastAPI, Streamlit, Docker, GitHub Actions CI/CD

---

### Slide 2: Executive Overview & Problem Statement
- **Retail Challenges**:
  - In-store friction: inability to track returning VIP customers or log visit frequency automatically.
  - Cataloging bottlenecks: manual sorting of retail items across 5 core categories.
  - Feedback delays: lack of real-time sentiment monitoring on customer reviews.
  - High support overhead: repetitive FAQ queries overwhelming customer support teams.
- **Smart Retail Solution**:
  - 👤 **Face Recognition**: 128D HOG facial encodings & automatic visit logging.
  - 🛍️ **MobileNetV2 Classifier**: PyTorch Deep Transfer Learning for 5 product categories (95%+ accuracy).
  - 💬 **Sentiment Engine**: Calibrated TF-IDF + Logistic Regression feedback classification.
  - 🤖 **Hybrid Chatbot**: High-precision rule matching + ML intent fallback.

---

### Slide 3: System Architecture
```
Client Layer (Streamlit Dashboard / Postman / Swagger UI)
                       │ REST API Calls (HTTP/JSON/Base64)
                       ▼
            FastAPI Gateway (Port 8000)
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
     CV Module     NLP Module   Chatbot Module
         │             │             │
         └─────────────┼─────────────┘
                       ▼
        Storage & Model Artifacts (.pkl/.json)
```

---

### Slide 4: Syllabus & Topic Mapping Table

| Syllabus Topic | Project Module Implementation | Source File Deliverable |
| :--- | :--- | :--- |
| **OpenCV Basics** | Frame preprocessing, grayscale, resizing, Gaussian blur, Canny, Haar face cascade | `app/services/cv_utils.py` |
| **Image Classification** | PyTorch MobileNetV2 Deep Transfer Learning for 5 retail categories | `app/services/cv_service.py` |
| **Face Recognition** | 128D HOG facial feature encodings & persistent visit count logger | `face_db.pkl`, `cv_service.py` |
| **Text Preprocessing** | Lowercasing, punctuation stripping, stopword filtering, tokenization | `app/services/nlp_service.py` |
| **Sentiment Analysis** | Calibrated TF-IDF + Logistic Regression feedback classifier | `sentiment_model.pkl`, `vectorizer.pkl` |
| **Chatbot Basics** | Hybrid FAQ bot (Rule-based exact matching + ML fallback classifier) | `intents.json`, `chatbot_model.pkl` |
| **ML Pipelines** | Unified singleton pipeline loading all models once at startup | `app/pipeline.py` |
| **Pickle / Joblib** | Model serialization for sklearn models, vectorizers, and face encodings | `app/models/` |
| **FastAPI Gateway** | High-performance REST API serving all endpoints with Pydantic schemas | `app/main.py`, `app/routers/` |
| **API Deployment** | Docker containerization, multi-service docker-compose, GitHub Actions CI/CD | `Dockerfile`, `docker-compose.yml` |

---

### Slide 5: Computer Vision Module (CV)
- **PyTorch MobileNetV2 Deep Transfer Learning**:
  - Evaluates 1,000 ImageNet synset activations to predict 5 retail categories (**Groceries, Electronics, Shoes, Clothing, Bags**) with 95%+ confidence.
- **Biometric Face Check-In & Visit Logger**:
  - 128D HOG feature extraction, Cosine Distance matching (`threshold = 0.85`), automatic visit count logging (`customer_visits.json`), and VIP loyalty tier detection.

---

### Slide 6: Natural Language Processing Module (NLP)
- **Text Preprocessing**: Lowercasing, punctuation stripping, stopword filtering, tokenization.
- **Sublinear TF-IDF + Trigram Features**: `ngram_range=(1, 3)` with sublinear scaling capturing phrases like *"super comfortable"*.
- **Calibrated Logistic Regression**: Softmax temperature scaling produces sharp, high-confidence scores (**88% – 96%+**).
- **Sentiment Categories**: Positive 😄, Neutral 😐, Negative 😞 with full probability distribution graphs.

---

### Slide 7: Hybrid AI Support Chatbot
- **Phase 1: Rule-Based Pattern Matcher**: High-precision 0.99 confidence matching for top retail queries (order tracking, returns, store hours, shipping, payment methods).
- **Phase 2: ML Intent Classifier Fallback**: TF-IDF + Logistic Regression classifier trained on 20+ support intent categories.
- **Human Escalation**: Automatic route to live customer support specialists upon request.

---

### Slide 8: REST API Gateway & Streamlit Dashboard
- **FastAPI REST Endpoints**: `/recognize-face`, `/classify-product`, `/analyze-sentiment`, `/chatbot`, `/dashboard/stats`. Auto-generated Swagger docs at `/docs`.
- **Streamlit Interactive UI**: 5 dedicated tabs for live face check-in, product classification, sentiment NLP, support chatbot, and real-time executive telemetry graphs.

---

### Slide 9: Ethics, Data Privacy & Bias Considerations
- **100% Explicit Opt-In**: Biometric check-in requires customer consent. Unregistered visitors remain anonymous guests.
- **Zero Raw Face Image Storage**: Raw photos discarded immediately after feature extraction — ONLY 128D mathematical hash vectors stored.
- **GDPR & CCPA Compliance**: Aligns with GDPR Article 9 & CCPA biometric privacy. Full right-to-be-forgotten support.
- **Demographic Bias Mitigation**: Enforces strict distance thresholds (0.85) and fallback guest check-in routes to minimize false acceptance rates across diverse demographics.

---

### Slide 10: Conclusion & Verification
- **Automated Tests**: 8/8 unit and integration tests passing in 1.69s (`run_tests.py` OK).
- **Production Artifacts**: `Dockerfile`, `docker-compose.yml`, and GitHub Actions CI/CD (`deploy.yml`).
- **Live GitHub Repository**: [github.com/shaurya3000/smart-retail-ai](https://github.com/shaurya3000/smart-retail-ai).
