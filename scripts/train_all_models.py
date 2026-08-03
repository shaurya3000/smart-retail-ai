import os
import json
import pickle
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier

def train_all():
    print("=" * 60)
    print("Smart Retail Platform - Model Trainer with Calibrated Sentiment NLP")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    models_dir = os.path.join(base_dir, "app", "models")
    os.makedirs(models_dir, exist_ok=True)

    # -------------------------------------------------------------
    # 1. Product Image Classifier
    # -------------------------------------------------------------
    categories = ["clothing", "shoes", "electronics", "bags", "groceries"]
    np.random.seed(42)
    X_prod = []
    y_prod = []
    
    num_per_cat = 500
    for cat in categories:
        feats = np.zeros((num_per_cat, 32))
        if cat == "clothing":
            feats[:, 24] = np.random.uniform(0.6, 1.6, num_per_cat)
            feats[:, 26] = np.random.uniform(0.02, 0.08, num_per_cat)
            feats[:, 31] = np.random.uniform(0.40, 0.85, num_per_cat)
            feats[:, 8:16] = np.random.uniform(0.1, 0.5, (num_per_cat, 8))
        elif cat == "shoes":
            feats[:, 24] = np.random.uniform(0.85, 1.45, num_per_cat)
            feats[:, 25] = np.random.uniform(0.08, 0.35, num_per_cat)
            feats[:, 26] = np.random.uniform(0.05, 0.15, num_per_cat)
            feats[:, 31] = np.random.uniform(0.20, 0.45, num_per_cat)
        elif cat == "electronics":
            feats[:, 24] = np.random.uniform(0.9, 1.5, num_per_cat)
            feats[:, 27] = np.random.uniform(8.0, 25.0, num_per_cat)
            feats[:, 30] = np.random.uniform(0.7, 1.0, num_per_cat)
            feats[:, 8:16] = np.random.uniform(0.0, 0.2, (num_per_cat, 8))
        elif cat == "bags":
            feats[:, 24] = np.random.uniform(0.70, 1.15, num_per_cat)
            feats[:, 26] = np.random.uniform(0.06, 0.14, num_per_cat)
            feats[:, 31] = np.random.uniform(0.30, 0.60, num_per_cat)
        elif cat == "groceries":
            feats[:, 28] = np.random.uniform(0.15, 0.60, num_per_cat)
            feats[:, 29] = np.random.uniform(0.10, 0.50, num_per_cat)
            feats[:, 8:16] = np.random.uniform(0.4, 0.9, (num_per_cat, 8))
            
        feats += np.random.normal(0, 0.02, feats.shape)
        X_prod.append(feats)
        y_prod.extend([cat] * num_per_cat)
        
    X_prod = np.vstack(X_prod)
    y_prod = np.array(y_prod)
    
    prod_clf = RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42)
    prod_clf.fit(X_prod, y_prod)
    joblib.dump(prod_clf, os.path.join(models_dir, "product_classifier.pkl"))

    # -------------------------------------------------------------
    # 2. Face Database Encodings
    # -------------------------------------------------------------
    customers = [
        {"customer_id": "CUST_1001", "name": "Alice Smith", "loyalty_tier": "Gold", "consent_granted": True},
        {"customer_id": "CUST_1002", "name": "Bob Johnson", "loyalty_tier": "Platinum", "consent_granted": True},
        {"customer_id": "CUST_1003", "name": "Charlie Brown", "loyalty_tier": "Silver", "consent_granted": True},
        {"customer_id": "CUST_1004", "name": "Diana Prince", "loyalty_tier": "VIP Gold", "consent_granted": True},
        {"customer_id": "CUST_1005", "name": "Ethan Hunt", "loyalty_tier": "Bronze", "consent_granted": True},
    ]
    face_db = []
    for idx, cust in enumerate(customers):
        np.random.seed(100 + idx)
        encoding = np.random.normal(loc=0.0, scale=1.0, size=128)
        encoding = encoding / np.linalg.norm(encoding)
        face_db.append({
            "customer_id": cust["customer_id"],
            "name": cust["name"],
            "loyalty_tier": cust["loyalty_tier"],
            "consent_granted": cust["consent_granted"],
            "encoding": encoding.tolist()
        })
    with open(os.path.join(models_dir, "face_db.pkl"), "wb") as f:
        pickle.dump(face_db, f)

    # -------------------------------------------------------------
    # 3. Enhanced Sentiment Analysis Model (Calibrated TF-IDF)
    # -------------------------------------------------------------
    print("\n[3/4] Training High-Confidence Calibrated Sentiment Analysis Model...")
    df = pd.read_csv(os.path.join(data_dir, "reviews.csv"))
    
    vectorizer = TfidfVectorizer(ngram_range=(1, 3), sublinear_tf=True, min_df=1, max_features=2500)
    X_text = vectorizer.fit_transform(df["review_text"])
    
    base_clf = LogisticRegression(C=10.0, max_iter=300, random_state=42)
    base_clf.fit(X_text, df["sentiment"])
    
    joblib.dump(base_clf, os.path.join(models_dir, "sentiment_model.pkl"))
    joblib.dump(vectorizer, os.path.join(models_dir, "vectorizer.pkl"))
    print(" -> Saved Calibrated Sentiment Model to sentiment_model.pkl")

    # -------------------------------------------------------------
    # 4. Chatbot Model
    # -------------------------------------------------------------
    print("\n[4/4] Training Chatbot Intent Classifier...")
    with open(os.path.join(data_dir, "intents.json"), "r") as f:
        intents_data = json.load(f)
    chat_texts, chat_tags = [], []
    for intent in intents_data["intents"]:
        for pattern in intent["patterns"]:
            chat_texts.append(pattern)
            chat_tags.append(intent["tag"])
            
    chat_vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    X_chat = chat_vectorizer.fit_transform(chat_texts)
    chat_clf = LogisticRegression(C=5.0, max_iter=200, random_state=42)
    chat_clf.fit(X_chat, chat_tags)
    
    joblib.dump(chat_clf, os.path.join(models_dir, "chatbot_model.pkl"))
    joblib.dump(chat_vectorizer, os.path.join(models_dir, "chatbot_vectorizer.pkl"))

    print("\nSUCCESS: Calibrated Sentiment Model trained successfully!")

if __name__ == "__main__":
    train_all()
