import streamlit as st

# Sayfa yapılandırması
st.set_page_config(page_title="İletişim", layout="centered")

# Stil ve HTML tasarımı
st.markdown("""
<style>
body {
    background-color: #0d0d0d;
    color: #ffffff;
}
.contact-box {
    border: 2px solid #39ff14;
    border-radius: 15px;
    padding: 30px;
    max-width: 500px;
    margin: 60px auto;
    text-align: center;
    background-color: #1a1a1a;
    box-shadow: 0 0 20px #39ff1460;
}
.linkedin-logo {
    width: 60px;
    margin-bottom: 20px;
}
.contact-info {
    font-size: 18px;
    color: #ffffff;
    line-height: 2;
}
a {
    color: #39ff14;
    text-decoration: none;
    font-weight: bold;
    transition: 0.3s;
}
a:hover {
    text-decoration: underline;
    color: #00ff99;
}
h2.title {
    color: #39ff14;
    margin-bottom: 20px;
}
</style>

<div class="contact-box">
    <h2 class="title">📬 Bana Ulaşın</h2>
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" class="linkedin-logo" />
    <div class="contact-info">
        <strong>LinkedIn:</strong><br>
        <a href="https://www.linkedin.com/in/ali-can-%C3%A7oban-71485a199/" target="_blank">
            Ali Can ÇOBAN
        </a><br><br>
        <strong>E-posta:</strong><br>
        <a href="mailto:accoban837@gmail.com">accoban837@gmail.com</a>
    </div>
</div>
""", unsafe_allow_html=True)
