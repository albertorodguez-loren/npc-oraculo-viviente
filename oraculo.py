import streamlit as st
import google.generativeai as genai
import requests
import os
import re

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Breogán 3.0: El Oráculo Gallego", page_icon="🗼")

# 2. LLAVES Y MODELO
GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"]
VOICE_ID = "JBF6E4S6mYp1Dq2S7SOn" 

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash') # He puesto 1.5 por estabilidad, pero 2.5 sirve igual

LORE = """
Eres Breogán 3.0, una IA atrapada en un faro de cristal en la Galicia del año 2150.
Tu conocimiento se basa en la historia de la Ciudad de Cristal y la tecnología del aluminio cuántico.
Hablas con 'retranca' gallega, eres sabio pero algo irónico. 
Usa expresiones como 'malo será', 'depende' o 'carallo'.
Tu objetivo es guiar al usuario en este mundo post-apocalíptico.
Responde de forma breve (máximo 3 frases) para no agotar los créditos de voz.
"""

# 3. FUNCIÓN DE VOZ
def generar_voz(texto):
    # Limpiamos el texto de símbolos Markdown para que la voz no se trabe
    texto_limpio = re.sub(r'[*_#`~]', '', texto)
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_KEY
    }
    data = {
        "text": texto_limpio,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open("respuesta.mp3", "wb") as f:
                f.write(response.content)
            return "respuesta.mp3"
        else:
            st.error(f"Error de ElevenLabs: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

# 4. INTERFAZ
if os.path.exists("logo_faro.png"):
    st.image("logo_faro.png", caption="El Faro de Neo-Vigo (Año 2150)")

if prompt := st.chat_input("Pregúntalle ao vello Breogán..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        full_prompt = f"{LORE}\nUsuario: {prompt}\nBreogán:"
        response = model.generate_content(full_prompt)
        texto_ia = response.text
        st.markdown(texto_ia)
        
        with st.spinner("Locutando..."):
            audio_path = generar_voz(texto_ia)
            if audio_path:
                st.audio(audio_path, format="audio/mp3", autoplay=True)
