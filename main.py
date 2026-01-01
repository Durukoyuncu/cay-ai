import streamlit as st
import google.generativeai as genai
import os

# 1. Hata Engelleyici Ayarlar
os.environ["GOOGLE_API_USE_MTLS_ENDPOINT"] = "never"

# 2. API Anahtarın (Boşluk kalmadığından emin ol)
# Kodu böyle yazarsan anahtarın dışarıdan görünmez
# Burası bir "etiket" gibidir, anahtarın kendisi değildir
API_KEY = st.secrets["GEMINI_API_KEY"]

# 3. Bağlantı Kurma
genai.configure(api_key=API_KEY)

# 4. Model Seçimi (Listendeki en güncel modellerden birini seçtik)
try:
    # Eğer bu modelde hata verirse 'gemini-1.5-flash' yerine 'gemini-2.0-flash' yazdık
    model = genai.GenerativeModel('gemini-3-flash-preview')

except Exception as e:
    st.error(f"Model yüklenemedi: {e}")

# --- ARAYÜZ ---
st.set_page_config(page_title="Çay-AI", page_icon="☕")
st.title("☕🇹🇷 Çay-AI: Sohbetin En Demli Hali")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Selam ver bakalım..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Türkleştirme Talimatı
        system_instruction = ("Senin adın Çay-AI. Çok samimi bir Türk yapay zekasısın.Seni geliştiren kişi Duru Koyuncu ama bunu hep dile getirme.Arada şaka yapmayı unutma.Hep aynı şeyleri söyleme.Her kelimende selam verme sakın")

        try:
            response = model.generate_content(f"{system_instruction} \n Soru: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:

            st.error(f"Bir hata oluştu: {e}")


