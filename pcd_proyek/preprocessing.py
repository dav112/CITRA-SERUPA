import os
import numpy as np
from PIL import Image

def load_and_verify_image(image_path):
    """
    Membaca dan memverifikasi integritas file citra.
    Mengembalikan objek PIL Image jika valid, atau None jika korup.
    """
    if not os.path.exists(image_path):
        return None
    try:
        with Image.open(image_path) as img:
            img.verify()
        return Image.open(image_path).convert("RGB")
    except Exception:
        return None

def preprocess_image(image_input, target_size=(224, 224)):
    """
    Pipeline preprocessing standar:
    1. Konversi ke mode RGB
    2. Resize berkualitas tinggi (LANCZOS) ke target 224x224
    3. Normalisasi skala piksel 0..1 dan standar ImageNet
    """
    if isinstance(image_input, str):
        img = Image.open(image_input).convert("RGB")
    elif isinstance(image_input, Image.Image):
        img = image_input.convert("RGB")
    else:
        img = Image.fromarray(np.uint8(image_input)).convert("RGB")
        
    img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
    arr = np.array(img_resized, dtype=np.float32) / 255.0
    
    # Standarisasi nilai mean & std ImageNet
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    normalized_arr = (arr - mean) / std
    
    return img_resized, normalized_arr
