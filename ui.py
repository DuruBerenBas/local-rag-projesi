import streamlit as st
import requests

# 1. Sayfa Konfigürasyonu ve Estetik Ayarlar
st.set_page_config(page_title="AI Corporate Assistant", page_icon="🏢", layout="wide")

# Özel CSS ile Arayüzü Güzelleştirme
# Özel CSS ile Arayüzü Güzelleştirme
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }

    /* Sidebar Buton Tasarımı */
    .stButton>button {
        width: 100% !important;
        border-radius: 8px;
        height: auto !important;
        padding: 12px 10px !important;
        background-color: #FF4B4B;
        color: white !important;
        font-weight: 500;
        font-size: 13px !important;
        border: none;
        white-space: normal !important; /* Metnin alt satıra geçmesini sağlar */
        line-height: 1.4 !important;
        margin-bottom: 8px;
        display: block;
        text-align: left; /* Soruların daha okunaklı olması için sola yasladık */
    }

    /* Butona dokunulduğunda oluşacak efekt */
    .stButton>button:hover {
        background-color: #ff3333;
        color: white !important;
        border: none;
    }

    /* Cevap kutusu metin rengi ve stili */
    .response-box {
        padding: 20px;
        background-color: white;
        border-radius: 15px;
        border-left: 5px solid #FF4B4B;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        color: #1f1f1f !important; /* Metni koyu gri/siyah yaparak netleştiriyoruz */
        font-size: 16px;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Yan Menü (Sidebar) - Kurumsal Bilgi Alanı

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=80)
    st.title("Asistan Paneli")
    st.info("Kategorilere tıklayarak sistemin zekasını test edebileceğiniz senaryoları görebilirsiniz.")
    st.divider()

    # 7 Ana Konu ve 4'er Mantıklı Soru
    menu_data = {
        "🛠️ Garanti ve Teknik Destek": [
            "SmartGözlük V2 ürünüm su dolu lavaboya düştü, ücretsiz tamir edilir mi?",
            "Cihazımı alalı 25 ay oldu, hala garantiden faydalanabilir miyim?",
            "Kullanıcı hatası olan ekran kırılmaları garanti kapsamında mıdır?",
            "Ürünün pili 1 yıl sonra şişti, bu durumda değişim yapılır mı?"
        ],
        "🦷 Özel Sağlık Sigortası": [
            "Eşimin 5.000 TL tutan kanal tedavisi için ne kadar ödeme alabilirim?",
            "Yeni doğan bebeğimi sigorta kapsamına dahil edebilir miyim?",
            "Yıllık diş muayenesi ve temizliği için limitimiz ne kadardır?",
            "Gözlük camı değişimi için sigorta ödeme yapıyor mu, limiti nedir?"
        ],
        "📦 İade ve İptal Süreçleri": [
            "Keyfi iadelerde kargo ücretini şirketin ödemesi zorunlu mu?",
            "İade ettiğim ürünün parası banka hesabıma tam olarak ne zaman yatar?",
            "Kusurlu çıkan bir ürünün iade kargo süreci nasıl işler?",
            "Müşteri temsilcisini 1 dakika bekledim, memnuniyetsizlik iadesi yapabilir miyim?"
        ],
        "🔥 Acil Durum ve Yangın": [
            "Mutfakta yangın çıktı, 112'yi mi aramalıyım yoksa yangın tüpü mü kullanmalıyım?",
            "Yangın anında tahliye için asansörü kullanmak neden yasaktır?",
            "Ofis içinde şüpheli bir paket gördüğümde ilk kime haber vermeliyim?",
            "Acil tahliye sırasında toplanma merkezimiz tam olarak neresidir?"
        ],
        "🤝 Tedarikçi Etik Kuralları": [
            "Bir tedarikçi bana 500 TL değerinde bir hediye çeki verdi, kabul etmeli miyim?",
            "15 yaşında bir çocuk, tedarikçimizde stajyer olarak çalışabilir mi?",
            "Tedarikçimizin sunduğu ücretsiz akşam yemeği davetine katılabilir miyim?",
            "Tedarikçi firmada çalışan bir yakınım olması çıkar çatışması yaratır mı?"
        ],
        "💻 Bilgi Güvenliği": [
            "Şirket bilgisayarıma kaynağını bilmediğim bir USB taktım, ne yapmalıyım?",
            "Şirket şifremi iş arkadaşımla acil bir durum için paylaşabilir miyim?",
            "Halka açık bir kafede çalışırken şirket verilerine erişmek güvenli mi?",
            "E-postama gelen şüpheli bir linke tıkladığımda BT birimine nasıl ulaşırım?"
        ],
        "🪑 Ofis ve Uzaktan Çalışma": [
            "Ofis koltuğum kırıldı, ikinci kez 5.000 TL koltuk ödeneği alabilir miyim?",
            "Evden çalışırken internetim kesilirse bunu kime bildirmem gerekir?",
            "Şirketin sağladığı monitörü evde kullanmak için dışarı çıkarabilir miyim?",
            "Uzaktan çalışma günlerinde mesai saatleri dışında gelen taleplere bakmalı mıyım?"
        ]
    }

    # Akordeon Menülerin Oluşturulması
    for kategori, sorular in menu_data.items():
        with st.expander(kategori):
            for s in sorular:
                if st.button(s, key=s): # Her soru için benzersiz key
                    st.session_state.soru_input = s
                    st.rerun() # Sayfayı yenileyerek soruyu kutuya doldur

# 3. Ana Sayfa Tasarımı

col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2593/2593635.png", width=80)
with col2:
    st.title("SmartCorp Akıllı Asistan")
    st.caption("Llama 3 ve RAG Teknolojisi ile Güçlendirilmiş Kurumsal Çözüm")

# Session state yönetimi (Örnek soruların kutuya dolması için)
if 'soru_input' not in st.session_state:
    st.session_state.soru_input = ""

# Soru Giriş Alanı

soru = st.text_area("Hangi konuda yardıma ihtiyacınız var?",
                    value=st.session_state.soru_input,
                    placeholder="Soru sormak için buraya yazın...",
                    height=120)

if st.button("Yapay Zekaya Sor"):
    if soru:
        with st.spinner("🔍 Dokümanlar taranıyor ve analiz ediliyor..."):
            try:
                response = requests.post("http://127.0.0.1:8000/ask", json={"soru": soru})
                if response.status_code == 200:
                    cevap = response.json().get("yapay_zeka_cevabi", "")
                    st.markdown("### 🤖 Yanıt")
                    st.markdown(f'<div class="response-box">{cevap}</div>', unsafe_allow_html=True)
                else:
                    st.error("Sunucu ile iletişim kurulamadı.")
            except:
                st.error("Arka plan API'si kapalı! Lütfen FastAPI'yi (8000) çalıştırın.")
    else:
        st.warning("Lütfen bir soru girin.")