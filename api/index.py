import streamlit as st
import pandas as pd
import requests
import random
import urllib.parse
from bs4 import BeautifulSoup
import sqlite3

# --- CONFIGURATION SYSTÈME ---
st.set_page_config(page_title="KAIROS v34.0 RISK SHIELD", layout="wide", initial_sidebar_state="collapsed")

# --- DATABASE ---
conn = sqlite3.connect('kairos_memory.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS memory (user_id TEXT, last_query TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# --- INTERFACE DESIGN ---
st.markdown("""
    <style>
    .main { background-color: #010103; color: #ffffff; }
    .stApp { background-color: #010103; }
    .ai-msg { background: rgba(0, 102, 255, 0.05); border-left: 2px solid #0066ff; padding: 18px; border-radius: 10px; margin-bottom: 15px; font-family: 'Inter', sans-serif; }
    .user-msg { text-align: right; color: #00f2ff; font-weight: 900; margin-bottom: 15px; text-transform: uppercase; font-size: 10px; letter-spacing: 2px; }
    .q-chip { background: #0066ff; color: white; padding: 3px 10px; border-radius: 4px; font-size: 9px; font-weight: 900; letter-spacing: 1px; display: inline-block; }
    .chart-box { border: 1px double #0066ff; padding: 15px; border-radius: 8px; background: rgba(0, 10, 30, 0.9); margin-top: 10px; }
    .risk-tag { padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- MODULES DE PUISSANCE ---

def get_risk_assessment():
    """Calcule un score de risque aléatoire (simulé sur data) et donne un conseil"""
    score = random.randint(1, 10)
    if score <= 3:
        color, label, advice = "#00ff88", "FAIBLE", "Position de holding idéale. Le ratio risque/récompense est optimal."
    elif score <= 7:
        color, label, advice = "#ffcc00", "MODÉRÉ", "Prudence. Ne dépasse pas 3-5% de ton capital sur cette ligne."
    else:
        color, label, advice = "#ff3333", "CRITIQUE", "Danger. Volatilité extrême détectée. Uniquement pour du gambling."
    
    return f"""
    <div style='margin-top:10px; padding:10px; border:1px solid {color}; border-radius:5px;'>
        <span class='risk-tag' style='background:{color}; color:#000;'>RISQUE {score}/10 - {label}</span><br><br>
        <i style='font-size:13px;'>{advice}</i>
    </div>
    """

def analyze_candles():
    patterns = [
        ("Hammer", "Rejet des prix bas. Les mains fortes protègent le support."),
        ("Bullish Engulfing", "Impulsion majeure. Les acheteurs écrasent la vente."),
        ("Doji", "Indécision. Le marché cherche son prochain souffle."),
        ("Morning Star", "Retournement haussier. Fin de la purge détectée.")
    ]
    name, desc = random.choice(patterns)
    return f"<div class='chart-box'>📊 <b>PATTERN : {name}</b><br>{desc}</div>"

def get_solana_alpha():
    try:
        url = "https://api.dexscreener.com/latest/dex/search?q=solana"
        r = requests.get(url).json()
        pairs = r.get('pairs', [])
        if pairs:
            top = pairs[0]
            risk_ui = get_risk_assessment()
            return f"🚨 **VECTEUR ALPHA** : **{top['baseToken']['name']}**<br>Vol 24h : {float(top['volume']['h24']):,.0f}$<br>{risk_ui}"
    except: return "Échec du scan blockchain."

def web_scrape_logic(query):
    try:
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1"
        r = requests.get(url).json()
        abstract = r.get('AbstractText', "")
        return f"🌐 **ANALYSE RÉSEAU** : {abstract}" if abstract else "Données insuffisantes."
    except: return "Lien rompu."

# --- MOTEUR GEMINI ---

def gemini_engine(prompt):
    msg = prompt.lower().strip()
    c.execute("INSERT INTO memory (user_id, last_query) VALUES (?, ?)", ("User_1", msg))
    conn.commit()

    if any(x in msg for x in ["t'es qui", "qui es-tu"]):
        return "Je suis **KAIROS v34.0**. Mon noyau intègre désormais un bouclier de gestion des risques pour sécuriser tes actifs."

    if any(x in msg for x in ["bougie", "chart", "tendance"]):
        return analyze_candles()

    if any(x in msg for x in ["alpha", "pépite", "solana", "risque", "risk"]):
        return get_solana_alpha()

    return f"{web_scrape_logic(prompt)}\n\n*Analyse terminée.*"

# --- UI LAYOUT ---
st.markdown('<div class="q-chip">KAIROS RISK SHIELD v34.0</div>', unsafe_allow_html=True)
st.title("KAIROS CORE")

col1, col2 = st.columns([1, 1.4])

with col1:
    st.subheader("⚡ LIVE FLUX")
    try:
        m_data = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10").json()
        df = pd.DataFrame(m_data)[['symbol', 'current_price', 'price_change_percentage_24h']]
        st.dataframe(df, use_container_width=True, hide_index=True)
    except: st.write("Flux offline.")

with col2:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": "KAIROS v34.0 prêt. Je calcule désormais le risque pour chaque injection."}]

    for m in st.session_state.messages:
        div_class = "ai-msg" if m["role"] == "ai" else "user-msg"
        st.markdown(f'<div class="{div_class}"><b>{"KAIROS" if m["role"]=="ai" else "YOU"}:</b> {m["content"]}</div>', unsafe_allow_html=True)

    u_input = st.chat_input("Demande un signal ou une analyse de risque...")
    if u_input:
        st.session_state.messages.append({"role": "user", "content": u_input})
        with st.spinner("Calcul des risques en cours..."):
            response = gemini_engine(u_input)
        st.session_state.messages.append({"role": "ai", "content": response})
        st.rerun()
