import numpy as np
from PIL import Image

def extract_color_histogram(image_input, bins=(8, 8, 8)):
    """
    Metode Klasik 1: Ekstraksi Histogram Warna 3D RGB.
    Menghasilkan vektor fitur warna terdistribusi dan dinormalisasi L2.
    """
    if isinstance(image_input, str):
        img = Image.open(image_input).convert("RGB")
    elif isinstance(image_input, Image.Image):
        img = image_input.convert("RGB")
    else:
        img = Image.fromarray(np.uint8(image_input)).convert("RGB")
        
    img_arr = np.array(img, dtype=np.uint8)
    
    # Hitung histogram 3D untuk saluran R, G, B
    hist, _ = np.histogramdd(
        img_arr.reshape(-1, 3),
        bins=bins,
        range=[(0, 256), (0, 256), (0, 256)]
    )
    
    # Ratakan dan normalisasi L2
    hist_vec = hist.flatten().astype(np.float32)
    norm = np.linalg.norm(hist_vec)
    if norm > 0:
        hist_vec /= norm
    return hist_vec

def extract_hog_features(image_input, cell_size=16, num_bins=9):
    """
    Metode Klasik 2: Ekstraksi Histogram of Oriented Gradients (HOG) Sederhana.
    Menangkap representasi gradien tepi, bentuk, dan kontur busana.
    """
    if isinstance(image_input, str):
        img = Image.open(image_input).convert("L")
    elif isinstance(image_input, Image.Image):
        img = image_input.convert("L")
    else:
        img = Image.fromarray(np.uint8(image_input)).convert("L")
        
    img = img.resize((128, 128))
    arr = np.array(img, dtype=np.float32)
    
    # Hitung gradien Sobel sederhana
    gx = np.zeros_like(arr)
    gy = np.zeros_like(arr)
    gx[:, 1:-1] = arr[:, 2:] - arr[:, :-2]
    gy[1:-1, :] = arr[2:, :] - arr[:-2, :]
    
    magnitude = np.sqrt(gx**2 + gy**2)
    orientation = (np.arctan2(gy, gx) * (180.0 / np.pi)) % 180.0
    
    # Hitung histogram gradien per sel
    h, w = arr.shape
    histograms = []
    bin_width = 180.0 / num_bins
    
    for y in range(0, h, cell_size):
        for x in range(0, w, cell_size):
            cell_mag = magnitude[y:y+cell_size, x:x+cell_size]
            cell_ori = orientation[y:y+cell_size, x:x+cell_size]
            
            bin_idx = np.floor(cell_ori / bin_width).astype(int) % num_bins
            cell_hist = np.zeros(num_bins, dtype=np.float32)
            
            for b in range(num_bins):
                cell_hist[b] = np.sum(cell_mag[bin_idx == b])
                
            norm = np.linalg.norm(cell_hist)
            if norm > 0:
                cell_hist /= norm
            histograms.extend(cell_hist)
            
    hog_vec = np.array(histograms, dtype=np.float32)
    total_norm = np.linalg.norm(hog_vec)
    if total_norm > 0:
        hog_vec /= total_norm
    return hog_vec
