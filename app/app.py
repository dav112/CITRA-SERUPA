import os
import glob
import numpy as np
import pandas as pd
from PIL import Image
import gradio as gr
import torch
import torch.nn as nn
from torchvision import models, transforms

# 1. Konfigurasi Device & Preprocessing
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform_pipeline = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 2. Inisialisasi Model ResNet-50 Pretrained
print(f"Memuat model ResNet-50 pada {device}...")
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.fc = nn.Identity()  # Ambil vektor fitur 2048 dimensi
model = model.to(device)
model.eval()

# 3. Direktori Katalog Sampel
sample_dir = os.path.join(os.path.dirname(__file__), "..", "data", "sample")
if not os.path.exists(sample_dir):
    sample_dir = os.path.join(os.path.dirname(__file__), "sample")

# Ekstraksi fitur embedding katalog sampel saat aplikasi pertama start
catalog_images = []
catalog_embeddings = []
catalog_names = []

image_files = sorted(glob.glob(os.path.join(sample_dir, "*.jpg")) + glob.glob(os.path.join(sample_dir, "*.jpeg")) + glob.glob(os.path.join(sample_dir, "*.png")))

print(f"Menyiapkan {len(image_files)} citra katalog...")
for img_path in image_files:
    try:
        pil_img = Image.open(img_path).convert("RGB")
        tensor = transform_pipeline(pil_img).unsqueeze(0).to(device)
        with torch.no_grad():
            feat = model(tensor).cpu().numpy().flatten()
            norm = np.linalg.norm(feat)
            if norm > 0:
                feat = feat / norm
        catalog_images.append(pil_img)
        catalog_embeddings.append(feat)
        catalog_names.append(os.path.basename(img_path))
    except Exception as e:
        print(f"Error memproses {img_path}: {e}")

if len(catalog_embeddings) > 0:
    catalog_embeddings = np.vstack(catalog_embeddings)
else:
    catalog_embeddings = np.empty((0, 2048))

# 4. Fungsi Rekomendasi Citra Serupa
def search_similar_clothing(query_img, top_k=6):
    if query_img is None:
        return None, "Silakan unggah foto busana terlebih dahulu."
    
    if len(catalog_embeddings) == 0:
        return None, "Katalog gambar belum tersedia."
        
    # Ekstraksi fitur citra query
    if not isinstance(query_img, Image.Image):
        query_img = Image.fromarray(query_img).convert("RGB")
    else:
        query_img = query_img.convert("RGB")
        
    query_tensor = transform_pipeline(query_img).unsqueeze(0).to(device)
    with torch.no_grad():
        query_feat = model(query_tensor).cpu().numpy().flatten()
        norm = np.linalg.norm(query_feat)
        if norm > 0:
            query_feat = query_feat / norm
            
    # Hitung Cosine Similarity via Dot Product
    scores = np.dot(catalog_embeddings, query_feat)
    top_indices = np.argsort(scores)[::-1][:top_k]
    
    results = []
    summary_text = "### 🎯 Hasil Analisis Rekomendasi:\n"
    for rank, idx in enumerate(top_indices, 1):
        score_pct = float(scores[idx] * 100)
        img = catalog_images[idx]
        name = catalog_names[idx]
        caption = f"Peringkat #{rank} | Kemiripan: {score_pct:.1f}%\n({name})"
        results.append((img, caption))
        summary_text += f"- **#{rank}** `{name}`: Kemiripan **{score_pct:.1f}%**\n"
        
    return results, summary_text

# 5. Desain Antarmuka Gradio
theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="slate"
)

with gr.Blocks(theme=theme, title="Citra Serupa - Visual Clothing Retrieval") as demo:
    gr.Markdown(
        """
        # 👗 CITRA SERUPA: Sistem Rekomendasi Pakaian
        ### Pengolahan Citra Digital (PCD) 2026 · IBI Kesatuan · Topik T5
        Unggah foto pakaian Anda (dari HP atau laptop), dan sistem AI berbasis **ResNet-50 Deep Learning** akan mencari busana paling serupa dari basis data.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=4):
            input_image = gr.Image(type="pil", label="📸 Unggah / Ambil Foto Pakaian (Query)")
            top_k_slider = gr.Slider(minimum=1, maximum=12, value=6, step=1, label="Banyaknya Rekomendasi (Top-K)")
            btn_search = gr.Button("🔍 Cari Pakaian Serupa", variant="primary", size="lg")
            
        with gr.Column(scale=6):
            output_gallery = gr.Gallery(
                label="✨ Rekomendasi Busana Paling Mirip",
                columns=3,
                rows=2,
                height="auto",
                object_fit="contain"
            )
            output_info = gr.Markdown("Unggah gambar di sebelah kiri lalu klik tombol cari.")
            
    btn_search.click(
        fn=search_similar_clothing,
        inputs=[input_image, top_k_slider],
        outputs=[output_gallery, output_info]
    )

if __name__ == "__main__":
    demo.launch()
