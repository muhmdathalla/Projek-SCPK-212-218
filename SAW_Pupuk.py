import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

st.set_page_config(
    page_title="SPK Kondisi Lahan Padi – SAW",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght=400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    .main { background-color: #f0f7ee; }
    
    /* Memastikan teks dalam card terbaca */
    .card {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 16px;
        color: #333333 !important; /* Warna teks gelap */
    }
    
    .card p, .card h2, .card h3, .card td, .card div {
        color: #333333 !important;
    }

    .metric-card {
        background: linear-gradient(135deg, #2d6a4f, #52b788);
        border-radius: 12px;
        padding: 18px 22px;
        color: white !important;
        text-align: center;
        box-shadow: 0 4px 12px rgba(45,106,79,0.3);
    }
    .metric-card h2, .metric-card p { color: white !important; }
    
    .title-header {
        background: linear-gradient(135deg, #1b4332, #2d6a4f);
        padding: 28px 32px;
        border-radius: 14px;
        color: white !important;
        margin-bottom: 24px;
    }
    .title-header h1, .title-header p { color: white !important; }
    
    .formula-box {
        background: #e8f5e9;
        border-left: 4px solid #2d6a4f;
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        font-family: monospace;
        font-size: 0.95rem;
        color: #1b4332 !important;
        margin: 10px 0;
    }
    
    /* Sidebar */
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1b4332 0%, #2d6a4f 100%);
    }
    div[data-testid="stSidebar"] * { color: white !important; }
    
    .stButton > button {
        background: linear-gradient(135deg, #2d6a4f, #40916c);
        color: white !important;
    }
    
    .info-box {
        background: #e8f5e9;
        border: 1px solid #52b788;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 12px;
        font-size: 0.9rem;
        color: #1b4332 !important;
    }
</style>
""", unsafe_allow_html=True)

# LOAD DATASET
@st.cache_data
def load_data():
    df = pd.read_csv("dataset_pupuk.csv")
    df.columns = [c.strip() for c in df.columns]
    return df

df_all = load_data()


# SIDEBAR – NAVIGASI & BOBOT
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌾 SPK Evaluasi Lahan Padi")
    st.markdown("---")
    halaman = st.selectbox(
        "📌 Pilih Halaman",
        ["🏠 Beranda", "📊 Dataset", "⚙️ Hitung SPK-SAW", "📈 Visualisasi Data", "👥 Profil Kelompok"]
    )
    st.markdown("---")
    st.markdown("### ⚖️ Bobot Kriteria")
    st.markdown("*Atur bobot tiap kriteria — berlaku di semua halaman*")

    w_N    = st.slider("🌿 Nitrogen (N)",           0, 100, 20, key="wN")
    w_P    = st.slider("🟡 Fosfor (P)",              0, 100, 15, key="wP")
    w_K    = st.slider("🔵 Kalium (K)",              0, 100, 15, key="wK")
    w_temp = st.slider("🌡️ Suhu (Temperature)",      0, 100, 15, key="wT")
    w_hum  = st.slider("💧 Kelembaban (Humidity)",   0, 100, 15, key="wH")
    w_ph   = st.slider("🧪 pH Tanah",                0, 100, 10, key="wPH")
    w_rain = st.slider("🌧️ Curah Hujan (Rainfall)",  0, 100, 10, key="wR")

    st.markdown("---")
    st.markdown("### 🌾 Fokus Analisis")
    st.success("Analisis difokuskan pada Tanaman Padi (Rice)")
    crop_filter = "rice"
    st.markdown("---")
    st.markdown("### 📏 Jumlah Hasil Ranking")
    top_n = st.number_input("Tampilkan Top-N:", min_value=5, max_value=200, value=20, step=5)

# HELPER FUNGSI SAW
# ─────────────────────────────────────────────
KRITERIA = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
TIPE     = ['benefit','benefit','benefit','benefit','benefit','benefit','benefit']

LABEL_MAP = {
    'N': 'Nitrogen (N)',
    'P': 'Fosfor (P)',
    'K': 'Kalium (K)',
    'temperature': 'Suhu',
    'humidity': 'Kelembaban',
    'ph': 'pH Tanah',
    'rainfall': 'Curah Hujan'
}

WARNA_HIJAU = ['#1b4332','#2d6a4f','#40916c','#52b788','#74c69d','#95d5b2','#b7e4c7']

def get_bobot(w_N, w_P, w_K, w_temp, w_hum, w_ph, w_rain):
    raw = np.array([w_N, w_P, w_K, w_temp, w_hum, w_ph, w_rain], dtype=float)
    total = raw.sum()
    if total == 0:
        return raw
    return raw / total

def normalisasi_saw(df_input):
    df_norm = pd.DataFrame(index=df_input.index)
    for i, col in enumerate(KRITERIA):
        if TIPE[i] == 'benefit':
            max_val = df_input[col].max()
            df_norm[col] = df_input[col] / max_val if max_val != 0 else 0
        else:
            min_val = df_input[col].min()
            df_norm[col] = min_val / df_input[col].replace(0, np.nan)
    return df_norm

def hitung_saw(df_input, bobot):
    df_norm = normalisasi_saw(df_input)
    nilai   = (df_norm[KRITERIA] * bobot).sum(axis=1)
    return df_norm, nilai

def get_filtered_df():
    """Kembalikan dataframe yang khusus difokuskan untuk tanaman padi (rice)."""
    return df_all[df_all['label'] == 'rice'].copy()

def get_saw_result(df_input):
    """Hitung SAW dengan bobot aktif dari sidebar."""
    bobot = get_bobot(w_N, w_P, w_K, w_temp, w_hum, w_ph, w_rain)
    df_w  = df_input.reset_index(drop=True)
    df_norm, nilai = hitung_saw(df_w[KRITERIA], bobot)
    df_hasil = df_w.copy()
    df_hasil['Nilai V'] = nilai.values
    df_hasil = df_hasil.sort_values('Nilai V', ascending=False).reset_index(drop=True)
    df_hasil.insert(0, 'Peringkat', range(1, len(df_hasil)+1))
    return df_hasil, bobot

# HALAMAN 1 – BERANDA
# ─────────────────────────────────────────────
if halaman == "🏠 Beranda":
    st.markdown("""
    <div class='title-header'>
        <h1>🌾 Sistem Pendukung Keputusan Penentuan Kondisi Lahan dan Nutrisi Optimal untuk Tanaman Padi</h1>
        <p>Metode SAW (Simple Additive Weighting) — Praktikum SCPK 2025/2026</p>
    </div>
    """, unsafe_allow_html=True)

    rice_count = len(df_all[df_all['label']=='rice'])
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><h2>{rice_count}</h2><p>Total Sampel Lahan Padi</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'><h2>7</h2><p>Kriteria Evaluasi</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'><h2>Padi (Rice)</h2><p>Fokus Tanaman</p></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='metric-card'><h2>SAW</h2><p>Metode SPK</p></div>", unsafe_allow_html=True)

    st.markdown("---")
    col_a, col_b = st.columns([1.2, 1])
    with col_a:
        st.subheader("📋 Tentang Sistem")
        st.markdown("""
        Sistem ini merupakan **Sistem Pendukung Keputusan (SPK)** berbasis metode 
        **SAW (Simple Additive Weighting)** untuk mengevaluasi dan meranking kondisi lahan terbaik 
        bagi budidaya tanaman padi 🌾.

        Analisis dilakukan menggunakan parameter:
        - Nitrogen (N)
        - Fosfor (P)
        - Kalium (K)
        - Suhu
        - Kelembaban
        - pH tanah
        - Curah hujan

        Dataset berasal dari:
        - 📦 Kaggle — Crop Recommendation Dataset
        - 👤 Author: atharvaingle
        - 📊 2.200 data penelitian pertanian

        Pada penelitian ini, dataset difokuskan khusus untuk analisis kondisi optimal tanaman padi (rice).
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.subheader("🧮 Rumus Metode SAW")
        st.markdown("**Langkah 1 — Normalisasi Matriks:**")
        st.markdown("""
        <div class='formula-box'>
        Benefit : r_ij = x_ij / max(x_j)<br>
        Cost    : r_ij = min(x_j) / x_ij
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**Langkah 2 — Nilai Preferensi:**")
        st.markdown("""
        <div class='formula-box'>
        V_i = Σ ( w_j × r_ij )
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **Keterangan:**
        - `r_ij` = nilai normalisasi kriteria j pada alternatif i
        - `w_j`  = bobot kriteria j (Σwj = 1)
        - `V_i`  = nilai preferensi akhir alternatif i
        - Alternatif dengan **V_i terbesar = Urutan Kondisi Lahan Terbaik**
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# HALAMAN 2 – DATASET
# ─────────────────────────────────────────────
elif halaman == "📊 Dataset":

    st.markdown("""
    <div class='title-header'>
        <h1>📊 Dataset Analisis Tanaman Padi</h1>
        <p>
            Dataset difokuskan khusus untuk analisis kondisi optimal tanaman padi (rice)
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "🔗 Buka Dataset Asli di Kaggle",
        "https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset",
        use_container_width=True
    )

    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown("#### 🔍 Info Dataset")
        rice_count = len(df_all[df_all['label']=='rice'])
        st.markdown(f"- **Total data padi:** {rice_count} baris")
        st.markdown("- **Fokus analisis:** Tanaman Padi (Rice)")
        st.markdown("- **Jenis metode:** Sistem Pendukung Keputusan (SAW)")
        st.markdown(f"- **Missing values:** {df_all[df_all['label']=='rice'].isnull().sum().sum()}")
        st.markdown(f"- **Duplikat:** {df_all[df_all['label']=='rice'].duplicated().sum()}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("#### 📌 Filter Tampilan Dataset")
        df_show = df_all[df_all['label'] == 'rice']
        st.markdown(f"Menampilkan **{len(df_show):,}** baris data padi (rice)")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### 📋 Tabel Lahan Padi")
    st.dataframe(df_show.reset_index(drop=True), use_container_width=True, height=400)
    st.markdown("---")
    st.markdown("#### 📈 Statistik Deskriptif Lahan Padi")
    st.dataframe(df_show.describe().round(3), use_container_width=True)

# HALAMAN 3 – HITUNG SPK SAW
# ─────────────────────────────────────────────
elif halaman == "⚙️ Hitung SPK-SAW":
    st.markdown("<div class='title-header'><h1>⚙️ Evaluasi Kondisi Lahan dan Nutrisi Padi – Metode SAW</h1><p>Simple Additive Weighting — Atur bobot di sidebar kiri</p></div>", unsafe_allow_html=True)

    df_hitung = get_filtered_df()
    df_hitung = df_hitung.reset_index(drop=True)
    df_hitung.index = df_hitung.index + 1
    df_hitung.index.name = "No"

    bobot = get_bobot(w_N, w_P, w_K, w_temp, w_hum, w_ph, w_rain)

    st.markdown("---")
    st.markdown("### ⚖️ Bobot Kriteria yang Digunakan")
    df_bobot = pd.DataFrame({
        "Kriteria": [LABEL_MAP[k] for k in KRITERIA],
        "Bobot (Input)": [w_N, w_P, w_K, w_temp, w_hum, w_ph, w_rain],
        "Bobot (Ternormalisasi)": [round(b, 4) for b in bobot],
        "Tipe": TIPE
    })
    st.dataframe(df_bobot, use_container_width=True, hide_index=True)
    st.markdown("---")

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        hitung = st.button("🚀 Hitung SPK-SAW Sekarang", use_container_width=True)

    if hitung:
        with st.spinner("Menghitung kondisi lahan... 🌾"):
            df_norm, nilai_preferensi = hitung_saw(df_hitung[KRITERIA], bobot)
            df_hasil = df_hitung.copy()
            df_hasil['Nilai Preferensi (V)'] = nilai_preferensi.values
            df_hasil = df_hasil.sort_values('Nilai Preferensi (V)', ascending=False)
            df_hasil.insert(0, 'Peringkat', range(1, len(df_hasil)+1))

            st.markdown("---")
            st.markdown("### 📌 Langkah 1 — Matriks Keputusan (Data Asli)")
            st.markdown(f"*Menampilkan {min(10, len(df_hitung))} baris pertama data alternatif lahan padi*")
            st.dataframe(df_hitung[KRITERIA].head(10).round(4), use_container_width=True)

            st.markdown("---")
            st.markdown("### 📌 Langkah 2 — Matriks Normalisasi (r_ij)")
            st.markdown("""<div class='formula-box'>Benefit: r_ij = x_ij / max(x_j)</div>""", unsafe_allow_html=True)
            df_norm_show = df_norm.copy()
            df_norm_show.columns = [LABEL_MAP[c] for c in KRITERIA]
            st.dataframe(df_norm_show.head(10).round(4), use_container_width=True)

            st.markdown("---")
            st.markdown("### 📌 Langkah 3 — Nilai Preferensi (V_i = Σ w_j × r_ij)")
            st.markdown("""<div class='formula-box'>V_i = w_N×r_N + w_P×r_P + w_K×r_K + w_T×r_T + w_H×r_H + w_pH×r_pH + w_R×r_R</div>""", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown(f"### 🏆 Hasil Evaluasi Kondisi Lahan & Nutrisi Padi (Top {top_n})")
            df_top = df_hasil.head(int(top_n)).copy()
            df_top_show = df_top[['Peringkat','label','N','P','K','temperature','humidity','ph','rainfall','Nilai Preferensi (V)']].copy()
            df_top_show.columns = ['Peringkat','Kategori','N','P','K','Suhu','Kelembaban','pH','Curah Hujan','Nilai V']
            df_top_show['Nilai V'] = df_top_show['Nilai V'].round(4)

            def warna_peringkat(row):
                if row['Peringkat'] == 1:
                    return ['background-color: #000000; font-weight:bold']*len(row)
                elif row['Peringkat'] == 2:
                    return ['background-color: #000000; font-weight:bold']*len(row)
                elif row['Peringkat'] == 3:
                    return ['background-color: #000000; font-weight:bold']*len(row)
                return ['']*len(row)

            st.dataframe(
                df_top_show.style.apply(warna_peringkat, axis=1),
                use_container_width=True, height=450, hide_index=True
            )

            st.markdown("---")
            st.markdown("### 🥇 3 Kondisi Lahan Padi Terbaik")
            medals = ["🥇", "🥈", "🥉"]
            col3 = st.columns(3)
            for idx in range(min(3, len(df_hasil))):
                row = df_hasil.iloc[idx]
                with col3[idx]:
                    st.markdown(f"""
                    <div class='card'>
                        <h2 style='margin:0;font-size:2rem'>{medals[idx]}</h2>
                        <h3 style='color:#2d6a4f;margin:4px 0'>KONDISI LAHAN #{idx+1}</h3>
                        <p style='margin:0;font-size:0.9rem'>N={row['N']} | P={row['P']} | K={row['K']}</p>
                        <p style='margin:4px 0;font-size:0.9rem'>Suhu={row['temperature']:.1f}°C | pH={row['ph']:.2f}</p>
                        <p style='font-weight:700;color:#1b4332;font-size:1.1rem'>V = {row['Nilai Preferensi (V)']:.4f}</p>
                    </div>
                    """, unsafe_allow_html=True)

            st.success("kondisi lahan berhasil dievaluasi menggunakan metode SAW")

# HALAMAN 4 – VISUALISASI (DINAMIS)
# ─────────────────────────────────────────────
elif halaman == "📈 Visualisasi Data":
    st.markdown(
        "<div class='title-header'>"
        "<h1>📈 Visualisasi Analisis Kondisi Padi</h1>"
        "<p>Visualisasi otomatis berubah sesuai bobot kriteria SAW</p>"
        "</div>",
        unsafe_allow_html=True
    )

    # Ambil data filter padi
    df_vis = get_filtered_df().reset_index(drop=True)
    bobot  = get_bobot(w_N, w_P, w_K, w_temp, w_hum, w_ph, w_rain)

    # Hitung nilai SAW untuk data padi
    df_norm_vis, nilai_vis = hitung_saw(df_vis[KRITERIA], bobot)
    df_vis['Nilai V'] = nilai_vis.values

    # Deteksi info konteks dinamis untuk interpretasi teks
    jumlah_data = len(df_vis)
    bobot_pct   = [round(b*100, 1) for b in bobot]
    idx_max     = int(np.argmax(bobot)) if bobot.sum() > 0 else 0
    bobot_dominan = LABEL_MAP[KRITERIA[idx_max]]
    nilai_v_max   = df_vis['Nilai V'].max()
    nilai_v_min   = df_vis['Nilai V'].min()
    nilai_v_mean  = df_vis['Nilai V'].mean()

    st.markdown(f"""
    <div class='info-box'>
        📌 <b>Fokus Analisis:</b> Tanaman Padi (Rice) &nbsp;|&nbsp;
        📦 <b>Data Evaluasi:</b> {jumlah_data:,} baris &nbsp;|&nbsp;
        🏆 <b>Bobot Terbesar:</b> {bobot_dominan} ({max(bobot_pct):.1f}%) &nbsp;|&nbsp;
        ⚖️ <b>Bobot (%):</b> N={bobot_pct[0]} P={bobot_pct[1]} K={bobot_pct[2]}
        Suhu={bobot_pct[3]} Lembab={bobot_pct[4]} pH={bobot_pct[5]} Hujan={bobot_pct[6]}
    </div>
    """, unsafe_allow_html=True)

    # GRAFIK 1 — DISTRIBUSI NILAI SAW Preferensi Padi
    # ══════════════════════════════════════════
    st.markdown("### 📊 Grafik 1 — Distribusi Nilai Preferensi SAW")
    
    fig1, ax1 = plt.subplots(figsize=(10,4))
    ax1.hist(df_vis['Nilai V'], bins=20, color='#52b788', edgecolor='white')
    ax1.set_title("Distribusi Nilai Preferensi Kondisi Lahan Padi", fontweight='bold')
    ax1.set_xlabel("Nilai Preferensi (V)")
    ax1.set_ylabel("Frekuensi")
    ax1.set_facecolor('#f8fffe')
    ax1.grid(axis='y', linestyle='--', alpha=0.4)
    st.pyplot(fig1)
    plt.close()

    # KETERANGAN TEKS DINAMIS GRAFIK 1
    st.markdown(f"""
    <div style='background-color: #ffffff; padding: 15px; border-radius: 8px; border-left: 5px solid #52b788; margin-bottom: 25px;'>
        <b>💡 Interpretasi Analitis Distribusi Preferensi (Dinamis):</b><br>
        Berdasarkan pembobotan kriteria saat ini, sebaran nilai preferensi ($V$) untuk {jumlah_data} sampel lahan padi berkisar antara 
        <b>{nilai_v_min:.4f}</b> hingga <b>{nilai_v_max:.4f}</b> dengan nilai rata-rata akurasi evaluasi sebesar <b>{nilai_v_mean:.4f}</b>. 
        Makin tinggi konsentrasi grafik ke arah kanan (mendekati {nilai_v_max:.2f}), menunjukkan bahwa dataset memiliki banyak sampel kondisi lahan yang sangat ideal dan siap mendukung produktivitas tanaman padi sesuai preferensi bobot yang Anda tentukan.
    </div>
    """, unsafe_allow_html=True)


    # GRAFIK 2 — KONTRIBUSI BOBOT KRITERIA
    # ══════════════════════════════════════════
    st.markdown("### 📊 Grafik 2 — Kontribusi Bobot Kriteria (Aktif)")
    fig2, axes2 = plt.subplots(1, 2, figsize=(14, 4.5))

    label_kriteria = [LABEL_MAP[k] for k in KRITERIA]
    raw_bobot = [w_N, w_P, w_K, w_temp, w_hum, w_ph, w_rain]

    if sum(raw_bobot) > 0:
        axes2[0].pie(raw_bobot, labels=label_kriteria, autopct=lambda p: f'{p:.1f}%' if p > 3 else '',
                     colors=WARNA_HIJAU, startangle=140, pctdistance=0.75,
                     wedgeprops=dict(edgecolor='white', linewidth=1.5))
    else:
        axes2[0].text(0.5, 0.5, 'Semua bobot = 0', ha='center', va='center', fontsize=13)
    axes2[0].set_title("Proporsi Bobot Kriteria", fontweight='bold')

    x_pos = range(len(KRITERIA))
    bar2  = axes2[1].bar(x_pos, bobot, color=WARNA_HIJAU, edgecolor='white', linewidth=0.8)
    axes2[1].set_xticks(list(x_pos))
    axes2[1].set_xticklabels(label_kriteria, rotation=30, ha='right', fontsize=9)
    axes2[1].set_ylabel("Bobot Ternormalisasi")
    axes2[1].set_title("Bobot Kriteria Ternormalisasi (Σ = 1.00)", fontweight='bold')
    axes2[1].set_facecolor('#f8fffe')
    axes2[1].grid(axis='y', linestyle='--', alpha=0.4)
    for bar, val in zip(bar2, bobot):
        axes2[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003, f"{val:.3f}", ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

    # KETERANGAN TEKS DINAMIS GRAFIK 2
    st.markdown(f"""
    <div style='background-color: #ffffff; padding: 15px; border-radius: 8px; border-left: 5px solid #2d6a4f; margin-bottom: 25px;'>
        <b>💡 Interpretasi Analitis Komposisi Bobot (Dinamis):</b><br>
        Sistem mendeteksi bahwa kriteria <b>{bobot_dominan} ({max(bobot_pct):.1f}%)</b> dikonfigurasi sebagai prioritas utama (kriteria paling krusial). 
        Hal ini secara langsung memaksa rumus SAW untuk memberikan penalti atau nilai preferensi rendah pada lahan padi yang memiliki nilai <i>{bobot_dominan}</i> kurang optimal, meskipun kriteria penunjang lainnya terpenuhi dengan baik.
    </div>
    """, unsafe_allow_html=True)


    # GRAFIK 4 — RADAR CHART TUNGGAL KONDISI IDEAL PADI
    # ══════════════════════════════════════════
    st.markdown("### 📊 Grafik 4 — Radar Chart Profil Kriteria")
    all_max = df_all[KRITERIA].max()
    rice_mean = df_vis[KRITERIA].mean()
    rice_norm = (rice_mean / all_max).values.tolist()
    bobot_norm_radar = (bobot / bobot.max()).tolist() if bobot.max() > 0 else bobot.tolist()

    labels_r = [LABEL_MAP[k] for k in KRITERIA]
    N_axis   = len(labels_r)
    angles   = [n / float(N_axis) * 2 * np.pi for n in range(N_axis)]
    angles  += angles[:1]

    fig4, axes4 = plt.subplots(1, 2, figsize=(14, 5.5), subplot_kw=dict(polar=True))

    ax_r1 = axes4[0]
    r_rice  = rice_norm + rice_norm[:1]
    ax_r1.plot(angles, r_rice, 'o-',  lw=2,   color='#2d6a4f', label='Kondisi Lahan Padi')
    ax_r1.fill(angles, r_rice, alpha=0.25, color='#52b788')
    ax_r1.set_xticks(angles[:-1])
    ax_r1.set_xticklabels(labels_r, fontsize=9)
    ax_r1.set_title("Karakteristik & Profil Ideal Lahan Padi", fontweight='bold', pad=20)
    ax_r1.set_facecolor('#f0f7ee')
    ax_r1.grid(color='#c7e9c0', linewidth=0.8)

    ax_r2 = axes4[1]
    r_bobot = bobot_norm_radar + bobot_norm_radar[:1]
    ax_r2.plot(angles, r_bobot, 'o-', lw=2.5, color='#f4a261', label='Bobot Aktif')
    ax_r2.fill(angles, r_bobot, alpha=0.30, color='#f4a261')
    ax_r2.set_xticks(angles[:-1])
    ax_r2.set_xticklabels([f"{labels_r[i]}\n({bobot_pct[i]}%)" for i in range(N_axis)], fontsize=8)
    ax_r2.set_title("Visualisasi Bobot Kriteria Aktif", fontweight='bold', pad=20)
    ax_r2.set_facecolor('#fff8f0')
    ax_r2.grid(color='#ffe0b2', linewidth=0.8)

    plt.tight_layout()
    st.pyplot(fig4)
    plt.close()

    # KETERANGAN TEKS DINAMIS GRAFIK 4
    st.markdown(f"""
    <div style='background-color: #ffffff; padding: 15px; border-radius: 8px; border-left: 5px solid #f4a261; margin-bottom: 25px;'>
        <b>💡 Interpretasi Analitis Radar Chart (Dinamis):</b><br>
        Grafik sebelah kiri menunjukkan karakteristik biologis data padi (tetap), sedangkan grafik sebelah kanan mencerminkan <b>fokus cara pandang SPK Anda</b> (berubah sesuai slider). 
        Saat ini, bentuk jaring laba-laba pembobotan Anda cenderung tajam/menonjol ke arah kriteria <b>{bobot_dominan}</b>. SPK akan mencari alternatif lahan yang bentuk profil fisiknya paling mendekati atau mampu mengimbangi tuntutan luasan area dari grafik bobot aktif tersebut.
    </div>
    """, unsafe_allow_html=True)


    # GRAFIK 6 — SCATTER TOP-N SAW 
    # ══════════════════════════════════════════
    st.markdown("### 📊 Grafik 6 — Scatter Plot Top Data Berdasarkan Nilai SAW")
    fig6, ax6 = plt.subplots(figsize=(11, 5))

    threshold_top = df_vis['Nilai V'].quantile(0.90)
    df_top_scatter = df_vis[df_vis['Nilai V'] >= threshold_top]
    df_bot_scatter = df_vis[df_vis['Nilai V'] < threshold_top]

    sorted_idx = np.argsort(bobot)[::-1]
    x_col = KRITERIA[sorted_idx[0]]
    y_col = KRITERIA[sorted_idx[1]] if bobot.sum() > 0 else KRITERIA[1]

    ax6.scatter(df_bot_scatter[x_col], df_bot_scatter[y_col], alpha=0.25, color='#b7e4c7', s=20, label='Kondisi Lahan Lainnya')
    scatter_top = ax6.scatter(df_top_scatter[x_col], df_top_scatter[y_col], alpha=0.85, c=df_top_scatter['Nilai V'],
                               cmap='YlGn', s=60, label='Top 10% Kondisi Lahan Terbaik', zorder=5, edgecolors='#1b4332', linewidths=0.5)
    plt.colorbar(scatter_top, ax=ax6, label='Nilai V (SAW)')
    ax6.set_xlabel(f"{LABEL_MAP[x_col]} (bobot terbesar: {bobot_pct[sorted_idx[0]]}%)")
    ax6.set_ylabel(f"{LABEL_MAP[y_col]} (bobot terbesar ke-2: {bobot_pct[sorted_idx[1]]}%)")
    ax6.set_title(f"Sebaran Parameter Lahan Padi: {LABEL_MAP[x_col]} vs {LABEL_MAP[y_col]}", fontsize=12, fontweight='bold')
    ax6.legend()
    ax6.set_facecolor('#f8fffe')
    ax6.grid(linestyle='--', alpha=0.4)
    plt.tight_layout()
    st.pyplot(fig6)
    plt.close()

    # KETERANGAN TEKS DINAMIS GRAFIK 6
    st.markdown(f"""
    <div style='background-color: #ffffff; padding: 15px; border-radius: 8px; border-left: 5px solid #1b4332; margin-bottom: 25px;'>
        <b>💡 Interpretasi Analitis Sebaran Titik Lahan Terbaik (Dinamis):</b><br>
        Karena Anda mengubah nilai slider, sumbu X otomatis mendeteksi kriteria ke-1 tertinggi yaitu <b>{LABEL_MAP[x_col]}</b> dan sumbu Y mendeteksi kriteria ke-2 tertinggi yaitu <b>{LABEL_MAP[y_col]}</b>. 
        Perhatikan titik-titik gelap (Top 10% Lahan Terbaik hasil SAW). Mereka mengelompok pada area tertentu. Ini membuktikan secara matematis bahwa metode SAW berhasil menyaring lahan yang tidak sekadar memiliki nutrisi tinggi acak, melainkan yang secara presisi mengoptimalkan kombinasi antara kriteria <i>{LABEL_MAP[x_col]}</i> dan <i>{LABEL_MAP[y_col]}</i>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("💡 **Tips Pengujian:** Coba geser salah satu slider di sidebar kiri sekarang! Seluruh teks penjelasan di atas beserta angka statistikonya akan langsung menyesuaikan logika matematika SAW yang baru.")

# HALAMAN 5 – PROFIL KELOMPOK
# ─────────────────────────────────────────────
elif halaman == "👥 Profil Kelompok":
    st.markdown("<div class='title-header'><h1>👥 Profil Kelompok</h1><p>Praktikum SCPK 2025/2026</p></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='card' style='text-align:center'>
            <div style='font-size:4rem'>👨‍💻</div>
            <h2 style='color:#2d6a4f'>Muhammad Athalla Bagaskara</h2>
            <p style='font-size:1rem; color:#555'>NIM: 123240212</p>
            <hr>
            <p>Anggota Kelompok</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='card' style='text-align:center'>
            <div style='font-size:4rem'>👨‍💻</div>
            <h2 style='color:#2d6a4f'>Muhammad Ridho Hikmatul Maulana</h2>
            <p style='font-size:1rem; color:#555'>NIM: 123240218</p>
            <hr>
            <p>Anggota Kelompok</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class='card'>
        <h3 style='color:#000000'>📋 Detail Proyek Akhir</h3>
        <table style='width:100%; font-size:0.95rem'>
            <tr>
                <td style='padding:6px;font-weight:600;width:200px'>Judul Proyek</td>
                <td>Sistem Pendukung Keputusan Penentuan Kondisi Lahan dan Nutrisi Optimal untuk Budidaya Tanaman Padi Menggunakan Metode SAW</td>
            </tr>
            <tr><td style='padding:6px;font-weight:600'>Metode SPK</td><td>SAW (Simple Additive Weighting)</td></tr>
            <tr><td style='padding:6px;font-weight:600'>Dataset</td><td>Crop Recommendation Dataset — Kaggle (Fokus data: rice)</td></tr>
            <tr><td style='padding:6px;font-weight:600'>Kriteria Evaluasi</td><td>N, P, K, Temperature, Humidity, pH, Rainfall (7 kriteria)</td></tr>
            <tr><td style='padding:6px;font-weight:600'>Teknologi</td><td>Python, Streamlit, Pandas, NumPy, Matplotlib, Seaborn</td></tr>
            <tr><td style='padding:6px;font-weight:600'>Mata Kuliah</td><td>Praktikum SCPK (Sistem Cerdas Pendukung Keputusan) 2025/2026</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
