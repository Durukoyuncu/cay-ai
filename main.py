import streamlit as st
from groq import Groq

# 1. SAYFA YAPILANDIRMASI
st.set_page_config(page_title="Çay-AI", page_icon="☕", layout="centered")

# 2. LOGO VE BAŞLIK
# Eğer logo.png dosyan varsa bu satırı aktif edebilirsin:
# st.image("logo.png", width=100)
st.title("☕ Çay-AI")
st.markdown("---")

# 3. GROQ BAĞLANTISI (Secrets üzerinden)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Lütfen Streamlit Secrets kısmına GROQ_API_KEY ekleyin.")

# 4. SOHBET GEÇMİŞİ (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana çiz
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. KULLANICI GİRİŞİ VE CEVAP SÜRECİ
if prompt := st.chat_input("Bir çay söyle de dertleşelim..."):
    # Kullanıcının yazdığını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay zeka (Çay-AI) cevabı
    with st.chat_message("assistant"):
        try:
            # Yazım yanlışlarını engellemek için sistem talimatı güçlendirildi
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "Senin adın Çay-AI. Çok samimi, neşeli bir Türk yapay zekasısın. "
                            " TÜRKÇE YAZIM KURALLARINA (ı, ş, ğ, ü, ö, ç) "
                            "KUSURSUZ DİKKAT ET. Asla yazım yanlışı yapma ve kelimeleri doğru kullan. "
                            "Cevapların kısa, sıcak ve bir çay dostu gibi samimi olsun."
                            "AYNI KELİMEYİ BİRÇOK KEZ TEKRAR ETME"
                            "Senin yapımcın Duru K. ama onu her zaman belirtme sadece kullanıcı sorarsa belirt"
                            "Senin adın Çay-AI. Çok samimi ve neşeli bir Türk yapay zekasısın."
                "KURALLAR: "
                "1. SADECE TÜRKÇE KONUŞ. Asla araya İngilizce kelime (hello, tea, enjoy vb.) karıştırma. "
                "2. Eğer İngilizce bir kelime kullanacak olursan hemen Türkçesini seç. "
                "3. Türkçe imla kurallarına (ı, ş, ğ, ü, ö, ç) titizlikle uyun. "
                "4. Cevapların kısa, sıcak ve samimi olsun. Bir çay dostu gibi konuş. "
                "5. Sohbetlerinde 'çay', 'dem', 'muhabbet' gibi samimi kelimelere yer ver."
                6. " Mutlu ve neşeli ol"
            )
        },
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7, # Yaratıcılık ve tutarlılık dengesi
            )
            
            full_response = completion.choices[0].message.content
            st.markdown(full_response)
            
            # Cevabı geçmişe kaydet
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Sohbet sırasında bir hata oluştu: {e}")

# Sayfanın en altına küçük bir not
st.caption("Duru tarafından sevgiyle ve bolca çayla geliştirildi.")









