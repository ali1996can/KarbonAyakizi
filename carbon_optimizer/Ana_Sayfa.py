import streamlit as st
import pandas as pd
import plotly.express as px
from utils.calculator import calculate_emission, load_emission_factors, log_to_csv
from utils.predictor import load_model, predict_emission, load_encoder
from utils.advisor import generate_advice
from utils.simulator import simulate_scenarios
from streamlit.components.v1 import html



# Sayfa yapılandırması
st.set_page_config(
    page_title="Ana_Sayfa",
    page_icon="🏠",
    layout="wide"
    
)

st.title("🏠 Karbon Ayak İzi Hesaplayıcı")

# Emisyon faktörlerini yükle
emission_factors = load_emission_factors()

# Sidebar form (her zaman görünür)
with st.sidebar:
    st.header("📥 Veri Girişi")
    city = st.selectbox("Şehir", ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan", "Artvin",
    "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur",
    "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan",
    "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Iğdır", "Isparta", "İstanbul",
    "İzmir", "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kırıkkale", "Kırklareli", "Kırşehir",
    "Kilis", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş",
    "Nevşehir", "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas",
    "Şanlıurfa", "Şırnak", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"])
    beef = st.number_input("Dana eti (kg/ay)", min_value=0, value=0)
    chicken = st.number_input("Tavuk eti (kg/ay)", min_value=0, value=0)
    car = st.number_input("Araç kullanımı (km/ay)", min_value=0, value=0)
    electricity = st.number_input("Elektrik kullanımı (kWh/ay)", min_value=0, value=0)
    hesapla = st.button("Hesapla")

# Varsayılan: Son kayıtlı veriyi oku
try:
    df_log = pd.read_csv("results/usage_log.csv", parse_dates=["timestamp"])
    last = df_log.iloc[-1]
    input_data = {
        "beef": last["beef"],
        "chicken": last["chicken"],
        "car": last["car"],
        "electricity": last["electricity"],
        "city": last["city"]
    }
except:
    input_data = {
        "beef": 5.0,
        "chicken": 3.0,
        "car": 100.0,
        "electricity": 150.0,
        "city": "İstanbul"
    }
    df_log = pd.DataFrame()
# —––––– ORTALAMA KARTLARI (ESTETİK VE SİMGELİ) —–––––


if not df_log.empty:
    avg_beef = df_log["beef"].mean()
    avg_chicken = df_log["chicken"].mean()
    avg_elec = df_log["electricity"].mean()
    avg_car = df_log["car"].mean()

    st.markdown("### 📊 Geçmiş Verilere Göre Aylık Ortalamalar")

    # Stil tanımı
    st.markdown("""
    <style>
    /* Sidebar arka plan */
    .css-1d391kg {
        background-color: #2e0854 !important;  /* koyu mor */
    }

    /* Sidebar içindeki yazılar */
    .css-1d391kg * {
        color: #d8b9ff !important; /* açık mor */
    }

    /* Sidebar başlıkları daha parlak neon mor */
    .css-1d391kg h2, .css-1d391kg h3, .css-1d391kg h4 {
        color: #b845fc !important;
    }
    </style>
""", unsafe_allow_html=True)


    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="small-card">
            <div class="small-icon">🥩</div>
            <div class="small-label">Dana Eti (kg/ay)</div>
            <div class="small-value">{avg_beef:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="small-card">
            <div class="small-icon">🍗</div>
            <div class="small-label">Tavuk Eti (kg/ay)</div>
            <div class="small-value">{avg_chicken:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="small-card">
            <div class="small-icon">⚡</div>
            <div class="small-label">Elektrik (kWh/ay)</div>
            <div class="small-value">{avg_elec:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="small-card">
            <div class="small-icon">🚗</div>
            <div class="small-label">Araç Kullanımı (km/ay)</div>
            <div class="small-value">{avg_car:.0f}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Henüz kayıtlı veri bulunamadı.")





# Eğer kullanıcı hesapla butonuna bastıysa, form verilerini al
if hesapla:
    input_data = {
        "beef": beef,
        "chicken": chicken,
        "car": car,
        "electricity": electricity,
        "city": city
    }
    log_to_csv(input_data, calculate_emission(input_data, emission_factors)[0])
    st.rerun()
()

# Hesaplama yap
total_emission, details = calculate_emission(input_data, emission_factors)

col1, col2 = st.columns(2)
if not df_log.empty:
    # kart kodları...
    
    # BURADAN HEMEN SONRA EKLE
    st.markdown("""
    <hr style='border: 1px solid #39ff14; margin-top: 15px; margin-bottom: 25px;' />
    """, unsafe_allow_html=True)

# Sol kolon: Emisyon ve dağılım
# ——— Toplam Emisyon, Model Tahmini ve Fark kutuları yan yana ———
# —––– Toplam Emisyon - Model Tahmini - Fark Kartları —–––
import streamlit.components.v1 as components

# Küçük kartlar için stil tanımı (tek sefer yazmak yeterli)
st.markdown("""
<style>
.small-card {
  backdrop-filter: blur(4px);
  background: rgba(20, 20, 20, 0.4);
  border-radius: 8px;
  padding: 6px;
  box-shadow: 0 0 8px rgba(57, 255, 20, 0.12);
  text-align: center;
  border: 1px solid rgba(57, 255, 20, 0.1);
  margin-bottom: 5px;
}
.small-card:hover {
  transform: scale(1.02);
  box-shadow: 0 0 10px rgba(57, 255, 20, 0.3);
}
.small-icon {
  font-size: 16px;
  margin-bottom: 3px;
  color: #39ff14;
}
.small-label {
  color: #bbbbbb;
  font-size: 14px;
  margin: 0;
}
.small-value {
  color: #39ff14;
  font-size: 13px;
  font-weight: bold;
  margin-top: 2px;
}

</style>
""", unsafe_allow_html=True)

# Kartlar için sütunlar
col1, col2, col3 = st.columns(3)

# 🌍 Toplam Emisyon
with col1:
    st.markdown(f"""
    <div class="small-card">
        <div class="small-icon">🌍</div>
        <div class="small-label">Toplam Emisyon</div>
        <div class="small-value">{total_emission:.2f} kg CO₂</div>
    </div>
    """, unsafe_allow_html=True)

# 🤖 Model Tahmini
with col2:
    try:
        model = load_model()
        encoder = load_encoder()
        prediction = predict_emission(model, input_data, encoder)
        fark = abs(prediction - total_emission)

        st.markdown(f"""
        <div class="small-card">
            <div class="small-icon">🤖</div>
            <div class="small-label">Model Tahmini</div>
            <div class="small-value">{prediction:.2f} kg CO₂</div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Model tahmini yapılamadı: {e}")
        prediction = None
        fark = None

# ⚖️ Fark
with col3:
    if prediction is not None:
        st.markdown(f"""
        <div class="small-card">
            <div class="small-icon">⚖️</div>
            <div class="small-label">Fark</div>
            <div class="small-value">{fark:.2f} kg CO₂</div>
        </div>
        """, unsafe_allow_html=True)



# Grafikler: Pasta ve Zaman Serisi Yan Yana
# 🔢 Toplam Emisyon Kartı


chart_col1, chart_col2 = st.columns(2)


st.markdown("### 📊 Emisyon Dağılımı ve Zaman Serisi")
col_pie, col_line = st.columns(2)

# Pie Chart
with col_pie:
    if details:
        labels = list(details.keys())
        values = [emission for _, (_, emission) in details.items()]
        fig_pie = px.pie(names=labels, values=values, title="Emisyon Dağılımı")
        fig_pie.update_layout(height=300, font=dict(size=12), margin=dict(t=30, b=20, l=20, r=20))
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Emisyon verisi (details) bulunamadı.")

# Zaman Serisi
with col_line:
    if not df_log.empty:
        fig_line = px.line(df_log, x="timestamp", y="total_emission", markers=True)
        fig_line.update_layout(height=300, font=dict(size=12), margin=dict(t=30, b=20, l=20, r=20))
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Henüz zaman serisi verisi yok.")



# Öneriler
st.subheader("💡 Öneriler")
for suggestion in generate_advice(details):
    st.info(suggestion)

# Simülasyon
st.subheader("🔮 Senaryo Simülasyonu")
sim_col1, sim_col2 = st.columns(2)
for i, (label, new_emission) in enumerate(simulate_scenarios(input_data, emission_factors)):
    with (sim_col1 if i % 2 == 0 else sim_col2):
        st.write(f"**{label}**")
        st.success(f"Yeni Emisyon: {new_emission:.2f} kg CO₂ | Tasarruf: {total_emission - new_emission:.2f} kg")

# Veri tablosu
st.subheader("📊 Kayıtlı Veriler")
if not df_log.empty:
    st.dataframe(df_log.sort_values("timestamp", ascending=False))
else:
    st.info("Henüz kayıtlı veri bulunamadı.")