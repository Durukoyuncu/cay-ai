import streamlit as st
from groq import Groq

# 1. SAYFA YAPILANDIRMASI
st.set_page_config(page_title="Çay-AI", page_icon="☕", layout="centered")

# 2. BAŞLIK
st.title("☕ Çay-AI")
st.markdown("---")

# 3. GROQ BAĞLANTISI
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Secrets ayarlarında GROQ_API_KEY bulunamadı!")

# 4. SOHBET GEÇMİŞİ
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. KULLANICI GİRİŞİ VE CEVAP
if prompt := st.chat_input("Bir çay söyle de dertleşelim..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Buradaki parantezlere ve virgüllere çok dikkat ettik:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "Senin adın Çay-AI. Çok samimi ve neşeli bir Türk yapay zekasısın. "
                            "SADECE TÜRKÇE KONUŞ. Asla araya İngilizce kelime karıştırma. "
                            "Türkçe imla kurallarına kusursuz dikkat et. "
                            "Cevapların kısa, sıcak ve samimi olsun."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

st.caption("Duru tarafından geliştirildi.")










