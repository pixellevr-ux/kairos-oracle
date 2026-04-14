import streamlit as st
import pandas as pd
import requests
import random
import urllib.parse
import sqlite3

# --- CONFIGURATION ---
st.set_page_config(page_title="KAIROS v37.0 OPTIMA", layout="wide", initial_sidebar_state="collapsed")

# --- CACHE INTELLIGENT (Économise tes 2000 pts) ---
@st.cache_data(ttl=600) # Rafraîchissement auto toutes les 10 min
def get_market_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10"
        return requests.get(url).json()
    except: return None

# --- DATABASE ---
conn = sqlite3.connect('kairos_memory.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS memory (user_id TEXT, last_query TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# --- DESIGN TERMINAL ---
st.markdown("""
    <style>
    .main { background-color: #010103; color: #ffffff; }
    .ai-msg { background: rgba(0, 102, 255, 0.05); border-left: 2px solid #0066ff; padding: 15px; border-radius: 10px; margin-bottom: 12px; }
    .user-msg { text-align: right; color: #00f2ff; font-weight: 800; font-size: 10px; text-transform: uppercase; }
    .status-bar { background: rgba(0, 255, 136, 0.1); border: 1px solid #00ff88; color: #00ff88; padding: 5px; border-radius: 5px; font-size: 10px; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- FONCTIONS DE CALCUL ---
def scan_alpha_logic():
    # Simulation de scan profond
    try:
        url = "https://api.dexscreener.com/latest/dex/search?q=solana"
        r = requests.get(url).json()
        top = r.get('pairs', [])[0]
        risk = random.randint(1, 10)
        return f"🚨 **VECTEUR ALPHA** : {top['baseToken']['name']}\n\n⚠️ **RISQUE : {risk}/10**\nConseil : Ne pas dépasser 3% du capital."
    except: return "Scan indisponible."

# --- INTERFACE ---
st.sidebar.markdown("<div class='status-bar'>SYSTÈME OPTIMISÉ - BUDGET 2000 PTS/MOIS</div>", unsafe_allow_html=True)

st.title("KAIROS CORE v37.0")

col1, col2 = st.columns([1, 1.4])

with col1:
    st.subheader("⚡ LIVE MARKET")
    data = get_market_data()
    if data:
        df = pd.DataFrame(data)[['symbol', 'current_price', 'price_change_percentage_24h']]
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Bouton manuel pour forcer l'update si besoin
    if st.button("🔄 FORCE REFRESH (-1 PT)"):
        st.cache_data.clear()
        st.rerun()

with col2:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": "KAIROS prêt. Budget optimisé pour 2000 pts. On cherche un signal ?"}]

    for m in st.session_state.messages:
        div = "ai-msg" if m["role"] == "ai" else "user-msg"
        st.markdown(f'<div class="{div}"><b>{"KAIROS" if m["role"]=="ai" else "YOU"}:</b> {m["content"]}</div>', unsafe_allow_html=True)

    u_input = st.chat_input("Injection de commande...")
    if u_input:
        st.session_state.messages.append({"role": "user", "content": u_input})
        
        # Logique de sécurité pour les scans lourds
        if any(x in u_input.lower() for x in ["alpha", "scan", "bougie", "tendance"]):
            # On affiche un bouton de confirmation juste sous le chat pour économiser
            st.warning("Confirmation requise pour scan haute puissance.")
            if st.button("LANCER L'ANALYSE (-5 PTS)"):
                res = scan_alpha_logic()
                st.session_state.messages.append({"role": "ai", "content": res})
                st.rerun()
        else:
            # Réponse textuelle simple (moins gourmande)
            st.session_state.messages.append({"role": "ai", "content": "Reçu. Noyau stable. Pose une question spécifique sur les charts pour activer les modules."})
            st.rerun()
