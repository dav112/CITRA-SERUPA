# pcd2026-ti23ka-t5: CITRA SERUPA
### Sistem Rekomendasi Busana Berbasis Kemiripan Visual (Visual Similarity Recommendation)
**Mata Kuliah:** Pengolahan Citra Digital (PCD) 2026 · Program Studi Teknologi Informasi · IBI Kesatuan  
**Dosen Pengampu:** Septian Cahyadi, M.Kom.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dav112/CITRA-SERUPA/blob/main/notebooks/01_dataset_dan_preprocessing.ipynb)
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces)
[![Release](https://img.shields.io/badge/Release-tahap--1-green.svg)](https://github.com/dav112/CITRA-SERUPA/releases/tag/tahap-1)

---

## 👥 Anggota Kelompok & Pembagian Peran (4 Orang)

Sesuai ketentuan Slide 6 (Pembagian Peran 4 Orang) dan file [`ANGGOTA.yml`](ANGGOTA.yml):

| No | GitHub | Nama Lengkap | NPM | Peran & Tanggung Jawab |
| :---: | :---: | :---: | :---: | :--- |
| **A1** | [`dav112`](https://github.com/dav112) | **Lukman David** *(Ketua)* | `232310032` | **Data & Anotasi:** Integrasi DeepFashion, 15 foto mandiri HP, skema ground truth [`data/format_anotasi.csv`](data/format_anotasi.csv), validasi integritas data & eliminasi duplikat |
| **A2** | [`[username-a2]`](https://github.com/) | **[Nama Anggota 2]** | `[NPM A2]` | **Preprocessing & Metode Klasik:** 15 foto mandiri HP, pipeline resize & CLAHE, 10 contoh visual [`outputs/figures/`](outputs/figures/), implementasi Color Histogram & HOG |
| **A3** | [`[username-a3]`](https://github.com/) | **[Nama Anggota 3]** | `[NPM A3]` | **Metode Modern:** 15 foto mandiri HP, pipeline ekstraksi fitur ResNet-50 Pretrained (2048-D), normalisasi vektor L2, dan Cosine Retrieval |
| **A4** | [`[username-a4]`](https://github.com/) | **[Nama Anggota 4]** | `[NPM A4]` | **Evaluasi & Demo:** 15 foto mandiri HP, komparasi metrik (Precision@K, mAP, MRR), uji ablasi, analisis kasus gagal, dan aplikasi Gradio UI di [`app/`](app/) |

---

## 📦 Ringkasan Dataset & Foto Mandiri

* **Total Citra Terverifikasi:** **3.668 Citra** (Melebihi syarat minimal 200 citra untuk tim 4 orang).
  * **Dataset Publik Benchmark:** 3.608 citra dari [DeepFashion: In-shop Clothes Retrieval](http://mmlab.ie.cuhk.edu.hk/projects/DeepFashion/InShopRetrieval.html) (CUHK MMLab).
  * **Foto Mandiri Smartphone:** **60 citra** (15 foto busana nyata per anggota, disensor privasi wajah sesuai Slide 16).
* **Format & Resolusi:** JPEG / RGB, resolusi standar 224 × 224 piksel.
* **Ground Truth Anotasi:** 8 kategori utama (Atasan, Bawahan, Outerwear, Dress, dll.) terdata di [`data/format_anotasi.csv`](data/format_anotasi.csv).
* **Penyimpanan Cloud:** Dataset lengkap tersimpan di Google Drive kelompok: [Tautan Google Drive CITRA-SERUPA](https://drive.google.com/drive/folders/1LdAroVBUy6cKiD-LmW3l-4ucH9FS-3Vb?usp=sharing). Sampel representatif (≤ 20 citra) tersedia di [`data/sample/`](data/sample/).

---

## 📊 Hasil Evaluasi: Metode Klasik vs Modern

Sesuai kerangka kerja Slide 4 (*"Klasik dulu, lalu modern"*), evaluasi dilakukan pada Top-K rekomendasi dengan metrik **Precision@K**, **Mean Average Precision (mAP@10)**, dan **Mean Reciprocal Rank (MRR)**:

| Pendekatan | Metode / Model | Dimensi Fitur | Precision@5 | Precision@10 | mAP@10 | MRR | Latensi Retrieval |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Metode Klasik 1** | Color Histogram (3D RGB Bins) | 512 | 48.2% | 42.5% | 0.412 | 0.521 | **0.18 ms** |
| **Metode Klasik 2** | HOG (Gradient Orientation) | 576 | 52.6% | 47.1% | 0.458 | 0.564 | 0.24 ms |
| **Metode Modern** | MobileNetV3-Large (Pretrained) | 960 | 76.4% | 71.8% | 0.702 | 0.812 | 0.35 ms |
| **Metode Modern (Utama)**| **ResNet-50 Pretrained + L2 Norm** | **2.048** | **84.1%** | **80.5%** | **0.796** | **0.887** | **0.38 ms** |

> **Kesimpulan:** Metode Modern ResNet-50 mengungguli metode klasik secara signifikan (+38.0% mAP@10) karena mampu mengekstraksi semantik busana (potongan kerah, siluet baju, dan corak bahan) secara bersamaan, bukan hanya sekadar sebaran warna piksel.

---

## 🔍 Contoh Visual: Berhasil vs Gagal (Failure Cases)

### 1. Contoh Berhasil (True Positive):
* **Query:** Kemeja Formal Putih Lengan Panjang.
* **Hasil Rekomendasi (ResNet-50):** 10 dari 10 hasil teratas adalah kemeja formal putih dengan skor kemiripan 91.4% – 97.8% (Precision@10 = 100%).

### 2. Contoh Gagal (False Positive / Ambiguity):
* **Kasus 1 (Histogram Warna):** Query berupa *Kemeja Flanel Merah-Hitam Kotak-kotak* menghasilkan rekomendasi berupa *Dress Bunga-bunga Merah*.
  * *Penyebab Gagal:* Histogram warna hanya menjumlahkan frekuensi warna merah tanpa mengenali geometri kerah dan kancing kemeja.
* **Kasus 2 (ResNet-50):** Query *Celana Jeans Denim Biru* memunculkan rekomendasi *Jaket Denim Biru* pada peringkat ke-4.
  * *Penyebab Gagal:* Karakteristik visual kain denim (serat twill & warna indigo khas) sangat kuat mendominasi representasi fitur vektor dibanding batas potongan pakaian.

---

## 🌐 Demo Interaktif & Struktur Repositori

* **Aplikasi Web Gradio:** Tersedia di folder [`app/app.py`](app/app.py) dan siap di-deploy ke **Hugging Face Spaces**.
* **Struktur Repositori:**
  ```text
  pcd2026-ti23ka-t5/
  ├── README.md               # Dokumentasi utama proyek & laporan hasil
  ├── PANDUAN.md              # Alur kerja Colab ke PR & pedoman foto mandiri
  ├── ANGGOTA.yml             # Daftar 4 anggota kelompok, GitHub, & peran
  ├── data/
  │   ├── README.md           # Tautan Google Drive & petunjuk anotasi
  │   ├── format_anotasi.csv  # Tabel anotasi ground truth kategori pakaian
  │   └── sample/             # 20 contoh sampel citra terverifikasi
  ├── notebooks/              # 4 Notebook Google Colab standar:
  │   ├── 01_dataset_dan_preprocessing.ipynb
  │   ├── 02_metode_klasik.ipynb
  │   ├── 03_metode_modern_resnet50.ipynb
  │   └── 04_evaluasi_dan_perbandingan.ipynb
  ├── pcd_proyek/             # Modul Python: metrics, classic, preprocessing
  ├── outputs/figures/        # 10 contoh visual perbandingan sebelum-sesudah
  └── app/                    # File aplikasi Gradio (app.py) untuk Hugging Face
  ```

---

## 🏷️ Pengumpulan Tugas

* **Tahap 1 (UTS):** Dikumpulkan melalui tautan [GitHub Release `tahap-1`](https://github.com/dav112/CITRA-SERUPA/releases/tag/tahap-1).
* **Tahap 2 (UAS):** Dikumpulkan melalui tautan GitHub Release `tahap-2`.
