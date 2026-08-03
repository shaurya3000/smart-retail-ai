import os
import sys
import numpy as np
import pickle
import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.metrics import accuracy_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "app", "models")
os.makedirs(MODELS_DIR, exist_ok=True)

def generate_large_dataset():
    """
    Generates a 5,000-sample dataset (1,000 samples per category) with enriched features
    specifically tuned for Shoes, Electronics, Groceries, Bags, and Clothing.
    """
    np.random.seed(42)
    n_samples_per_class = 1000
    classes = ["clothing", "shoes", "electronics", "bags", "groceries"]
    
    X = []
    y = []

    for class_idx, class_name in enumerate(classes):
        for _ in range(n_samples_per_class):
            # 32 Features:
            # 0..7: Hue Hist, 8..15: Sat Hist, 16..23: Val Hist
            # 24: Aspect Ratio, 25: Sole Contrast, 26: Edge Density, 27: Green Ratio, 28: Red Ratio, 29: Top Bright, 30: Bot Bright, 31: Blue Ratio
            
            h_hist = np.random.dirichlet(np.ones(8))
            s_hist = np.random.dirichlet(np.ones(8))
            v_hist = np.random.dirichlet(np.ones(8))
            
            aspect_ratio = 1.0
            sole_contrast = 0.2
            edge_density = 0.05
            green_ratio = 0.01
            red_ratio = 0.01
            top_bright = 0.5
            bot_bright = 0.5
            blue_ratio = 0.01

            if class_name == "electronics":
                # Laptops, MacBooks, Smartphones, Monitors, Keyboards:
                # Wide aspect ratio (1.1 - 1.9), high keyboard/screen edge density (0.05 - 0.35), low saturation (metallic/black)
                v_hist = np.array([0.45, 0.25, 0.10, 0.05, 0.05, 0.04, 0.03, 0.03])
                s_hist = np.array([0.60, 0.20, 0.10, 0.04, 0.03, 0.01, 0.01, 0.01]) # Very low saturation
                aspect_ratio = np.random.uniform(1.10, 1.90)
                edge_density = np.random.uniform(0.05, 0.35) # High straight edge density from keys & screens
                sole_contrast = np.random.uniform(0.05, 0.25)
                green_ratio = np.random.uniform(0.0, 0.02)
                red_ratio = np.random.uniform(0.0, 0.02)
                blue_ratio = np.random.uniform(0.02, 0.25) # Screen blue light
                
            elif class_name == "shoes":
                # Sneakers, Boots, Loafers, Running Shoes, Heels:
                # Elongated footwear aspect ratio (1.25 - 2.5), high sole-to-upper contrast (0.35 - 0.85)
                aspect_ratio = np.random.uniform(1.25, 2.50) # Key footwear shape
                sole_contrast = np.random.uniform(0.35, 0.85) # High sole contrast
                edge_density = np.random.uniform(0.03, 0.15)
                green_ratio = np.random.uniform(0.0, 0.03)
                red_ratio = np.random.uniform(0.0, 0.05)
                top_bright = np.random.uniform(0.3, 0.8)
                bot_bright = np.random.uniform(0.1, 0.4) # Darker sole base
                
            elif class_name == "groceries":
                # Vegetables, produce, apples, bananas, market crates:
                # High green/red produce saturation
                s_hist = np.array([0.02, 0.05, 0.1, 0.2, 0.3, 0.2, 0.1, 0.03])
                aspect_ratio = np.random.uniform(0.85, 1.45)
                edge_density = np.random.uniform(0.02, 0.12)
                green_ratio = np.random.uniform(0.12, 0.65) # Produce green
                red_ratio = np.random.uniform(0.08, 0.55)   # Produce red
                sole_contrast = np.random.uniform(0.05, 0.25)
                
            elif class_name == "bags":
                # Backpacks, totes, purses, luggage:
                # Tall vertical aspect ratio (0.55 - 0.88), strap contours
                aspect_ratio = np.random.uniform(0.55, 0.88)
                edge_density = np.random.uniform(0.03, 0.12)
                sole_contrast = np.random.uniform(0.1, 0.3)
                green_ratio = np.random.uniform(0.0, 0.03)
                
            elif class_name == "clothing":
                # Shirts, jackets, coats, garments:
                # Medium square/vertical ratio (0.85 - 1.20), soft fabric contrast
                aspect_ratio = np.random.uniform(0.85, 1.20)
                edge_density = np.random.uniform(0.01, 0.08)
                sole_contrast = np.random.uniform(0.05, 0.30)
                green_ratio = np.random.uniform(0.0, 0.05)

            # Add minor random noise for realistic variance
            noise = np.random.normal(0, 0.01, 32)
            feat_vec = np.concatenate([
                h_hist, s_hist, v_hist,
                [aspect_ratio, sole_contrast, edge_density, green_ratio, red_ratio, top_bright, bot_bright, blue_ratio]
            ]) + noise
            
            X.append(feat_vec)
            y.append(class_idx)

    return np.array(X), np.array(y), classes

def train_ensemble_model():
    X, y, classes = generate_large_dataset()
    print(f"[Ensemble Trainer] Large Dataset generated: X={X.shape}, y={y.shape}")

    rf = RandomForestClassifier(n_estimators=200, max_depth=16, random_state=42)
    gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)

    ensemble = VotingClassifier(estimators=[('rf', rf), ('gb', gb)], voting='soft')
    ensemble.fit(X, y)

    y_pred = ensemble.predict(X)
    acc = accuracy_score(y, y_pred)
    print(f"[Ensemble Trainer] Ensemble Model Accuracy: {acc * 100:.2f}%")

    model_path = os.path.join(MODELS_DIR, "product_classifier.pkl")
    meta_path = os.path.join(MODELS_DIR, "product_classifier_meta.pkl")

    joblib.dump(ensemble, model_path)
    with open(meta_path, "wb") as f:
        pickle.dump({"classes": classes, "n_samples": len(X), "accuracy": acc}, f)

    print(f"SUCCESS: Saved 5,000-sample trained ML Ensemble model to {model_path}")

if __name__ == "__main__":
    train_ensemble_model()
