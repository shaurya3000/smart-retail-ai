# AI-Powered Smart Retail & Customer Intelligence Platform

[![Live Web App](https://img.shields.io/badge/🚀_Live_Web_App-Click_to_Open-ff4b4b?style=for-the-badge&logo=streamlit)](https://smart-retail-ai-a5kksj3kt7ab6xyzqfwx66.streamlit.app/)
[![FastAPI](https://img.shields.io/badge/API_Gateway-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://github.com/shaurya3000/smart-retail-ai)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)](https://github.com/shaurya3000/smart-retail-ai)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)](https://github.com/shaurya3000/smart-retail-ai)

> 🌐 **Live Web Application URL**:  
> Evaluators and reviewers can open and interact with the live deployed application in 1-click:  
> 👉 **[https://smart-retail-ai-a5kksj3kt7ab6xyzqfwx66.streamlit.app/](https://smart-retail-ai-a5kksj3kt7ab6xyzqfwx66.streamlit.app/)**

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

## 📊 3. Project Presentation Deliverables

- 🌐 **Live Web Application**: [https://smart-retail-ai-a5kksj3kt7ab6xyzqfwx66.streamlit.app/](https://smart-retail-ai-a5kksj3kt7ab6xyzqfwx66.streamlit.app/)
- 📄 **Slide-by-Slide Presentation Report**: [`DEMO_PRESENTATION.md`](https://github.com/shaurya3000/smart-retail-ai/blob/master/DEMO_PRESENTATION.md)
- 📊 **Downloadable PowerPoint Deck**: [`Smart_Retail_Platform_Presentation_Final.pptx`](https://github.com/shaurya3000/smart-retail-ai/raw/master/Smart_Retail_Platform_Presentation_Final.pptx)

---

## ⚡ 4. Quick Start & Setup Guide for Evaluators

### Option 1: Live Cloud Web Access (0 Setup)
Open **[https://smart-retail-ai-a5kksj3kt7ab6xyzqfwx66.streamlit.app/](https://smart-retail-ai-a5kksj3kt7ab6xyzqfwx66.streamlit.app/)** directly in any web browser.

---

### Option 2: Local Execution (3 Commands)
```bash
# 1. Clone repository
git clone https://github.com/shaurya3000/smart-retail-ai.git
cd smart-retail-ai

# 2. Install dependencies & initialize models
pip install -r requirements.txt
python scripts/train_all_models.py

# 3. Run dashboard
python -m streamlit run dashboard.py
```
Open **[http://localhost:8501](http://localhost:8501)** in any web browser.

---

### Option 3: 1-Click Docker Container Setup
```bash
git clone https://github.com/shaurya3000/smart-retail-ai.git
cd smart-retail-ai
docker-compose up --build
```
Open **[http://localhost:8501](http://localhost:8501)** in any web browser.
