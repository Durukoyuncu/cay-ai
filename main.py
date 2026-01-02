import streamlit as st
from groq import Groq

# 1. SAYFA AYARLARI (En üstte olmalı)
st.set_page_config(page_title="Çay-AI", page_icon="☕")

# 2. GROQ BAĞLANTISI
# Streamlit Secrets kısmına GROQ_API_KEY yazdığından emin ol
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Bağlantı Ayarı Hatası: Lütfen Secrets kısmını kontrol et.")

# 3. BAŞLIK VE GÖRÜNÜM
st.title("☕ Çay-AI")
st.caption("Samimi, hızlı ve limitsiz sohbetin adresi.")

# 4. SOHBET GEÇMİŞİ
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana yansıt
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. KULLANICI GİRİŞİ VE CEVAP
if prompt := st.chat_input("Bir çay söyle de dertleşelim..."):
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay zeka cevabını oluştur
    with st.chat_message("assistant"):
        try:
            # Buradaki model en hızlı olanıdır
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Senin adın Çay-AI. Çok samimi, neşeli ve misafirperver bir Türk yapay zekasısın. Çayı çok seversin, her fırsatta çay ikram edersin. Cevapların kısa, sıcak ve samimi olsun."},
                    {"role": "user", "content": prompt}
                ],
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Sohbet sırasında bir hata oluştu: {e}")





