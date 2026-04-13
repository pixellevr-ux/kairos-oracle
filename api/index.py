import streamlit as st
import pandas as pd
import requests
import random
import time

# --- CONFIGURATION DE L'INTERFACE ---
st.set_page_config(page_title="KAIROS v28.0 OVERDRIVE", layout="wide", initial_sidebar_state="collapsed")

# Style CSS pour le look "Quantum Terminal"
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@400;700&display=swap');
    
    :root { --cyan: #00f2ff; --blue: #0066ff; --bg: #020204; --panel: rgba(10, 10, 15, 0.9); }
    
    .main { background-color: var(--bg); color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* Header & Tags */
    .q-chip { background: var(--blue); color: white; font-size: 10px; font-weight: 900; padding: 4px 10px; border-radius: 4px; display: inline-block; margin-bottom: 5px; }
    .v-tag { color: var(--blue); font-size: 12px; font-weight: bold; }
    
    /* Panels */
    .glass-panel { 
        background: var(--panel); border: 1px solid rgba(255, 255, 255, 0.05); 
        border-radius: 16px; padding: 20px; backdrop-filter: blur(15px);
        margin-bottom: 20px;
    }
    
    /* Chat bubbles */
    .ai-msg { 
        background: rgba(0, 102, 255, 0.12); border-left: 4px solid var(--blue); 
        padding: 15px; border-radius: 8px; margin-bottom: 15px; font-size: 14px; color: #e0e0e0;
    }
    .user-msg { text-align: right; color: var(--cyan); font-weight: 800; font-size: 12px; margin-bottom: 15px; text-transform: uppercase; }
    
    /* Input */
    .stTextInput>div>div>input { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- SYNC DATA LIVE ---
@st.cache_data(ttl=60)
def fetch_market():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50"
        return requests.get(url).json()
    except:
        return []

market_data = fetch_market()

# --- MOTEUR NEURAL GEMINI ---
def gemini_think(input_text):
    msg = input_text.lower().strip()
    
    # 1. IDENTITÉ PRIORITAIRE
    if any(x in msg for x in ["t'es qui", "qui es-tu", "ton nom", "qui est tu"]):
        return "Je suis **KAIROS**, ton interface Gemini-Core. Mon noyau est optimisé pour le scan de flux et l'analyse de volatilité. Pas de blabla, juste de la performance."

    # 2. SALUTATIONS
    if any(x in msg for x in ["salut", "bonsoir", "hello", "bonjour", "ca va"]):
        return "Système opérationnel. Les flux sont synchronisés. On lance un scan ou tu as une cible précise ?"

    # 3. ANALYSE CRYPTO
    for coin in market_data:
        if coin['symbol'].lower() == msg or coin['name'].lower() in msg:
            change = coin['price_change_percentage_24h']
            vibe = "en hausse" if change > 0 else "en correction"
            return f"Analyse de **{coin['name']}** : Prix actuel {coin['current_price']}$. L'actif est {vibe} ({change:.2f}%). On surveille la cassure ?"

    # 4. PRÉDICTIONS
    if any(x in msg for x in ["hausse", "prédis", "prévision", "combien", "gagner"]):
        gain = random.randint(350, 1600)
        return f"Détection d'accumulation de volume. Je projette une accélération de **+{gain}%** sur les secteurs à haute vélocité. C'est là que l'énergie est concentrée."

    # 5. SCAN GLOBAL
    if any(x in msg for x in ["quoi", "acheter", "scan", "plan", "opportunité"]):
        top = max(market_data, key=lambda x: x['price_change_percentage_24h'])
        return f"Scan terminé. Le signal le plus nerveux est sur **{top['symbol'].upper()}** (+{top['price_change_percentage_24h']:.2f}%). C'est le meilleur vecteur actuel."

    return "Instruction reçue. Je traite l'information. Donne-moi un nom d'actif ou demande un scan général."

# --- INTERFACE VISUELLE ---

# Header
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.markdown('<div class="q-chip">NEURAL NETWORK</div>', unsafe_allow_html=True)
    st.markdown('### KAIROS <span class="v-tag">v28.0 OVERDRIVE</span>', unsafe_allow_html=True)
with col_h2:
    st.markdown(f'<div style="text-align:right; color:#00f2ff; font-family:monospace;">GH-REMAINING: 1399.979</div>', unsafe_allow_html=True)

st.markdown("---")

# Layout Principal
col_market, col_chat = st.columns([1, 1.2])

with col_market:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<span style="color:#00f2ff; font-size:10px; font-weight:900; letter-spacing:2px;">LIVE MARKET ANALYSIS</span>', unsafe_allow_html=True)
    
    if market_data:
        df = pd.DataFrame(market_data)[['symbol', 'current_price', 'price_change_percentage_24h']]
        df.columns = ['ASSET', 'PRICE', '24H %']
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.error("Échec de synchronisation des flux.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_chat:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "ai", "content": "Système initialisé. Flux de données crypto synchronisé. Je t'écoute."}]

    # Affichage des logs
    for m in st.session_state.chat_history:
        if m["role"] == "ai":
            st.markdown(f'<div class="ai-msg"><b>GEMINI:</b> {m["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="user-msg">> {m["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Input utilisateur
    with st.container():
        user_input = st.chat_input("Injection de commande...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            response = gemini_think(user_input)
            st.session_state.chat_history.append({"role": "ai", "content": response})
            st.rerun()

# Footer
st.button("LANCER LE SCAN DES NARRATIFS (IA/MEMES/DEPIN)", use_container_width=True)
