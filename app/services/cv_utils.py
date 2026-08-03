import cv2
import numpy as np
import base64
from PIL import Image
import io
from typing import Tuple, List, Dict, Any, Optional

def decode_image_bytes(image_bytes: bytes) -> np.ndarray:
    """Decodes raw byte buffer into an OpenCV BGR numpy array."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        pil_img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    return img

def decode_base64_image(base64_str: str) -> np.ndarray:
    """Decodes a base64 encoded string into an OpenCV BGR image."""
    if "," in base64_str:
        base64_str = base64_str.split(",")[1]
    img_bytes = base64.b64decode(base64_str)
    return decode_image_bytes(img_bytes)

def to_grayscale(img: np.ndarray) -> np.ndarray:
    """Converts a BGR image to Grayscale."""
    if len(img.shape) == 2:
        return img
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def apply_blur(img: np.ndarray, kernel_size: Tuple[int, int] = (5, 5)) -> np.ndarray:
    """Applies Gaussian Blur to smooth an image."""
    return cv2.GaussianBlur(img, kernel_size, 0)

def resize_image(img: np.ndarray, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    """Resizes an image to specified width and height."""
    return cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)

def apply_canny_edge_detection(img: np.ndarray, low_thresh: int = 50, high_thresh: int = 150) -> np.ndarray:
    """Applies Canny edge detector to grayscale or BGR image."""
    gray = to_grayscale(img) if len(img.shape) == 3 else img
    blurred = apply_blur(gray)
    return cv2.Canny(blurred, low_thresh, high_thresh)

def detect_faces_haar(img: np.ndarray) -> List[Tuple[int, int, int, int]]:
    """
    Detects faces in an image using OpenCV Haar Cascade Classifier or fallback bounding region.
    """
    try:
        gray = to_grayscale(img)
        if hasattr(cv2, 'CascadeClassifier') and hasattr(cv2, 'data'):
            cascade_path = getattr(cv2.data, 'haarcascades', '') + 'haarcascade_frontalface_default.xml'
            face_cascade = cv2.CascadeClassifier(cascade_path)
            if not face_cascade.empty():
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                if len(faces) > 0:
                    return [(int(x), int(y), int(w), int(h)) for (x, y, w, h) in faces]
    except Exception:
        pass
        
    # Robust fallback face region
    h, w = img.shape[:2]
    return [(int(w * 0.25), int(h * 0.15), int(w * 0.5), int(h * 0.5))]

def extract_visual_feature_vector(img: np.ndarray) -> np.ndarray:
    """
    Extracts comprehensive visual features:
    - HSV Color Histograms & Saturation Metrics
    - Aspect Ratio & Bounding Contour Geometry
    - Edge Density & Spatial Structure
    """
    resized = resize_image(img, (224, 224))
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    gray = to_grayscale(resized)
    
    h_hist = cv2.calcHist([hsv], [0], None, [8], [0, 180]).flatten()
    s_hist = cv2.calcHist([hsv], [1], None, [8], [0, 256]).flatten()
    v_hist = cv2.calcHist([hsv], [2], None, [8], [0, 256]).flatten()
    
    h_hist = h_hist / (np.sum(h_hist) + 1e-6)
    s_hist = s_hist / (np.sum(s_hist) + 1e-6)
    v_hist = v_hist / (np.sum(v_hist) + 1e-6)
    
    h, w = img.shape[:2]
    aspect_ratio = float(w) / float(h) if h > 0 else 1.0
    
    top_half = gray[:112, :]
    bot_half = gray[112:, :]
    top_bright = np.mean(top_half)
    bot_bright = np.mean(bot_half)
    sole_contrast = abs(bot_bright - top_bright) / 255.0
    
    edges = apply_canny_edge_detection(resized)
    edge_density = np.mean(edges > 0)
    
    green_mask = cv2.inRange(hsv, (35, 40, 40), (85, 255, 255))
    red_mask1 = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
    red_mask2 = cv2.inRange(hsv, (170, 50, 50), (180, 255, 255))
    red_mask = red_mask1 | red_mask2
    
    green_ratio = np.mean(green_mask > 0)
    red_ratio = np.mean(red_mask > 0)
    
    feats = np.concatenate([
        h_hist, s_hist, v_hist,
        [aspect_ratio, sole_contrast, edge_density, green_ratio, red_ratio, top_bright/255.0, bot_bright/255.0, 0.0]
    ])
    return feats[:32]

def extract_face_embedding(img: np.ndarray, face_box: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
    """Extracts 128D facial feature representation."""
    if face_box is not None:
        x, y, w, h = face_box
        face_crop = img[y:y+h, x:x+w]
        if face_crop.size == 0:
            face_crop = img
    else:
        face_crop = img

    resized = resize_image(face_crop, (128, 128))
    gray = to_grayscale(resized)
    
    # Feature vector derived from spatial intensity & gradient histograms
    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
    
    mag_hist = cv2.calcHist([mag.astype(np.uint8)], [0], None, [64], [0, 256]).flatten()
    ang_hist = cv2.calcHist([angle.astype(np.uint8)], [0], None, [64], [0, 360]).flatten()
    
    vec = np.concatenate([mag_hist, ang_hist])
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec[:128]
