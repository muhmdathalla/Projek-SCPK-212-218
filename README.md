```markdown
# 🌾 Sistem Pendukung Keputusan Pemilihan Pupuk Tanaman Padi — Metode SAW

Aplikasi **Sistem Pendukung Keputusan (SPK)** berbasis web ini dibangun menggunakan **Streamlit** untuk menganalisis dan menentukan pupuk atau rekomendasi kondisi lahan terbaik bagi penanaman tanaman padi. Proyek ini memenuhi ketentuan Proyek Akhir Praktikum **Sistem Pendukung Keputusan (SCPK) 2025/2026** di **UPN "Veteran" Yogyakarta**.

---

## 👥 Profil Kelompok
* **Muhammad Athalla Bagaskara** (NIM: *[Isi NIM Lu di Sini]*) - UPN "Veteran" Yogyakarta
* **Muhammad Ridho Hikmatul Maulana** (NIM: 123240218) - Anggota Kelompok 2

---

## 📊 Ringkasan Proyek
* **Metode SPK:** *Simple Additive Weighting* (SAW)
* **Dataset:** *Crop Recommendation Dataset* (Sumber: Kaggle - atharvaingle), disaring khusus untuk optimasi komparatif atau pelabelan kondisi alternatif dengan total data acuan yang komprehensif (2.200 baris total dataset).
* **Jumlah Kriteria:** 7 Kriteria Fisik & Kimiawi Lingkungan.

### 📐 Kriteria & Bobot Awal
Aplikasi ini mengevaluasi alternatif berdasarkan 7 kriteria utama yang krusial bagi pertumbuhan padi:
1.  **N (Nitrogen):** Kandungan nitrogen dalam tanah.
2.  **P (Phosfor):** Kandungan fosfor dalam tanah.
3.  **K (Kalium):** Kandungan kalium dalam tanah.
4.  **Temperature:** Suhu lingkungan (°C).
5.  **Humidity:** Kelembapan udara (%).
6.  **pH:** Tingkat keasaman tanah.
7.  **Rainfall:** Curah hujan (mm).

---

## 🚀 Fitur Utama Aplikasi
Sesuai dengan **Panduan Teknis Proyek Akhir SCPK**, antarmuka Streamlit ini dilengkapi dengan:

1.  **Navigasi Layout Terstruktur:** Menggunakan sidebar/tabs yang memisahkan halaman informasi data, proses perhitungan SPK, dan profil tim.
2.  **Tampilan Dataset Interaktif:** Menampilkan data mentah dari `dataset_pupuk.csv` secara rapi menggunakan `st.dataframe`.
3.  **Input Bobot Dinamis:** Menyediakan widget interaktif (*Slider / Number Input*) agar asisten praktikum atau pengguna dapat mengubah bobot preferensi kriteria secara *real-time*.
4.  **Tombol Eksekusi (*Trigger*):** Proses kalkulasi matriks keputusan, normalisasi, dan peringan tidak berjalan otomatis, melainkan dipicu secara eksplisit menggunakan `st.button` untuk efisiensi komputasi.
5.  **Visualisasi Data Analitik Terintegrasi:** Dilengkapi minimal **3 jenis grafik berbeda** menggunakan *Matplotlib / Seaborn* untuk menganalisis distribusi kriteria dan hasil preferensi (syarat wajib jika mengambil metode SAW/WP).

---

## 🧮 Alur Perhitungan Metode SAW dalam Kode
Metode *Simple Additive Weighting* (SAW) sering dikenal sebagai metode penjumlahan terbobot. Langkah-langkah matematis yang diimplementasikan di dalam `SAW_Pupuk.py` meliputi:

1.  **Pembentukan Matriks Keputusan ($X$):** Mengambil nilai kriteria dari dataset untuk setiap alternatif yang diuji.
2.  **Normalisasi Matriks ($R$):**
    * Untuk kriteria **Benefit** (Keuntungan): 
        $$r_{ij} = \frac{x_{ij}}{\max(x_{ij})}$$
    * Untuk kriteria **Cost** (Biaya/Kerugian): 
        $$r_{ij} = \frac{\min(x_{ij})}{x_{ij}}$$
3.  **Proses Nilai Preferensi ($V$):** Mengalikan matriks yang telah dinormalisasi dengan bobot dinamis ($W$) yang diinput oleh user melalui antarmuka Streamlit:
        $$V_i = \sum_{j=1}^{n} w_j \cdot r_{ij}$$
4.  **Perangkingan:** Mengurutkan nilai $V_i$ dari yang tertinggi ke terendah untuk menentukan alternatif terbaik.

---

## 📁 Struktur Repositori
```bash
├── README.md               # Dokumentasi proyek (File ini)
├── SAW_Pupuk.py            # Main script Python untuk aplikasi GUI Streamlit
├── dataset_pupuk.csv       # Dataset kondisi tanah & rekomendasi (format .csv)
└── Laporan_Proyek_Akhir.pdf # Laporan resmi proyek akhir SCPK
