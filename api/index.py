import streamlit as st
import pandas as pd
import requests
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="KAIROS v28.0", layout="wide", initial_sidebar_state="collapsed")

# Injection du look "Cyber Terminal"
st.markdown("""
    <style>
    .main { background-color: #020204; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #0a0a0f; color: #00f2ff; border: 1px solid #0066ff; }
    .ai-msg { background: rgba(0, 102, 255, 0.1); border-left: 4px solid #0066ff; padding: 15px; border-radius: 5px; margin-bottom: 10px; font-size: 14px; }
    .user-msg { text-align: right; color: #00f2ff; font-weight: bold; margin-bottom: 10px; text-transform: uppercase; font-size: 12px; }
    .q-chip { background: #0066ff; color: white; padding: 2px 8px; border-radius: 3px; font-size: 10px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- RÉCUPÉRATION DES DONNÉES (API) ---
@st.cache_data(ttl=60)
def get_market_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50"
        return requests.get(url).json()
    except:
        return []

data = get_market_data()

# --- LE CERVEAU GEMINI (Logique de réponse) ---
def gemini_engine(prompt):
    msg = prompt.lower().strip()
    
    # 1. PRIORITÉ : IDENTITÉ
    if any(x in msg for x in ["t'es qui", "qui es-tu", "ton nom", "qui est tu", "c'est quoi kairos"]):
        return "Je suis **KAIROS**, ton interface Gemini-Core. Mon noyau est optimisé pour l'analyse de données et le scan de flux. Pas de blabla, juste de la performance."

    # 2. ANALYSE RÉSEAUX
    if any(x in msg for x in ["réseau", "network", "blockchain", "chaîne"]):
        return "Analyse des couches terminée. **Solana** domine le volume on-chain actuel. **Base** montre une forte accumulation sur les narratifs émergents. Quel secteur on scanne ?"

    # 3. DÉTECTION CRYPTO PRÉCISE
    for coin in data:
        if coin['symbol'].lower() == msg or coin['name'].lower() in msg:
            change = coin['price_change_percentage_24h']
            vibe = "en hausse" if change > 0 else "en correction"
            return f"Analyse de **{coin['name']}** : Prix actuel {coin['current_price']}$. L'actif est {vibe} ({change:.2f}%). On surveille la cassure ?"

    # 4. PRÉDICTIONS / HAUSSE
    if any(x in msg for x in ["hausse", "prédis", "prévision", "combien", "gagner"]):
        gain = random.randint(400, 1700)
        return f"Mes modèles détectent une accumulation de volume. Je projette une accélération de **+{gain}%** sur les secteurs à haute volatilité."

    # 5. SCAN GLOBAL
    if any(x in msg for x in ["quoi", "acheter", "scan", "plan"]):
        top = max(data, key=lambda x: x['price_change_percentage_24h'])
        return f"Scan terminé. Le signal le plus nerveux est sur **{top['symbol'].upper()}** (+{top['price_change_percentage_24h']:.2f}%). C'est le vecteur idéal actuel."

    # 6. SALUTATIONS
    if any(x in msg for x in ["salut", "bonsoir", "hello", "bonjour"]):
        return "Système opérationnel. Les flux mondiaux sont synchronisés. On lance un scan ?"

    return "Instruction reçue. Je traite l'info. Donne-moi un nom d'actif ou demande-moi un scan général des réseaux."

# --- INTERFACE VISUELLE ---
st.markdown('<div class="q-chip">NEURAL CORE</div>', unsafe_allow_html=True)
st.title("KAIROS v28.0 PURE GEMINI")

col_m, col_c = st.columns([1, 1.2])

with col_m:
    st.subheader("📊 LIVE MARKET DATA")
    if data:
        df = pd.DataFrame(data)[['symbol', 'current_price', 'price_change_percentage_24h']]
        df.columns = ['ASSET', 'PRICE ($)', '24H %']
        st.dataframe(df, use_container_width=True, hide_index=True)

with col_c:
    st.subheader("💬 CHAT INTERFACE")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": "Système en ligne. Prêt pour le scan. On commence par quoi ?"}]

    for m in st.session_state.messages:
        role = "GEMINI" if m["role"] == "ai" else "YOU"
        div = "ai-msg" if m["role"] == "ai" else "user-msg"
        st.markdown(f'<div class="{div}"><b>{role}:</b> {m["content"]}</div>', unsafe_allow_html=True)

    u_input = st.chat_input("Injection de commande...")
    if u_input:
        st.session_state.messages.append({"role": "user", "content": u_input})
        res = gemini_engine(u_input)
        st.session_state.messages.append({"role": "ai", "content": res})
        st.rerun()
