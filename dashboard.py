import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import io
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

# Import direct pipeline as fallback for Cloud deployment / Standalone execution
try:
    from app.pipeline import pipeline
    pipeline.initialize()
    PIPELINE_AVAILABLE = True
except Exception as p_err:
    PIPELINE_AVAILABLE = False
    print(f"Pipeline import warning: {p_err}")

# Set Page Configuration
st.set_page_config(
    page_title="Smart Retail Intelligence Platform",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Glassmorphism Design
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #e0e6ed;
    }
    .stAppHeader {
        background-color: rgba(14, 17, 23, 0.8);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        text-align: center;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #4facfe;
    }
    .metric-label {
        font-size: 0.95rem;
        color: #a0aec0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .custom-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .badge-healthy {
        background-color: #10B981;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-standalone {
        background-color: #3B82F6;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# API Base URL
API_URL = "http://127.0.0.1:8000"

# Service Helpers with automatic Direct Pipeline Fallback for Streamlit Cloud
def fetch_recognize_face(img_bytes):
    try:
        response = requests.post(f"{API_URL}/recognize-face", files={"file": ("face.jpg", img_bytes, "image/jpeg")}, timeout=2)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    if PIPELINE_AVAILABLE:
        return pipeline.recognize_face(img_bytes)
    raise RuntimeError("Service unavailable")

def fetch_classify_product(img_bytes):
    try:
        response = requests.post(f"{API_URL}/classify-product", files={"file": ("product.jpg", img_bytes, "image/jpeg")}, timeout=2)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    if PIPELINE_AVAILABLE:
        return pipeline.classify_product(img_bytes)
    raise RuntimeError("Service unavailable")

def fetch_analyze_sentiment(text):
    try:
        response = requests.post(f"{API_URL}/analyze-sentiment", json={"text": text}, timeout=2)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    if PIPELINE_AVAILABLE:
        return pipeline.analyze_sentiment(text)
    raise RuntimeError("Service unavailable")

def fetch_chatbot_reply(msg):
    try:
        response = requests.post(f"{API_URL}/chatbot", json={"message": msg}, timeout=2)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    if PIPELINE_AVAILABLE:
        res = pipeline.process_chat(msg)
        return {
            "bot_reply": res["reply"],
            "strategy_used": res["strategy"],
            "intent": res["intent"],
            "confidence": res["confidence"]
        }
    raise RuntimeError("Service unavailable")

def fetch_dashboard_stats():
    try:
        response = requests.get(f"{API_URL}/dashboard/stats", timeout=2)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    if PIPELINE_AVAILABLE:
        return pipeline.get_aggregate_stats()
    raise RuntimeError("Service unavailable")

# Header Section
col_title, col_status = st.columns([3, 1])
with col_title:
    st.markdown('<div class="custom-title">Smart Retail & Customer Intelligence Platform</div>', unsafe_allow_html=True)
    st.markdown("*AI-Powered CV, NLP & MLOps System for Modern Retail Automation*")

with col_status:
    try:
        r = requests.get(f"{API_URL}/health", timeout=1)
        if r.status_code == 200:
            st.markdown('<br><span class="badge-healthy">🟢 API Gateway Online</span>', unsafe_allow_html=True)
        else:
            st.markdown('<br><span class="badge-standalone">⚡ Standalone Cloud Mode</span>', unsafe_allow_html=True)
    except Exception:
        st.markdown('<br><span class="badge-standalone">⚡ Standalone Cloud Mode</span>', unsafe_allow_html=True)

st.divider()

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/isometric/100/shopping-bag.png", width=70)
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Module:",
    [
        "👤 Face Recognition & Check-In",
        "🛍️ Product Category Classifier",
        "💬 Sentiment Analysis Engine",
        "🤖 AI Retail Support Chatbot",
        "📊 Executive Intelligence Dashboard"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("**System Architecture Overview:**")
st.sidebar.caption("• **Vision**: OpenCV + HOG / Haar Face Encodings + 5-Class Product Classifier")
st.sidebar.caption("• **NLP**: TF-IDF + Logistic Regression Sentiment Engine")
st.sidebar.caption("• **Chatbot**: Hybrid Rule-Based FAQ + ML Fallback Intent Classifier")
st.sidebar.caption("• **Deployment**: FastAPI Gateway + Streamlit Dashboard + Docker")

# -----------------------------------------------------------------------------
# Module 1: Face Recognition & Check-In
# -------------------------------------------------------------
if page == "👤 Face Recognition & Check-In":
    st.header("👤 Customer Recognition & Visit Logger")
    st.write("Upload or capture a customer image to detect facial features, verify returning customer status, and log visit analytics.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Face Input")
        input_type = st.radio("Choose Input Method:", ["Sample Customer Faces", "Upload Image", "Webcam Capture"])
        
        img_bytes = None
        if input_type == "Sample Customer Faces":
            sample_cust = st.selectbox(
                "Select Test Profile:",
                [
                    "Alice Smith (Gold VIP)",
                    "Bob Johnson (Platinum VIP)",
                    "Charlie Brown (Silver VIP)",
                    "Diana Prince (VIP Gold)",
                    "New Guest / Unrecognized"
                ]
            )
            img = Image.new('RGB', (300, 300), color=(73, 109, 137))
            buf = io.BytesIO()
            img.save(buf, format='JPEG')
            img_bytes = buf.getvalue()
            st.image(img, caption=f"Selected: {sample_cust}", width=250)
            
        elif input_type == "Upload Image":
            uploaded_file = st.file_uploader("Choose a face image...", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                img_bytes = uploaded_file.getvalue()
                st.image(img_bytes, caption="Uploaded Image", width=250)
                
        elif input_type == "Webcam Capture":
            camera_file = st.camera_input("Take a photo")
            if camera_file is not None:
                img_bytes = camera_file.getvalue()

    with col2:
        st.subheader("Recognition Results")
        if img_bytes and st.button("Run Face Recognition Pipeline", type="primary"):
            with st.spinner("Analyzing facial features and querying database..."):
                try:
                    data = fetch_recognize_face(img_bytes)
                    if data["status"] == "recognized":
                        st.success(f"🎉 **{data['message']}**")
                    else:
                        st.info(f"👋 **{data['message']}**")
                        
                    st.json({
                        "Status": data["status"],
                        "Customer ID": data["customer_id"],
                        "Name": data["name"],
                        "Loyalty Tier": data["loyalty_tier"],
                        "Recognition Confidence": f"{data['confidence']*100:.1f}%",
                        "Total Store Visits": data["total_visits"],
                        "Last Visit Timestamp": data["last_visit"],
                        "Biometric Consent Granted": data["consent_granted"]
                    })
                except Exception as ex:
                    st.error(f"Error executing face recognition: {ex}")

# -----------------------------------------------------------------------------
# Module 2: Product Category Classifier
# -------------------------------------------------------------
elif page == "🛍️ Product Category Classifier":
    st.header("🛍️ Product Image Classification Engine")
    st.write("Upload a retail product image to classify it into **Clothing, Shoes, Electronics, Bags, or Groceries**.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Product Image Upload")
        uploaded_file = st.file_uploader("Upload product picture...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is None:
            st.info("💡 Upload any product image, or click below to run test classification.")
            img = Image.new('RGB', (224, 224), color=(120, 80, 200))
            buf = io.BytesIO()
            img.save(buf, format='JPEG')
            img_bytes = buf.getvalue()
            st.image(img, caption="Demo Product Sample", width=224)
        else:
            img_bytes = uploaded_file.getvalue()
            st.image(img_bytes, caption="Uploaded Product Image", width=250)

    with col2:
        st.subheader("Classification Predictions")
        if st.button("Classify Product Image", type="primary"):
            with st.spinner("Extracting visual features & evaluating classifier..."):
                try:
                    data = fetch_classify_product(img_bytes)
                    st.markdown(f"### Predicted Category: **{data['predicted_category'].upper()}**")
                    st.markdown(f"Confidence Score: **{data['confidence']*100:.1f}%**")
                    
                    st.subheader("Category Probability Breakdown:")
                    df_probs = pd.DataFrame(list(data["all_probabilities"].items()), columns=["Category", "Probability"])
                    df_probs["Probability"] = df_probs["Probability"] * 100
                    
                    st.bar_chart(df_probs.set_index("Category"))
                except Exception as ex:
                    st.error(f"Classification error: {ex}")

# -----------------------------------------------------------------------------
# Module 3: Sentiment Analysis Engine
# -------------------------------------------------------------
elif page == "💬 Sentiment Analysis Engine":
    st.header("💬 Customer Feedback & Review NLP Sentiment Engine")
    st.write("Analyze customer feedback text to detect sentiment (Positive, Neutral, Negative) and confidence scores.")
    
    sample_text = st.selectbox(
        "Try sample customer reviews:",
        [
            "Custom text entry",
            "The quality of this leather jacket is exceptional. Super comfortable and stylish!",
            "Battery life on this smartwatch is terrible. It died in less than 4 hours.",
            "The bag is okay, nothing special. Materials feel a bit cheap for the price.",
            "Delivery took over two weeks and the box was completely damaged."
        ]
    )
    
    if sample_text == "Custom text entry":
        user_review = st.text_area("Enter Customer Review / Feedback:", "I love shopping at this store! Fast delivery and great prices.")
    else:
        user_review = st.text_area("Enter Customer Review / Feedback:", sample_text)

    if st.button("Analyze Sentiment", type="primary"):
        with st.spinner("Executing NLP cleaning pipeline & predicting sentiment..."):
            try:
                data = fetch_analyze_sentiment(user_review)
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    if data["sentiment"] == "positive":
                        st.success(f"### Sentiment: POSITIVE 😄")
                    elif data["sentiment"] == "negative":
                        st.error(f"### Sentiment: NEGATIVE 😞")
                    else:
                        st.warning(f"### Sentiment: NEUTRAL 😐")
                    st.metric("Confidence Score", f"{data['confidence']*100:.1f}%")
                    
                with col_res2:
                    st.markdown("**NLP Preprocessing Pipeline:**")
                    st.code(f"Raw Input: '{data['raw_text']}'\nCleaned Tokens: '{data['cleaned_text']}'")
                    
                st.subheader("Sentiment Probability Breakdown:")
                df_s = pd.DataFrame(list(data["probabilities"].items()), columns=["Sentiment", "Probability"])
                st.bar_chart(df_s.set_index("Sentiment"))
            except Exception as ex:
                st.error(f"Error processing sentiment: {ex}")

# -----------------------------------------------------------------------------
# Module 4: AI Retail Support Chatbot
# -------------------------------------------------------------
elif page == "🤖 AI Retail Support Chatbot":
    st.header("🤖 AI Retail Customer Support Assistant")
    st.write("Test our hybrid chatbot combining **Rule-based FAQ matching** with an **ML Intent Classifier fallback**.")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I am your AI Smart Retail Assistant. How can I help you today with orders, returns, shipping, or store info?"}
        ]

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "meta" in msg:
                st.caption(f"Strategy: {msg['meta']['strategy']} | Intent: `{msg['meta']['intent']}` | Confidence: {msg['meta']['confidence']*100:.0f}%")

    st.caption("Quick FAQ Prompts:")
    q_cols = st.columns(4)
    quick_query = None
    if q_cols[0].button("Track Order"): quick_query = "Where is my order?"
    if q_cols[1].button("Return Policy"): quick_query = "What is your return policy?"
    if q_cols[2].button("Store Hours"): quick_query = "What are your store hours?"
    if q_cols[3].button("Human Agent"): quick_query = "I want to speak to a human agent"

    user_input = st.chat_input("Type your question here...")
    prompt = quick_query or user_input
    
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        try:
            data = fetch_chatbot_reply(prompt)
            bot_reply = data["bot_reply"]
            meta = {
                "strategy": data["strategy_used"],
                "intent": data["intent"],
                "confidence": data["confidence"]
            }
            
            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply, "meta": meta})
            with st.chat_message("assistant"):
                st.write(bot_reply)
                st.caption(f"Strategy: {meta['strategy']} | Intent: `{meta['intent']}` | Confidence: {meta['confidence']*100:.0f}%")
        except Exception as ex:
            st.error(f"Error querying chatbot: {ex}")

# -----------------------------------------------------------------------------
# Module 5: Executive Intelligence Dashboard
# -------------------------------------------------------------
elif page == "📊 Executive Intelligence Dashboard":
    st.header("📊 Executive Retail Intelligence & System Analytics")
    st.write("Real-time telemetry and aggregate customer insights across all deployed AI modules.")
    
    try:
        stats = fetch_dashboard_stats()
        
        # Metric Cards
        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        with mcol1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{stats["total_customer_visits"]}</div><div class="metric-label">Total Store Visits</div></div>', unsafe_allow_html=True)
        with mcol2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{stats["unique_recognized_customers"]}</div><div class="metric-label">Registered Customers</div></div>', unsafe_allow_html=True)
        with mcol3:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{stats["chatbot_query_count"]}</div><div class="metric-label">Chatbot Queries</div></div>', unsafe_allow_html=True)
        with mcol4:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{stats["system_status"]}</div><div class="metric-label">Pipeline Status</div></div>', unsafe_allow_html=True)

        st.divider()
        
        # Analytics Charts
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Customer Feedback Sentiment Distribution")
            sent_data = stats["sentiment_summary"]
            df_sent = pd.DataFrame(list(sent_data.items()), columns=["Sentiment", "Count"])
            st.bar_chart(df_sent.set_index("Sentiment"))
            
        with c2:
            st.subheader("Top Chatbot FAQ Inquiries")
            top_faqs = stats.get("top_faq_intents", [])
            if top_faqs:
                df_faqs = pd.DataFrame(top_faqs)
                st.dataframe(df_faqs, use_container_width=True)
            else:
                st.info("No query logs accumulated yet.")

        st.divider()
        st.subheader("Recent Customer Visit Telemetry")
        if stats["recent_visits"]:
            df_visits = pd.DataFrame(stats["recent_visits"])
            st.dataframe(df_visits, use_container_width=True)

    except Exception as ex:
        st.error(f"Unable to load live dashboard stats: {ex}")
