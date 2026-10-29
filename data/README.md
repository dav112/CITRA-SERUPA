# 📁 PANDUAN & SPESIFIKASI DATASET (DATA)

Direktori ini berisi sampel representatif citra katalog dan skema anotasi *ground truth* untuk evaluasi sistem pencarian citra serupa (*visual similarity retrieval*).

---

## 🔗 Tautan Penyimpanan Dataset Lengkap (Google Drive)

Sesuai aturan dosen (Slide 12 & 16), dataset lengkap berukuran besar **tidak di-commit ke repositori GitHub**, melainkan disimpan di Google Drive bersama dengan akses terbatas (hanya anggota tim dan dosen pengampu):

* **Tautan Google Drive Dataset Utama:**  
  [Folder Google Drive CITRA-SERUPA (Dataset & Features)](https://drive.google.com/drive/folders/1LdAroVBUy6cKiD-LmW3l-4ucH9FS-3Vb?usp=sharing)
* **Path di Lingkungan Google Colab:**  
  `/content/drive/MyDrive/CITRA-SERUPA/dataset/`

---

## 📊 Rincian Komposisi Dataset (Target Tim 4 Orang)

Berdasarkan ketentuan beban kerja Slide 5:
* **Total Citra Minimal:** 200 citra (Koleksi kita telah mencapai **3.608 citra** dari benchmark DeepFashion In-shop Clothes).
* **Foto Sendiri (15 Foto / Anggota):** 4 anggota x 15 = **60 foto pakaian nyata** dari smartphone masing-masing anggota.
* **Privasi & Keamanan:** Bagian wajah pada foto model / foto sendiri wajib disensor (blur/mosaic) sebelum dimasukkan ke dalam arsip dataset.

---

## 🏷️ Skema Anotasi Ground Truth (`format_anotasi.csv`)

Metrik evaluasi pada tahap UAS (*Precision@K, mAP@10, MRR*) membutuhkan label kebenaran dasar (*ground truth*) untuk menentukan apakah gambar yang direkomendasikan sistem benar-benar relevan dengan gambar yang dicari.

### Struktur Kolom `format_anotasi.csv`:
1. `image_id`: Nomor identifikasi unik citra (format: `IMG_0001`, `IMG_0002`, dst).
2. `filename`: Nama file gambar (contoh: `fashion_0001.jpg` atau `foto_lukman_01.jpg`).
3. `category`: Kategori utama busana (contoh: `Atasan`, `Bawahan`, `Gaun/Dress`, `Jaket/Outerwear`).
4. `subcategory`: Subkategori spesifik (contoh: `Kemeja Flanel`, `Celana Chino`, `Hoodie`, `Kaos Polos`).
5. `color`: Warna dominan pakaian (contoh: `Hitam`, `Putih`, `Biru Navy`, `Merah Marun`).
6. `pattern`: Motif pakaian (contoh: `Polos`, `Kotak-kotak`, `Garis-garis`, `Bunga-bunga`).
7. `source`: Asal dataset (`DeepFashion` atau `Foto_Mandiri`).
8. `contributor_github`: Username GitHub anggota yang mengambil foto (untuk foto mandiri) atau `katalog_dataset`.
