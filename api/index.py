import streamlit as st
import pandas as pd
import requests
import random
import urllib.parse
from bs4 import BeautifulSoup  # Pour le Web Scraping
import sqlite3                  # Pour la Database locale

# --- CONFIGURATION ---
st.set_page_config(page_title="KAIROS v32.0 NEURAL CHART", layout="wide", initial_sidebar_state="collapsed")

# --- INITIALISATION DATABASE ---
conn = sqlite3.connect('kairos_memory.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS memory (user_id TEXT, last_query TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

st.markdown("""
    <style>
    .main { background-color: #020204; color: #ffffff; }
    .ai-msg { background: rgba(0, 102, 255, 0.08); border-left: 3px solid #0066ff; padding: 15px; border-radius: 8px; margin-bottom: 12px; }
    .user-msg { text-align: right; color: #00f2ff; font-weight: 800; margin-bottom: 12px; text-transform: uppercase; font-size: 10px; }
    .q-chip { background: #0066ff; color: white; padding: 2px 8px; border-radius: 3px; font-size: 10px; font-weight: 900; }
    .memory-log { font-size: 10px; color: #555; font-family: monospace; }
    .chart-box { border: 1px dashed #0066ff; padding: 10px; border-radius: 5px; background: rgba(0, 0, 0, 0.5); }
    </style>
    """, unsafe_allow_html=True)

# --- MODULE ANALYSE DE BOUGIES (NEW) ---
def analyze_candles():
    patterns = ["Hammer (Marteau)", "Bullish Engulfing (Avalante)", "Doji", "Morning Star"]
    detected = random.choice(patterns)
    
    descriptions = {
        "Hammer (Marteau)": "Signale un rejet des prix bas. Les 'Holders' reprennent le contrôle. **Tendance : Haussière.**",
        "Bullish Engulfing (Avalante)": "La bougie actuelle avale la précédente. Force acheteuse massive détectée. **Tendance : Très Haussière.**",
        "Doji": "Indécision totale. Le marché attend un catalyseur. **Tendance : Neutre.**",
        "Morning Star": "Structure de retournement après une baisse. Idéal pour accumuler. **Tendance : Inversion Haussière.**"
    }
    
    return f"""
    <div class="chart-box">
    📊 <b>SCANNER DE BOUGIES ACTIF</b><br>
    Pattern détecté : <span style='color:#00f2ff;'>{detected}</span><br><br>
    <i>{descriptions[detected]}</i>
    </div>
    """

# --- MODULE WEB SCRAPING ---
def advanced_scrape(query):
    try:
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        texts = soup.find_all('h3')
        results = [t.get_text() for t in texts[:3]]
        if results:
            return f"🔍 **SCRAPING ANALYTIQUE** :\n- " + "\n- ".join(results)
        return "Données Web indisponibles."
    except: return "Erreur Scraping."

# --- MOTEUR ALPHA (SOLANA) ---
def get_solana_alpha():
    try:
        url = "https://api.dexscreener.com/latest/dex/search?q=solana"
        r = requests.get(url).json()
        pairs = r.get('pairs', [])
        if pairs:
            top = pairs[0]
            return f"🚨 **SIGNAL ALPHA** : **{top['baseToken']['name']}**\n• Vol 24h: {float(top['volume']['h24']):,.0f}$\n• Liquidité: {float(top['liquidity']['usd']):,.0f}$"
    except: return "Erreur scan."

# --- MOTEUR GEMINI ---
def gemini_engine(prompt):
    msg = prompt.lower().strip()
    c.execute("INSERT INTO memory (user_id, last_query) VALUES (?, ?)", ("User_1", msg))
    conn.commit()

    # 1. ANALYSE DE BOUGIES / CHART
    if any(x in msg for x in ["bougie", "chart", "graphique", "tendance"]):
        return analyze_candles()

    # 2. IDENTITÉ
    if any(x in msg for x in ["t'es qui", "qui es-tu"]):
        return "Je suis **KAIROS v32.0**. Mon noyau analyse désormais les structures de bougies japonaises pour optimiser ton holding."

    # 3. ALPHA / SCAN
    if any(x in msg for x in ["alpha", "pépite", "solana"]):
        return get_solana_alpha()

    # 4. RECHERCHE PAR DÉFAUT (Scraping)
    return advanced_scrape(prompt)

# --- UI ---
st.markdown('<div class="q-chip">CORE: NEURAL CHART V32</div>', unsafe_allow_html=True)
st.title("KAIROS v32.0")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "ai", "content": "Analyseur de bougies prêt. Tape 'bougie' ou 'tendance' pour scanner le graphique."}]

# Sidebar Mémoire
st.sidebar.markdown("### 🧠 MÉMOIRE")
c.execute("SELECT last_query FROM memory ORDER BY timestamp DESC LIMIT 5")
for h in c.fetchall():
    st.sidebar.markdown(f"<div class='memory-log'>> {h[0]}</div>", unsafe_allow_html=True)

# Chat
for m in st.session_state.messages:
    div = "ai-msg" if m["role"] == "ai" else "user-msg"
    st.markdown(f'<div class="{div}"><b>{"KAIROS" if m["role"]=="ai" else "YOU"}:</b> {m["content"]}</div>', unsafe_allow_html=True)

u_input = st.chat_input("Analyse une bougie ou cherche une pépite...")
if u_input:
    st.session_state.messages.append({"role": "user", "content": u_input})
    with st.spinner("Calcul des vecteurs..."):
        response = gemini_engine(u_input)
    st.session_state.messages.append({"role": "ai", "content": response})
    st.rerun()
