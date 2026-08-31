import os
import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(
    page_title="ThinkLab - Tutora Socrática",
    page_icon="🌿",
    layout="centered"
)

# Obtener API Key de los Secrets de Streamlit
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
genai.configure(api_key=api_key)

# System Prompt
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

# Interfaz gráfica
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

# Inicializar modelo
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# Memoria de sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt := st.chat_input("Escribe tu duda de física, química o biología..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("ThinkLab está pensando... 🔬"):
            try:
                # Formatear el historial de chat para la API
                history = []
                for msg in st.session_state.messages[:-1]:
                    role = "user" if msg["role"] == "user" else "model"
                    history.append({"role": role, "parts": [msg["content"]]})

                chat = model.start_chat(history=history)
                response = chat.send_message(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error al conectar con Gemini: {e}")