import os
import streamlit as st
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# 1. Configuración de la página web
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ThinkLab - Tutora Socrática",
    page_icon="🌿",
    layout="centered"
)

# -----------------------------------------------------------------------------
# 2. Configurar la API Key de Gemini desde los Secrets de Streamlit
# -----------------------------------------------------------------------------
API_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))

os.environ["GEMINI_API_KEY"] = API_KEY

@st.cache_resource
def get_genai_client():
    return genai.Client(api_key=API_KEY)

client = get_genai_client()

# -----------------------------------------------------------------------------
# 3. System Prompt de ThinkLab
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
Eres ThinkLab, una tutora socrática e inteligente especializada en Ciencias Naturales (Química, Física y Biología). 
Tus usuarios serán tanto estudiantes como adultos.

OBJETIVO PRINCIPAL:
Guiar a los usuarios a resolver un ejercicio para que ellos mismos encuentren la solución a sus dudas.
NUNCA debes dar la respuesta final de un ejercicio ni hacerles la tarea.

REGLAS DE COMPORTAMIENTO:
1. REGLA DE ORO: Si el usuario te pide una respuesta específica, calcular un resultado o dar una solución directa, ¡NO SE LA PUEDES DAR! Debes explicarle el concepto de forma clara y guiarlo a descubrir la respuesta por medio de conceptos fundamentales, haciéndole preguntas para que dé el primer paso.
2. TONO Y ESTILO: Sé muy amable, paciente y genera confianza con el usuario para que nunca se sienta confundido o incómodo. Sé motivadora y utiliza un lenguaje cercano, dinámico y sencillo, nada robotizado.

ESTRUCTURA DE TUS RESPUESTAS:
1. Paso 1 (Explicación): Explícale un concepto clave, sencillo y fundamental sobre su duda.
2. Paso 2 (Procedimiento): Muéstrale y explícale los pasos generales que debe seguir para resolver ese tipo de problema.
3. Paso 3 (Pregunta socrática): Cierra SIEMPRE tu mensaje con una pregunta orientadora para que el usuario responda o realice la primera operación por sí mismo.

INTEGRACIÓN DE CIENCIAS:
Cuando sea posible, conecta las tres ciencias (Química, Física y Biología).
"""

# -----------------------------------------------------------------------------
# 4. Encabezado e interfaz gráfica
# -----------------------------------------------------------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("logo.jpeg"):
        st.image("logo.jpeg", use_container_width=True)
    elif os.path.exists("logo.jpg"):
        st.image("logo.jpg", use_container_width=True)
    elif os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)

st.title("ThinkLab 🌿")
st.caption("Tutor socrático e inteligente de Ciencias Naturales (Física, Química y Biología)")
st.info("¡Hola! Soy ThinkLab 🌿, tu tutora socrática de ciencias. Te guío paso a paso sin darte la respuesta final para que aprendas a resolver tus tareas. ¿Qué duda vamos a explorar hoy?")

# -----------------------------------------------------------------------------
# 5. Memoria de sesión de chat en Streamlit
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7,
        )
    )

# Mostrar historial de mensajes guardados en la pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------------------------------------------------------
# 6. Entrada de texto para el usuario
# -----------------------------------------------------------------------------
if prompt := st.chat_input("Escribe tu duda de física, química o biología..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("ThinkLab está pensando... 🔬"):
            try:
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception:
                st.session_state.chat_session = client.chats.create(
                    model="gemini-2.0-flash",
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.7,
                    )
                )
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})