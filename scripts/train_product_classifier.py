import os
import sys
import numpy as np
import pickle
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "app", "models")
os.makedirs(MODELS_DIR, exist_ok=True)

def generate_dataset():
    """
    Generates a realistic 32-dimensional feature dataset representing 5 retail categories:
    0: clothing, 1: shoes, 2: electronics, 3: bags, 4: groceries
    """
    np.random.seed(42)
    n_samples_per_class = 200
    
    X = []
    y = []

    classes = ["clothing", "shoes", "electronics", "bags", "groceries"]

    for class_idx, class_name in enumerate(classes):
        for _ in range(n_samples_per_class):
            # 32 Features:
            # 0..7: Hue Hist, 8..15: Sat Hist, 16..23: Val Hist
            # 24: Aspect Ratio, 25: Sole Contrast, 26: Edge Density, 27: Green Ratio, 28: Red Ratio, 29..31: Brightness
            
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
            extra = 0.0

            if class_name == "electronics":
                # Laptops, phones, screens: metallic/dark V hist, high edge density, neutral aspect ratio
                v_hist = np.array([0.4, 0.3, 0.1, 0.05, 0.05, 0.05, 0.03, 0.02])
                s_hist = np.array([0.5, 0.3, 0.1, 0.05, 0.02, 0.01, 0.01, 0.01]) # Low saturation
                aspect_ratio = np.random.uniform(1.1, 1.8)
                edge_density = np.random.uniform(0.08, 0.25) # Key feature: straight line edges
                green_ratio = np.random.uniform(0.0, 0.02)
                red_ratio = np.random.uniform(0.0, 0.02)
                
            elif class_name == "groceries":
                # Produce, vegetables, fruits: high green/red saturation, organic texture
                s_hist = np.array([0.02, 0.05, 0.1, 0.2, 0.3, 0.2, 0.1, 0.03]) # High saturation
                aspect_ratio = np.random.uniform(0.9, 1.5)
                edge_density = np.random.uniform(0.02, 0.12)
                green_ratio = np.random.uniform(0.15, 0.60) # Key feature: high green produce
                red_ratio = np.random.uniform(0.10, 0.50)   # Key feature: high red produce
                
            elif class_name == "shoes":
                # Sneakers, boots: wide elongated aspect ratio (w > h), sole contrast
                aspect_ratio = np.random.uniform(1.35, 2.2) # Key feature: horizontal footwear shape
                sole_contrast = np.random.uniform(0.35, 0.70) # Dark sole vs upper
                edge_density = np.random.uniform(0.04, 0.12)
                green_ratio = np.random.uniform(0.0, 0.02)
                
            elif class_name == "bags":
                # Backpacks, totes: tall vertical aspect ratio (w < h), strap edges
                aspect_ratio = np.random.uniform(0.55, 0.88) # Key feature: vertical bag height
                edge_density = np.random.uniform(0.03, 0.10)
                green_ratio = np.random.uniform(0.0, 0.03)
                
            elif class_name == "clothing":
                # Shirts, jackets, garments: mid-range balanced aspect ratio and texture
                aspect_ratio = np.random.uniform(0.85, 1.15)
                edge_density = np.random.uniform(0.02, 0.07)
                green_ratio = np.random.uniform(0.0, 0.05)

            feat_vec = np.concatenate([
                h_hist, s_hist, v_hist,
                [aspect_ratio, sole_contrast, edge_density, green_ratio, red_ratio, top_bright, bot_bright, extra]
            ])
            
            X.append(feat_vec)
            y.append(class_idx)

    return np.array(X), np.array(y), classes

def train_and_save():
    X, y, classes = generate_dataset()
    print(f"[Training Product Classifier] Dataset shape: X={X.shape}, y={y.shape}")

    clf = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42)
    clf.fit(X, y)

    y_pred = clf.predict(X)
    acc = accuracy_score(y, y_pred)
    print(f"[Training Product Classifier] Training Accuracy: {acc * 100:.2f}%")

    model_path = os.path.join(MODELS_DIR, "product_classifier.pkl")
    meta_path = os.path.join(MODELS_DIR, "product_classifier_meta.pkl")

    joblib.dump(clf, model_path)
    with open(meta_path, "wb") as f:
        pickle.dump({"classes": classes}, f)

    print(f"SUCCESS: Saved product classifier model to {model_path}")

if __name__ == "__main__":
    train_and_save()
