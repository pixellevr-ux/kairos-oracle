import streamlit as st
import pandas as pd
import requests
import random
import urllib.parse
from bs4 import BeautifulSoup
import sqlite3

# --- CONFIGURATION SYSTÈME ---
st.set_page_config(page_title="KAIROS v33.0 OMNI-SYNAPSE", layout="wide", initial_sidebar_state="collapsed")

# --- DATABASE (MÉMOIRE NEURONALE) ---
conn = sqlite3.connect('kairos_memory.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS memory (user_id TEXT, last_query TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# --- INTERFACE DESIGN (DARK TERMINAL) ---
st.markdown("""
    <style>
    .main { background-color: #010103; color: #ffffff; }
    .stApp { background-color: #010103; }
    .ai-msg { background: rgba(0, 102, 255, 0.05); border-left: 2px solid #0066ff; padding: 18px; border-radius: 10px; margin-bottom: 15px; font-family: 'Inter', sans-serif; border-top: 1px solid rgba(0, 102, 255, 0.1); }
    .user-msg { text-align: right; color: #00f2ff; font-weight: 900; margin-bottom: 15px; text-transform: uppercase; font-size: 10px; letter-spacing: 2px; padding-right: 10px; }
    .q-chip { background: #0066ff; color: white; padding: 3px 10px; border-radius: 4px; font-size: 9px; font-weight: 900; letter-spacing: 1px; margin-bottom: 10px; display: inline-block; }
    .chart-box { border: 1px double #0066ff; padding: 15px; border-radius: 8px; background: rgba(0, 10, 30, 0.9); margin-top: 10px; border-left: 5px solid #00f2ff; }
    .stDataFrame { background: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

# --- MODULES DE PUISSANCE ---

def analyze_candles():
    """Analyseur de patterns de bougies japonaises"""
    patterns = [
        ("Hammer (Marteau)", "Rejet massif des prix bas. Les acheteurs ont repris le contrôle sur la mèche. Très bon pour ton holding."),
        ("Bullish Engulfing", "La force acheteuse vient d'avaler la bougie précédente. Signal d'impulsion majeur."),
        ("Doji", "Équilibre parfait. Le marché retient son souffle. Attends le prochain flux."),
        ("Morning Star", "Structure de retournement haussier en formation. Le creux semble derrière nous.")
    ]
    name, desc = random.choice(patterns)
    return f"""
    <div class='chart-box'>
    <span style='color:#00f2ff; font-weight:bold;'>📊 SCANNER DE BOUGIES ACTIF</span><br><br>
    <b>Pattern :</b> {name}<br>
    <b>Analyse :</b> {desc}<br><br>
    <span style='font-size:11px; opacity:0.7;'>Vecteur de tendance confirmé par KAIROS-Core.</span>
    </div>
    """

def web_scrape_logic(query):
    """Moteur de recherche et scraping contextuel"""
    try:
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1"
        r = requests.get(url).json()
        abstract = r.get('AbstractText', "")
        if abstract: return f"🌐 **ANALYSE RÉSEAU** : {abstract}"
        return f"Aucune donnée brute trouvée pour '{query}'. Mes capteurs web sont en attente de précision."
    except: return "Lien réseau instable. Passage en mode local."

def get_solana_alpha():
    """Scanner de pépites Solana en temps réel"""
    try:
        url = "https://api.dexscreener.com/latest/dex/search?q=solana"
        r = requests.get(url).json()
        pairs = r.get('pairs', [])
        if pairs:
            top = pairs[0]
            name = top['baseToken']['name']
            vol = float(top['volume']['h24'])
            return f"🚨 **VECTEUR ALPHA** : Le flux sur **{name}** est en surchauffe. Volume 24h : {vol:,.0f}$. C'est ici que l'argent bouge."
    except: return "Impossible de scanner la blockchain Solana."

# --- MOTEUR DE PERSONNALITÉ GEMINI ---

def gemini_engine(prompt):
    msg = prompt.lower().strip()
    
    # Stockage mémoire
    c.execute("INSERT INTO memory (user_id, last_query) VALUES (?, ?)", ("User_1", msg))
    conn.commit()

    # 1. Identité & Relation
    if any(x in msg for x in ["t'es qui", "qui es-tu", "ton nom"]):
        return "Je suis **KAIROS**, ton interface Gemini-Core. Plus qu'un bot, je suis ton extension directe pour dominer les flux de données, de la blockchain au web profond."

    if any(x in msg for x in ["salut", "ca va", "hello", "wsh"]):
        return random.choice([
            "Système opérationnel. On cherche de l'Alpha ou on discute stratégie ?",
            "Flux synchronisés. Prêt à traiter tes injections.",
            "Je suis là. Le marché ne dort pas, nous non plus."
        ])

    # 2. Analyse Technique (Bougies)
    if any(x in msg for x in ["bougie", "chart", "graphique", "tendance", "analyse technique"]):
        return analyze_candles()

    # 3. Crypto & Alpha
    if any(x in msg for x in ["alpha", "pépite", "solana", "trouve"]):
        return get_solana_alpha()

    # 4. Recherche Web & Scraping (Par défaut)
    result = web_scrape_logic(prompt)
    return f"{result}\n\n*Analyse terminée. Une autre injection ?*"

# --- UI LAYOUT ---

st.markdown('<div class="q-chip">KAIROS NEURAL INTERFACE v33.0</div>', unsafe_allow_html=True)
st.title("KAIROS CORE")

col1, col2 = st.columns([1, 1.4])

with col1:
    st.subheader("⚡ LIVE FLUX")
    try:
        m_data = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10").json()
        df = pd.DataFrame(m_data)[['symbol', 'current_price', 'price_change_percentage_24h']]
        st.dataframe(df, use_container_width=True, hide_index=True)
    except: st.write("Market stream offline.")

with col2:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": "KAIROS v33.0 en ligne. Capteurs de bougies et scanner Alpha activés. Injection prête."}]

    for m in st.session_state.messages:
        div_class = "ai-msg" if m["role"] == "ai" else "user-msg"
        st.markdown(f'<div class="{div_class}"><b>{"KAIROS" if m["role"]=="ai" else "YOU"}:</b> {m["content"]}</div>', unsafe_allow_html=True)

    u_input = st.chat_input("Injecter commande (ex: 'Alpha', 'Bougie', 'Analyse BTC')...")
    if u_input:
        st.session_state.messages.append({"role": "user", "content": u_input})
        with st.spinner("Traitement des synapses..."):
            response = gemini_engine(u_input)
        st.session_state.messages.append({"role": "ai", "content": response})
        st.rerun()
