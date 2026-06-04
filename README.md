# 🌾 SPK Evaluasi Lahan & Nutrisi Optimal Lahan Padi (Metode SAW)

Aplikasi Sistem Pendukung Keputusan (SPK) berbasis web untuk menentukan, mengevaluasi, dan meranking kondisi lahan serta nutrisi optimal yang paling sesuai untuk budidaya tanaman padi (*Rice*). Sistem ini dibangun menggunakan metode **Simple Additive Weighting (SAW)** dan diimplementasikan secara interaktif menggunakan framework **Streamlit** (Python).

Proyek ini disusun sebagai bagian dari luaran **Praktikum Sistem Pendukung Keputusan (SCPK) Tahun Akademik 2025/2026**.

---

## 👥 Profil Kelompok
* **Universitas:** UPN "Veteran" Yogyakarta  
* **Program Studi:** Informatika / Geoinformatika / Sistem Pendukung Keputusan  
* **Kelompok:** 2  
* **Anggota Kelompok:**
  1. Muhammad Athalla Bagaskara (NIM: 123240212)
  2. Muhammad Ridho Hikmatul Maulana (NIM: 123240218)

---

## 🎯 Fitur Utama Aplikasi

1. **🏠 Beranda & Dashboard Interaktif**
   * Ringkasan statistik dataset (Total sampel, jumlah kriteria, metode SPK).
   * Panel rumus matematis metode SAW sebagai transparansi perhitungan sistem.
   * Tabel parameter kriteria lengkap beserta satuan pengukurannya.

2. **📊 Manajemen Dataset & Kriteria Dinamis**
   * Integrasi langsung dengan dataset pertanian (terfilter otomatis khusus tanaman padi).
   * **Tipe Kriteria Dinamis:** Pengguna dapat mengubah status kriteria (`Benefit` atau `Cost`) melalui *dropdown* web secara langsung, dan mesin kalkulasi SAW akan beradaptasi otomatis secara *real-time*.
   * **Operasi Data Alternatif (CRUD):** Fitur untuk menambah baris alternatif lahan baru atau menghapus sampel data yang *outlier*/rusak langsung dari aplikasi web.
   * Menampilkan ringkasan statistik deskriptif data lahan.
   * Tautan langsung ke sumber data asli di Kaggle.

3. **⚙️ Kalkulasi Akurat Metode SPK-SAW**
   * Bobot kriteria yang sepenuhnya fleksibel dapat diatur via *slider* pada sidebar.
   * Matriks Keputusan ($X$), Matriks Normalisasi ($R$), dan Hasil Nilai Preferensi ($V$) ditampilkan secara transparan langkah demi langkah.
   * **Rekomendasi Visual (Podium):** Menampilkan 3 alternatif kondisi lahan terbaik dalam bentuk visual *card* medali emas, perak, dan perunggu.
   * **Fitur Unduh (Download):** Mengekspor hasil perangkingan penuh ke dalam format **CSV** dan **Excel (.xls)** secara instan yang langsung rapi terbagi per kolom (*auto-detect separators*).

4. **📈 Visualisasi & Analitik Data**
   * **Grafik 1:** Distribusi nilai preferensi preferensi SAW dan rata-rata peringkat horizontal.
   * **Grafik 2:** Proporsi kontribusi bobot kriteria aktif (*Pie & Bar Chart*).
   * **Grafik 3:** Sebaran data mentah parameter lingkungan menggunakan *Boxplot*.
   * **Grafik 4:** *Radar Chart (Spider Web)* untuk membandingkan kecocokan profil lahan vs bobot aktif.
   * **Grafik 5:** *Heatmap* Korelasi Pearson antar kriteria terhadap nilai akhir SAW.
   * **Grafik 6:** *Scatter Plot* pintar yang melacak sebaran top 10% alternatif lahan terbaik secara dinamis.

---

## 📊 Spesifikasi Kriteria & Parameter

Sistem mengevaluasi alternatif lahan berdasarkan 7 parameter lingkungan utama dengan standar satuan berikut:

| Kriteria | Parameter Lingkungan | Satuan | Deskripsi Kontrol |
| :--- | :--- | :---: | :--- |
| **N** | Nitrogen | mg/kg | Kandungan hara Nitrogen dalam tanah |
| **P** | Fosfor | mg/kg | Kandungan hara Fosfor dalam tanah |
| **K** | Kalium | mg/kg | Kandungan hara Kalium dalam tanah |
| **temperature**| Suhu Lahan | °C | Suhu udara di sekitar area lahan |
| **humidity** | Kelembaban | % | Tingkat kelembaban udara relatif |
| **ph** | pH Tanah | — | Tingkat keasaman atau kebasaan tanah |
| **rainfall** | Curah Hujan | mm | Intensitas curah hujan tahunan |

---

## 🧮 Alur Perhitungan Metode SAW

### 1. Normalisasi Matriks ($R$)
Normalisasi dilakukan secara dinamis berdasarkan tipe kriteria yang dipilih oleh user:
* **Kriteria Benefit** (Semakin besar nilai semakin baik):
  $$r_{ij} = \frac{x_{ij}}{\max_{i}(x_{ij})}$$
* **Kriteria Cost** (Semakin kecil nilai semakin baik):
  $$r_{ij} = \frac{\min_{i}(x_{ij})}{x_{ij}}$$

### 2. Nilai Preferensi ($V$)
Menghitung total bobot preferensi untuk setiap baris alternatif lahan:
$$V_i = \sum_{j=1}^{n} w_j \cdot r_{ij}$$
*Di mana $w_j$ adalah bobot ternormalisasi dari slider kriteria ($\sum w_j = 1$). Alternatif dengan nilai $V_i$ tertinggi merupakan lahan yang paling optimal.*

---

## 🛠️ Langkah Instalasi & Menjalankan Aplikasi Lokally

Pastikan komputer/laptop Anda telah terpasang **Python 3.8+**. Ikuti instruksi perintah terminal di bawah ini:

### 1. Clone Repositori
```bash
git clone [https://github.com/username-kamu/nama-repo-kamu.git](https://github.com/username-kamu/nama-repo-kamu.git)
cd nama-repo-kamu
