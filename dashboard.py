import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="E-Commerce Performance Dashboard",
    page_icon="📦",
    layout="wide"
)

sns.set_theme(style="darkgrid")

# ==========================================
# CUSTOM CSS — Perbaikan Tampilan
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* Global font */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background utama */
.main .block-container {
    background-color: #f0f2f6;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1280px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0d1b2a 0%, #1b3a5c 60%, #1e4976 100%);
    border-right: none;
}
[data-testid="stSidebar"] * { color: #dce9f5 !important; }
[data-testid="stSidebar"] .stMarkdown h2 {
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: #ffffff !important;
    text-transform: uppercase;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15) !important;
    margin: 14px 0;
}
[data-testid="stSidebar"] .stText, 
[data-testid="stSidebar"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    color: #b8d4ed !important;
    line-height: 1.8;
}

/* Title */
h1 {
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: #0d1b2a !important;
    letter-spacing: -0.02em;
    margin-bottom: 0 !important;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background: #ffffff;
    border-radius: 14px;
    padding: 18px 22px !important;
    box-shadow: 0 1px 8px rgba(0,0,0,0.08);
    border-top: 4px solid #1b3a5c;
    transition: box-shadow 0.2s;
}
[data-testid="stMetric"]:hover {
    box-shadow: 0 4px 18px rgba(27,58,92,0.15);
}
[data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #6b7c93 !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    color: #0d1b2a !important;
}

/* Divider */
hr {
    border: none !important;
    border-top: 1.5px solid #dde3ec !important;
    margin: 20px 0 !important;
}

/* Subheader */
h2 {
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    color: #0d1b2a !important;
    letter-spacing: -0.01em;
    padding-bottom: 6px;
    border-bottom: 2px solid #1b3a5c;
    display: inline-block;
    margin-bottom: 12px !important;
}

/* Caption / Footer */
.stCaption, [data-testid="stCaptionContainer"] {
    text-alia bernama 'orders_cleaned.csv' di folder yang samagn: center;
    font-size: 0.78rem !important;
    color: #9eafc0 !important;
    padding: 16px 0 4px 0;
    border-top: 1px solid #dde3ec;
    margin-top: 28px;
}

/* Info text below title */
.stMarkdown p {
    color: #4a6075;
    font-size: 0.9rem;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    
    df = pd.read_csv('orders_cleaned.csv')
    
    # Memastikan kolom waktu tetap bertipe datetime
    datetime_cols = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_customer_date']
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col])
    
    # Filter Tahun 2017 (Sesuai Pertanyaan Bisnis)
    df_2017 = df[df['order_purchase_timestamp'].dt.year == 2017].copy()
    
    # Menambahkan kolom untuk pendukung visualisasi
    df_2017['purchase_day'] = df_2017['order_purchase_timestamp'].dt.day_name()
    df_2017['purchase_hour'] = df_2017['order_purchase_timestamp'].dt.hour
    df_2017['delivery_days'] = (df_2017['order_delivered_customer_date'] - df_2017['order_approved_at']).dt.total_seconds() / 86400
    
    return df_2017

df_main = load_data()

# ==========================================
# 3. SIDEBAR (PROFIL)
# ==========================================
with st.sidebar:
    st.image("https://raw.githubusercontent.com/dicodingacademy/assets/main/logo.png", width=150)
    st.markdown("---")
    st.markdown("## 👨‍💻 Profil Analis")
    st.text("Nama: Syadza Oktifani")
    st.text("NIM: 23343019")
    st.text("Prodi: Informatika, UNP")
    st.text("Cohort ID: CDCC282D6X1136")
    st.markdown("---")

# ==========================================
# 4. KONTEN UTAMA & KPI
# ==========================================
st.title("📦 E-Commerce Performance Dashboard (2017)")
st.markdown("Dashboard ini menggunakan data yang telah dibersihkan untuk menganalisis perilaku pelanggan dan efisiensi pengiriman guna merumuskan rekomendasi strategi bisnis.")

# Spacer kecil sebelum metrics
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Pesanan", value=f"{df_main.shape[0]:,}")

with col2:
    avg_delivery = df_main['delivery_days'].mean()
    st.metric("Rata-rata Pengiriman", value=f"{avg_delivery:.2f} Hari")

with col3:
    peak_day = df_main['purchase_day'].mode()[0]
    st.metric("Hari Puncak (Total)", value=peak_day)

with col4:
    peak_hour = df_main['purchase_hour'].mode()[0]
    st.metric("Jam Puncak", value=f"{peak_hour}:00")

st.markdown("---")

# ==========================================
# 5. VISUALISASI 1: WAKTU PROMOSI (HEATMAP)
# ==========================================
st.subheader("Analisis Waktu Optimal Promosi")

# Persiapan data heatmap
heatmap_data = df_main.groupby(['purchase_day', 'purchase_hour']).size().reset_index(name='count')
pivot_data = heatmap_data.pivot(index='purchase_day', columns='purchase_hour', values='count')
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
pivot_data = pivot_data.reindex(days_order)

# Chart styling yang lebih rapi
fig1, ax1 = plt.subplots(figsize=(12, 5))
fig1.patch.set_facecolor('#ffffff')
ax1.set_facecolor('#f8fafc')

sns.heatmap(
    pivot_data, cmap="YlGnBu", ax=ax1,
    linewidths=0.3, linecolor='#e2e8f0',
    cbar_kws={'label': 'Jumlah Order', 'shrink': 0.8}
)
ax1.set_title("Intensitas Checkout Pelanggan Berdasarkan Hari & Jam",
              fontsize=13, fontweight='bold', pad=14, color='#0d1b2a')
ax1.set_xlabel("Jam Pembelian (0-23)", fontsize=10, color='#4a6075', labelpad=8)
ax1.set_ylabel("Hari", fontsize=10, color='#4a6075', labelpad=8)
ax1.tick_params(colors='#4a6075', labelsize=9)
plt.tight_layout()

st.pyplot(fig1)

# Tambahan: Expander Insight untuk Reviewer Dicoding
with st.expander("💡 Lihat Insight & Rekomendasi Bisnis"):
    st.write("""
    **Insight:** Terdapat konsentrasi transaksi yang sangat tinggi (warna gelap) pada hari **Senin pukul 13:00 siang dan 21:00 malam**. Transaksi di akhir pekan (Sabtu-Minggu) cenderung sepi.
    
    **Rekomendasi Action Item:** Tim Marketing harus memfokuskan anggaran iklan dan peluncuran kampanye promosi besar (*Flash Sale*) pada awal pekan, tepatnya beberapa jam sebelum waktu puncak (misal: Senin pukul 12:00 dan 20:00) untuk menangkap momentum kesiapan pelanggan melakukan *checkout*.
    """)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 6. VISUALISASI 2: LOGISTIK (HISTOGRAM)
# ==========================================
st.subheader("Distribusi Waktu Pengiriman Logistik")

fig2, ax2 = plt.subplots(figsize=(10, 4))
fig2.patch.set_facecolor('#ffffff')
ax2.set_facecolor('#f8fafc')

sns.histplot(df_main['delivery_days'], bins=50, kde=True, color='teal', ax=ax2,
             edgecolor='#005f5f', linewidth=0.3)

# Garis rata-rata
ax2.axvline(avg_delivery, color='#e8932e', linewidth=2, linestyle='--',
            label=f'Rata-rata: {avg_delivery:.1f} hari')
ax2.legend(fontsize=9.5, framealpha=0.85)

ax2.set_xlim(0, 60)
ax2.set_title("Distribusi Durasi Penyelesaian Pesanan",
              fontsize=13, fontweight='bold', pad=14, color='#0d1b2a')
ax2.set_xlabel("Durasi Pengiriman (Hari)", fontsize=10, color='#4a6075', labelpad=8)
ax2.set_ylabel("Jumlah Pesanan", fontsize=10, color='#4a6075', labelpad=8)
ax2.tick_params(colors='#4a6075', labelsize=9)
plt.tight_layout()

st.pyplot(fig2)

# Tambahan: Expander Insight untuk Reviewer Dicoding
with st.expander("💡 Lihat Insight & Rekomendasi Bisnis"):
    st.write("""
    **Insight:** Rata-rata pengiriman memakan waktu **12,6 hari**, dengan grafik yang memanjang jauh ke kanan (*right-skewed*), menandakan banyaknya anomali keterlambatan pengiriman yang memakan waktu berminggu-minggu.
    
    **Rekomendasi Action Item:** Waktu tunggu hampir 2 minggu sangat lambat. Perusahaan harus memberlakukan denda/insentif batas waktu pengemasan (*packing time*) maksimal 24 jam bagi para penjual (*seller*), serta mengevaluasi rute dan *Service Level Agreement* (SLA) dengan mitra ekspedisi.
    """)

st.caption("Copyright (c) Syadza Oktifani 2026")