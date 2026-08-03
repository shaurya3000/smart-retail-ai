import cv2
import numpy as np

def to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert BGR image to Grayscale."""
    if len(image.shape) == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def resize_image(image: np.ndarray, width: int = 128, height: int = 128) -> np.ndarray:
    """Resize image to targeted dimensions."""
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

def apply_blur(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """Apply Gaussian Blur to smooth out noise."""
    ksize = (kernel_size, kernel_size) if kernel_size % 2 == 1 else (kernel_size + 1, kernel_size + 1)
    return cv2.GaussianBlur(image, ksize, 0)

def detect_edges_canny(image: np.ndarray, threshold1: int = 50, threshold2: int = 150) -> np.ndarray:
    """Apply Canny edge detection."""
    gray = to_grayscale(image)
    return cv2.Canny(gray, threshold1, threshold2)

def detect_faces_haar(image: np.ndarray):
    """
    Detect face bounding boxes using OpenCV Haar Cascades.
    Returns list of tuples: [(x, y, w, h), ...]
    """
    gray = to_grayscale(image)
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return [(int(x), int(y), int(w), int(h)) for (x, y, w, h) in faces]

def extract_color_histogram(image: np.ndarray) -> np.ndarray:
    """
    Extract a normalized 3D color/texture feature vector for lightweight classification.
    """
    resized = resize_image(image, 64, 64)
    hist_b = cv2.calcHist([resized], [0], None, [16], [0, 256])
    hist_g = cv2.calcHist([resized], [1], None, [16], [0, 256])
    hist_r = cv2.calcHist([resized], [2], None, [16], [0, 256])
    features = np.concatenate([hist_b, hist_g, hist_r]).flatten()
    norm = np.linalg.norm(features)
    return features / norm if norm > 0 else features
