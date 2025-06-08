import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Sayfa yapılandırması
st.set_page_config(page_title="Karbon Emisyonu Dashboard", layout="wide")
st.title("📊 Karbon Emisyonu Dashboard & Analizler")

# Özel stil (şehir seçimi dahil)
st.markdown("""
<style>
.st-ah.st-cs.st-ct.st-cu.st-cv {
    color: red !important;
    font-size: 15px !important; /* yazı boyutu */
    font-weight: bold; 
}
</style>
""", unsafe_allow_html=True)


# Veri yükleme
df = pd.read_csv("results/usage_log.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df = df.dropna(subset=['timestamp'])

# Eksik sütunları tamamla
for col in ['kuzu', 'balik', 'ucus_emisyonu']:
    if col not in df.columns:
        df[col] = 0

# Sütun isimlerini Türkçeleştir (orijinal sütun varsa)
df.rename(columns={
    'beef': 'dana',
    'chicken': 'tavuk',
    'lamb': 'kuzu',
    'fish': 'balik',
    'car': 'araba',
    'flight_emission': 'ucus_emisyonu',
    'electricity': 'elektrik'
}, inplace=True)

# Hesaplamalar
df['et_emisyonu'] = df[['dana', 'tavuk', 'kuzu', 'balik']].sum(axis=1)
df['ulasim_emisyonu'] = df['araba'] + df['ucus_emisyonu']
df['elektrik_emisyonu'] = df['elektrik']
df['toplam_emisyon'] = df['et_emisyonu'] + df['ulasim_emisyonu'] + df['elektrik_emisyonu']

# Sidebar filtreleri
st.sidebar.markdown("## 🔍 Filtreler")

min_date, max_date = df['timestamp'].min().date(), df['timestamp'].max().date()
tarih_araligi = st.sidebar.date_input("📅 Tarih Aralığı", [min_date, max_date], min_value=min_date, max_value=max_date)

sehirler = df['city'].unique()
secili_sehirler = st.sidebar.multiselect("🏙️ Şehir Seçimi", sehirler, default=sehirler)

et_turleri = ['dana', 'tavuk']
secili_etler = st.sidebar.multiselect("🥩 Et Türleri", et_turleri, default=et_turleri)

ulasim_turleri = ['araba']
secili_ulasim = st.sidebar.multiselect("🚗 Ulaşım Türleri", ulasim_turleri, default=['araba'])

# 🔄 Filtreyi Uygula
df_filtreli = df[
    (df['timestamp'].dt.date >= tarih_araligi[0]) &
    (df['timestamp'].dt.date <= tarih_araligi[1]) &
    (df['city'].isin(secili_sehirler))
]

if df_filtreli.empty:
    st.warning("Seçilen filtrelerle eşleşen veri bulunamadı.")
    st.stop()

# 📊 GRAFİKLER
st.markdown("### 📈 Emisyon Trendleri")

col1, col2 = st.columns(2)

with col1:
    fig_toplam = px.line(df_filtreli, x='timestamp', y='toplam_emisyon',
                        title="Toplam Karbon Emisyonu (Zamana Göre)",
                        labels={'timestamp': 'Tarih', 'toplam_emisyon': 'kg CO₂'},
                        line_shape='spline',
                        color_discrete_sequence=['#00FF00'])
    fig_toplam.update_layout(height=320)
    st.plotly_chart(fig_toplam, use_container_width=True)

with col2:
    fig_elektrik = px.area(df_filtreli, x='timestamp', y='elektrik_emisyonu',
                       title="Elektrik Tüketimi Emisyonu",
                       labels={'timestamp': 'Tarih', 'elektrik_emisyonu': 'kg CO₂'},
                       color_discrete_sequence=["#FF14EB"])
    fig_elektrik.update_layout(height=320)
    st.plotly_chart(fig_elektrik, use_container_width=True)

st.markdown("### 🥩🚗 Et ve Ulaşım Emisyonları")

col3, col4 = st.columns(2)

with col3:
    fig_et = go.Figure()
    renkler = {'dana': 'red', 'tavuk': 'orange'}
    for et in secili_etler:
        fig_et.add_trace(go.Scatter(x=df_filtreli['timestamp'], y=df_filtreli[et],
                                      mode='lines', name=et.capitalize(),
                                      line=dict(color=renkler.get(et, 'gray'))))
    fig_et.update_layout(title="🥩 Et Türlerine Göre Emisyonlar", 
                           xaxis_title="Tarih", yaxis_title="kg CO₂", height=320)
    st.plotly_chart(fig_et, use_container_width=True)

with col4:
    fig_ulasim = go.Figure()
    if 'araba' in secili_ulasim:
        fig_ulasim.add_trace(go.Scatter(x=df_filtreli['timestamp'], y=df_filtreli['araba'],
                                           mode='lines', name='Araba', line=dict(color='gray')))
    if 'ucus_emisyonu' in secili_ulasim:
        fig_ulasim.add_trace(go.Scatter(x=df_filtreli['timestamp'], y=df_filtreli['ucus_emisyonu'],
                                           mode='lines', name='Uçuş', line=dict(color='skyblue')))
    fig_ulasim.update_layout(title="🚗 Ulaşım Türlerine Göre Emisyonlar", 
                                xaxis_title="Tarih", yaxis_title="kg CO₂", height=320)
    st.plotly_chart(fig_ulasim, use_container_width=True)

# Isı Haritası
st.markdown("### 🗺️ Şehir Bazında Günlük Emisyon Isı Haritası")
df_filtreli['ay'] = df_filtreli['timestamp'].dt.to_period('M').astype(str)
harita_verisi = df_filtreli.groupby(['city', 'ay'])['toplam_emisyon'].sum().unstack(fill_value=0)

fig_harita = px.imshow(harita_verisi,
                        labels=dict(x="Ay", y="Şehir", color="Emisyon (kg CO₂)"),
                        x=harita_verisi.columns,
                        y=harita_verisi.index,
                        color_continuous_scale='Viridis',
                        height=400)
fig_harita.update_layout(title="Günlük Emisyon Isı Haritası")
st.plotly_chart(fig_harita, use_container_width=True)
