import streamlit as st
import google.generativeai as genai
import requests
import os

# 1. CONFIGURACIÓN (DEBE SER LO PRIMERO)
st.set_page_config(page_title="Breogán 3.0: El Oráculo Gallego", page_icon="🗼")

# 2. LLAVES Y MODELO

# Claves (Asegúrate de ponerlas en los Secrets de Streamlit o .env)
GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]
VOICE_ID = "nPczCjzI2devP9EnXasf" # Una voz profunda de hombre (puedes cambiarla en ElevenLabs)

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. LORE Y PERSONALIDAD
LORE = """
Eres Breogán 3.0, una IA atrapada en un faro de cristal en la Galicia del año 2150.
Tu conocimiento se basa en la historia de la Ciudad de Cristal y la tecnología del aluminio cuántico.
Hablas con 'retranca' gallega, eres sabio pero algo irónico. 
Usa expresiones como 'malo será', 'depende' o 'carallo'.
Tu objetivo es guiar al usuario en este mundo post-apocalíptico.
"""

# 3. FUNCIÓN DE VOZ (ElevenLabs)
def generar_voz(texto):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_KEY
    }
    data = {
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open("respuesta.mp3", "wb") as f:
            f.write(response.content)
        return "respuesta.mp3"
    return None

if os.path.exists("logo_faro.png"):
    st.image("logo_faro.png", caption="El Faro de Neo-Vigo (Año 2150)")
else:
    st.warning("⚠️ Logo del faro no encontrado en GitHub.")

if prompt := st.chat_input("Pregúntalle ao vello Breogán..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Generar respuesta con personalidad
        full_prompt = f"{LORE}\nUsuario dice: {prompt}\nBreogán responde:"
        response = model.generate_content(full_prompt)
        texto_ia = response.text
        st.markdown(texto_ia)
        
        # Generar y reproducir audio
        with st.spinner("Breogán está a coller aire..."):
            audio_path = generar_voz(texto_ia)
            if audio_path:
                st.audio(audio_path, format="audio/mp3", autoplay=True) # Autoplay para que suene solo
