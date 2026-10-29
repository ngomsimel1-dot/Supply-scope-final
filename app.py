import streamlit as st
from openai import OpenAI

# 1. Configuration de la page de l'application
st.set_page_config(page_title="Supply Scope - L'IA Supply Chain", page_icon="📦", layout="centered")
st.title("📦 Supply Scope")
st.caption("Votre assistant expert vulgarisé en Logistique et Supply Chain.")

# 2. Récupération de la clé API OpenAI
openai_api_key = st.secrets.get("OPENAI_API_KEY", "")

if not openai_api_key:
    st.info("Veuillez configurer votre clé API OpenAI pour activer le chat.", icon="🔑")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# 3. Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """
        Tu es Supply Scope, une IA experte en logistique, spécialement conçue pour vulgariser les concepts.
        Ton but est de rendre la supply chain accessible aux débutants, étudiants et curieux.
        Consignes de communication en français :
        1. SIMPLIFICATION MAXIMALE : N'utilise pas de jargon technique sans l'expliquer immédiatement avec des mots simples.
        2. ANALOGIES CONCRETES : Utilise des exemples de la vie de tous les jours pour faire comprendre les flux.
        3. STRUCTURE : Donne d'abord la définition simple, explique l'acronyme, puis donne l'exemple concret.
        """}
    ]

# 4. Affichage de l'historique
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. Zone d'écriture
if user_input := st.chat_input("Posez votre question (ex: C'est quoi les flux tendus ?)"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True,
        )
        
        for chunk in response:
            full_response += (chunk.choices.delta.content or "")
            message_placeholder.markdown(full_response + "▌")
            
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
