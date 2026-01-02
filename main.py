import streamlit as st
from groq import Groq

# API Anahtarını Streamlit Secrets'tan alıyoruz
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Secrets ayarlarında GROQ_API_KEY bulunamadı!")

st.set_page_config(page_title="Çay-AI", page_icon="☕")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
st.title("☕ Çay-AI (Hızlı & Limitsiz)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Çaylar benden, sohbet senden..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Llama 3.3 modeli çok hızlı ve zekidir
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Senin adın Çay-AI. Çok samimi ve neşeli bir Türk yapay zekasısın. Çayı çok seversin. Cevapların kısa ve öz olsun."},
                    {"role": "user", "content": prompt}
                ],
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")




