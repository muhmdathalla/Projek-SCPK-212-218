# 🌾 Sistem Pendukung Keputusan Penentuan Kondisi Lahan dan Nutrisi Optimal untuk Budidaya Tanaman Padi Menggunakan Metode SAW

Aplikasi **Sistem Pendukung Keputusan (SPK)** berbasis web ini dibangun menggunakan **Streamlit** untuk mengevaluasi, menganalisis, dan menentukan peringkat kondisi lahan serta nutrisi optimal terbaik bagi budidaya tanaman padi (*rice*). 

Proyek ini disusun untuk memenuhi ketentuan Proyek Akhir Praktikum **Sistem Cerdas Pendukung Keputusan (SCPK) 2025/2026**, Program Studi Informatika, Fakultas Teknik Industri, **UPN "Veteran" Yogyakarta**.

---

## 👥 Anggota Kelompok 10
* **Muhammad Athalla Bagaskara** (NIM: 123240212)
* **Muhammad Ridho Hikmatul Maulana** (NIM: 123240218)

---

## 📊 Ringkasan Proyek
* **Metode SPK:** *Simple Additive Weighting* (SAW)
* **Dataset:** *Crop Recommendation Dataset* (Sumber: Kaggle - `atharvaingle`), yang difokuskan khusus secara eksklusif untuk analisis komprehensif data tanaman padi (*rice*) dengan total sampel acuan yang diuji.
* **Fokus Solusi:** Menghindari bias klasifikasi *Machine Learning* / rekomendasi crop umum, sistem ini murni melakukan evaluasi dan perangkingan multikriteria terhadap kondisi fisik & kimiawi lahan agar sesuai dengan batas pertumbuhan optimal komoditas padi.

### 📐 Kriteria Evaluasi Lahan
Aplikasi ini mengevaluasi alternatif sampel lahan berdasarkan 7 kriteria utama yang krusial bagi produktivitas tanaman padi:
1. **N (Nitrogen):** Kandungan hara Nitrogen dalam tanah (Kriteria *Benefit*).
2. **P (Fosfor):** Kandungan hara Fosfor dalam tanah (Kriteria *Benefit*).
3. **K (Kalium):** Kandungan hara Kalium dalam tanah (Kriteria *Benefit*).
4. **Temperature (Suhu):** Tingkat suhu lingkungan tempat lahan berada dalam °C (Kriteria *Benefit*).
5. **Humidity (Kelembaban):** Tingkat kelembaban udara sekitar lahan dalam % (Kriteria *Benefit*).
6. **pH Tanah:** Tingkat keasaman dan kebasaan media tanam (Kriteria *Benefit*).
7. **Rainfall (Curah Hujan):** Pasokan air hujan tahunan/lokal dalam mm (Kriteria *Benefit*).

---

## 🚀 Fitur Utama Aplikasi
Sesuai dengan **Panduan Teknis Proyek Akhir SCPK**, antarmuka Streamlit ini dilengkapi dengan fungsionalitas tingkat lanjut:

1. **Navigasi Layout Terstruktur:** Menggunakan sistem seleksi menu sidebar modular yang memisahkan halaman Beranda (Informasi Teori), Dataset, Proses Hitung SPK-SAW, Visualisasi Data Interaktif, dan Profil Kelompok.
2. **Input Bobot Dinamis secara Real-Time:** Pengguna atau Asisten Praktikum dapat menggeser *Slider* bobot kriteria di sidebar. Angka bobot akan langsung dinormalisasi ulang (total = 1.00) dan dampaknya dapat dilihat langsung di seluruh halaman.
3. **Tombol Eksekusi Perhitungan (*Trigger Button*):** Proses kalkulasi matriks keputusan, normalisasi $r_{ij}$, dan perhitungan preferensi $V_i$ dijalankan secara efisien hanya ketika tombol `🚀 Hitung SPK-SAW Sekarang` diklik secara eksplisit.
4. **6 Jenis Visualisasi Data Analitik Interaktif:** Menyediakan analisis data yang kaya dan dinamis (berubah *real-time* mengikuti pergerakan slider bobot) menggunakan kombinasi *Matplotlib* dan *Seaborn*:
   * **Grafik 1 (Histogram):** Distribusi nilai preferensi preferensi SAW ($V$).
   * **Grafik 2 (Pie & Bar Chart):** Proporsi input bobot kriteria aktif.
   * **Grafik 3 (Boxplot Multifaktor):** Distribusi sebaran nilai 7 kriteria asli khusus untuk padi.
   * **Grafik 4 (Dual Radar Chart):** Perbandingan karakteristik biologi lahan padi dengan jaring laba-laba preferensi bobot user.
   * **Grafik 5 (Heatmap):** Korelasi matriks antar kriteria lingkungan dengan nilai preferensi akhir SAW.
   * **Grafik 6 (Scatter Plot Adaptif):** Memetakan sebaran koordinat top 10% lahan terbaik berdasarkan 2 kriteria dengan bobot tertinggi saat itu.
5. **Keterangan Interpretasi Teks Dinamis (*Automated Insights*):** Di bawah setiap grafik visualisasi, terdapat teks penjelasan analitis otomatis yang membaca kondisi data terkini berdasarkan posisi slider bobot yang aktif.

---

## 🧮 Alur Perhitungan Metode SAW dalam Kode
Metode *Simple Additive Weighting* (SAW) sering dikenal sebagai metode penjumlahan terbobot. Langkah-langkah matematis yang diimplementasikan di dalam `SAW_Pupuk.py` meliputi:

1. **Pembentukan Matriks Keputusan ($X$):** Mengekstraksi subset data dari `dataset_pupuk.csv` yang memiliki `label == 'rice'`.
2. **Normalisasi Matriks ($R$):**
   Karena seluruh kriteria diarahkan pada batas kecocokan optimum pertumbuhan padi (skema *Benefit*), maka rumusnya adalah:
   $$r_{ij} = \frac{x_{ij}}{\max(x_{ij})}$$
3. **Proses Nilai Preferensi ($V$):** Mengalikan matriks hasil normalisasi dengan vektor bobot relatif ($W$) yang didapatkan dari slider Streamlit:
   $$V_i = \sum_{j=1}^{n} w_j \cdot r_{ij}$$
4. **Evaluasi Akhir:** Mengurutkan alternatif dari nilai $V_i$ terbesar hingga terkecil untuk menyajikan rekomendasi top-N sampel kondisi lahan terbaik bagi tanaman padi.

---

## 📁 Struktur Repositori
```bash
├── README.md               # Dokumentasi proyek/panduan repositori (File ini)
├── SAW_Pupuk.py            # Main script Python untuk aplikasi GUI web Streamlit
├── dataset_pupuk.csv       # Dataset kondisi tanah & lingkungan (format .csv)
└── Laporan_Proyek_Akhir.pdf # Laporan resmi proyek akhir praktikum SCPK
