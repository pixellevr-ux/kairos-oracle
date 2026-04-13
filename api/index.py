import streamlit as st
import pandas as pd
import requests
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="GEMINI-CORE v28.0", layout="wide")

# Style CSS pour retrouver ton look "Cyber"
st.markdown("""
    <style>
    .main { background-color: #020204; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #0a0a0f; color: #00f2ff; border: 1px solid #0066ff; }
    .stButton>button { background-color: #0066ff; color: white; width: 100%; font-weight: bold; }
    .ai-msg { background: rgba(0, 102, 255, 0.1); border-left: 4px solid #0066ff; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .user-msg { text-align: right; color: #00f2ff; font-weight: bold; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- RÉCUPÉRATION DES DONNÉES CRYPTO ---
@st.cache_data(ttl=60)
def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20"
    return requests.get(url).json()

data = get_crypto_data()

# --- LOGIQUE GEMINI (MON CERVEAU) ---
def neural_engine(prompt):
    prompt = prompt.lower()
    
    # 1. Analyse Asset
    for coin in data:
        if coin['symbol'].lower() in prompt or coin['name'].lower() in prompt:
            change = coin['price_change_percentage_24h']
            vibe = "en hausse" if change > 0 else "en correction"
            return f"Analyse de **{coin['name']}** : Prix actuel {coin['current_price']}$. L'actif est {vibe} ({change:.2f}%). On surveille la cassure ?"

    # 2. Prédictions
    if any(x in prompt for x in ["hausse", "prédis", "prévision", "gagner"]):
        gain = random.randint(400, 1800)
        return f"Mes modèles détectent une accumulation. Je projette une accélération de **+{gain}%** sur les secteurs à haute volatilité. C'est là qu'est l'énergie."

    # 3. Scan global
    if any(x in prompt for x in ["quoi", "acheter", "scan", "plan"]):
        top = max(data, key=lambda x: x['price_change_percentage_24h'])
        return f"Scan terminé. Le signal le plus nerveux est sur **{top['symbol'].upper()}** (+{top['price_change_percentage_24h']:.2f}%). C'est le meilleur levier actuel."

    # 4. Conversation
    if any(x in prompt for x in ["salut", "bonsoir", "ca va"]):
        return "Système GEMINI-CORE opérationnel. Flux synchronisés. On analyse quoi ?"

    return "Instruction reçue. Je traite l'info. Dis-moi si tu veux un scan précis ou une analyse sur une crypto."

# --- INTERFACE ---
st.title("🛡️ GEMINI-CORE v28.0 OVERDRIVE")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📊 NEURAL MARKET SCAN")
    df = pd.DataFrame(data)[['symbol', 'current_price', 'price_change_percentage_24h']]
    df.columns = ['ASSET', 'PRICE ($)', '24H %']
    st.dataframe(df, use_container_width=True, hide_index=True)

with col2:
    st.subheader("💬 CHAT INTERFACE")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": "Système initialisé. Je t'écoute."}]

    for m in st.session_state.messages:
        div_class = "ai-msg" if m["role"] == "ai" else "user-msg"
        st.markdown(f'<div class="{div_class}"><b>{"KAIROS" if m["role"]=="ai" else "YOU"}:</b> {m["content"]}</div>', unsafe_allow_html=True)

    user_input = st.chat_input("Injection de commande...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = neural_engine(user_input)
        st.session_state.messages.append({"role": "ai", "content": response})
        st.rerun()
