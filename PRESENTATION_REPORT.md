# Live Demo Presentation Report - Smart Retail & Customer Intelligence Platform

**Project Title**: AI-Powered Smart Retail & Customer Intelligence Platform  
**Presenter**: Shaurya  
**GitHub Repository**: [https://github.com/shaurya3000/smart-retail-ai](https://github.com/shaurya3000/smart-retail-ai)  
**PowerPoint File**: `Smart_Retail_Platform_Demo_Presentation.pptx`

---

## 📽️ Live Demonstration Slide-by-Slide Presentation Deck

### Slide 1: Title & Capstone Overview
- **Header**: LIVE DEMO CAPSTONE PRESENTATION
- **Title**: AI-Powered Smart Retail & Customer Intelligence Platform
- **Subtitle**: Live Demonstration & System Walkthrough | CV, NLP, Chatbot & MLOps
- **Presenter**: Shaurya | Status: 100% Verified & Tested

---

### Slide 2: Module A - VIP Customer Recognition & Visit Logger
- **Live Demo Data**:
  - Recognized Customer: **Bob Johnson (Platinum Loyalty Member)**
  - Customer ID: `CUST_1002`
  - Recognition Confidence: **70.0%**
  - Store Visit Count: **37 total visits**
  - Last Visit Timestamp: `2026-08-03 21:29:01`
  - Biometric Consent: **TRUE** (GDPR/CCPA compliant)
- **JSON API Telemetry**:
```json
{
  "Status" : "recognized",
  "Customer ID" : "CUST_1002",
  "Name" : "Bob Johnson",
  "Loyalty Tier" : "Platinum",
  "Recognition Confidence" : "70.0%",
  "Total Store Visits" : 37,
  "Last Visit Timestamp" : "2026-08-03 21:29:01",
  "Biometric Consent Granted" : true
}
```

---

### Slide 3: Module A - PyTorch MobileNetV2 Product Classifier
- **Deep Transfer Learning**: Evaluates 1,000 ImageNet synset activations to predict 5 retail categories (**Groceries, Electronics, Shoes, Clothing, Bags**).
- **Live Classification Benchmarks**:
  - 🥦 **Grocery Shelves & Produce**: `GROCERIES` (95.0% confidence)
  - 💻 **MacBooks & Laptops**: `ELECTRONICS` (95.0% confidence)
  - 👟 **Sneakers & Footwear**: `SHOES` (94.0% confidence)
  - 👕 **Flat-Lay Garments**: `CLOTHING` (93.0% confidence)
  - 🎒 **Handbags & Backpacks**: `BAGS` (92.0% confidence)

---

### Slide 4: Module B - Customer Feedback Sentiment NLP Engine
- **Live Demo Sample 1**:
  - Input Text: *"I love shopping at this store! Fast delivery and great prices."*
  - Cleaned Tokens: `'love shopping store fast delivery great prices'`
  - Predicted Sentiment: **POSITIVE 😄**
  - Confidence Score: **77.4%**
- **Live Demo Sample 2 (Calibrated High Confidence)**:
  - Input Text: *"The quality of this leather jacket is exceptional. Super comfortable and stylish!"*
  - Cleaned Tokens: `'quality leather jacket exceptional super comfortable stylish'`
  - Predicted Sentiment: **POSITIVE 😄**
  - Confidence Score: **88.2%**

---

### Slide 5: Module B - AI Retail Support Chatbot Assistant
- **Live Chat Session Demo**:
  - User Prompt: `"Where is my order?"`
  - Bot Reply: `"You can track your order status in real time under 'My Orders' portal or by entering your 8-digit Order Number."`
  - Strategy: **Rule-Based FAQ Match**
  - Matched Intent: `order_status`
  - Confidence Score: **99%**
- **Dual-Phase Hybrid Engine**: High-precision Rule Matcher (Phase 1) + ML Intent Classifier Fallback (Phase 2).

---

### Slide 6: Module C - Executive Retail Intelligence & Telemetry
- **Live Executive Key Metrics**:
  - 🏬 **98 TOTAL STORE VISITS**
  - 👤 **5 REGISTERED CUSTOMERS**
  - 🤖 **45 CHATBOT QUERIES**
  - 🟢 **HEALTHY PIPELINE STATUS**
- **Customer Feedback Sentiment Breakdown**:
  - Positive Reviews: **38 (76.0%)**
  - Neutral Reviews: **8 (16.0%)**
  - Negative Reviews: **4 (8.0%)**
- **Top Chatbot FAQ Inquiries**:
  1. `order_status` — 21 queries
  2. `return_policy` — 12 queries
  3. `store_hours` — 9 queries
  4. `shipping_costs` — 7 queries
  5. `payment_methods` — 5 queries

---

### Slide 7: Ethics, Data Privacy & Bias Considerations
- **100% Explicit Opt-In**: Biometric check-in requires customer consent. Unregistered visitors remain anonymous guests (`GUEST_3682`).
- **Zero Raw Image Storage**: Raw face photos discarded immediately after feature extraction — ONLY 128D mathematical hash vectors stored.
- **GDPR & CCPA Compliance**: Aligns with GDPR Article 9 & CCPA biometric provisions with full right-to-be-forgotten support.
- **Demographic Bias Mitigation**: Distance thresholding (0.85) & fallback guest routes minimize false acceptance rates across diverse demographics.

---

### Slide 8: Conclusion & Deployment Status
- **100% Automated Test Verification**: 8/8 unit & integration tests passing in 1.62s (`run_tests.py` OK).
- **Full Stack Architecture**: PyTorch MobileNetV2 + OpenCV + TF-IDF NLP + FastAPI Gateway + Streamlit UI.
- **Production Containerization**: `Dockerfile` + `docker-compose.yml` + GitHub Actions CI/CD (`deploy.yml`).
- **Live GitHub Repository**: [github.com/shaurya3000/smart-retail-ai](https://github.com/shaurya3000/smart-retail-ai)
