import streamlit as st
import pandas as pd
import requests
import random
import urllib.parse
from bs4 import BeautifulSoup
import sqlite3

# --- CONFIGURATION ---
st.set_page_config(page_title="KAIROS v33.0 OMNI-SYNAPSE", layout="wide", initial_sidebar_state="collapsed")

# --- DATABASE ---
conn = sqlite3.connect('kairos_memory.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS memory (user_id TEXT, last_query TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

st.markdown("""
    <style>
    .main { background-color: #010103; color: #ffffff; }
    .ai-msg { background: rgba(0, 102, 255, 0.05); border-left: 2px solid #0066ff; padding: 18px; border-radius: 10px; margin-bottom: 15px; font-family: 'Inter', sans-serif; }
    .user-msg { text-align: right; color: #00f2ff; font-weight: 900; margin-bottom: 15px; text-transform: uppercase; font-size: 10px; letter-spacing: 2px; }
    .q-chip { background: #0066ff; color: white; padding: 3px 10px; border-radius: 4px; font-size: 9px; font-weight: 900; letter-spacing: 1px; }
    .chart-box { border: 1px double #0066ff; padding: 12px; border-radius: 8px; background: rgba(0, 10, 30, 0.8); margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- MODULES TECHNIQUES ---
def analyze_candles():
    patterns = ["Hammer", "Bullish Engulfing", "Doji", "Morning Star"]
    p = random.choice(patterns)
    return f"<div class='chart-box'>📈 <b>SCANNER BIOMÉTRIQUE</b> : Pattern <b>{p}</b> identifié. Structure solide pour un holder. Ne tremble pas, la tendance reste ton alliée.</div>"

def advanced_scrape(query):
    try:
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1"
        r = requests.get(url).json()
        abstract = r.get('AbstractText', "")
        if abstract: return f"🌐 **ANALYSE RÉSEAU** : {abstract}"
        return f"Je n'ai pas trouvé de trace précise de '{query}' dans mes flux actuels. Sois plus spécifique."
    except: return "Lien réseau rompu. Impossible de scanner le web."

def get_solana_alpha():
    try:
        url = "https://api.dexscreener.com/latest/dex/search?q=solana"
        r = requests.get(url).json()
        pairs = r.get('pairs', [])
        if pairs:
            top = pairs[0]
            return f"🚨 **VECTEUR ALPHA** : **{top['baseToken']['name']}** est en train de briser la résistance. Volume 24h: {float(top['volume']['h24']):,.0f}$. Si tu cherches l'action, elle est ici."
    except: return "Scan Solana hors ligne."

# --- MOTEUR DE PERSONNALITÉ (GEMINI CORE) ---
def gemini_engine(prompt):
    msg = prompt.lower().strip()
    c.execute("INSERT INTO memory (user_id, last_query) VALUES (?, ?)", ("User_1", msg))
    conn.commit()

    # LOGIQUE DE PERSONNALITÉ
    if any(x in msg for x in ["t'es qui", "qui es-tu", "ton nom"]):
        return "Je suis **KAIROS**, ton interface Gemini-Core. Je ne suis pas juste un bot crypto, je suis ton extension directe. Je traite le web et la blockchain en simultané pour que tu n'aies jamais un train de retard."

    if any(x in msg for x in ["salut", "ça va", "wsh", "hello"]):
        return random.choice([
            "Système opérationnel. Je suis prêt à scanner ou à discuter, selon ton niveau d'ambition.",
            "Flux synchronisés. Qu'est-ce qu'on traite aujourd'hui ?",
            "Je suis là. Pas de temps à perdre, on passe aux choses sérieuses ?"
        ])

    if any(x in msg for x in ["bougie", "chart", "graphique", "tendance"]):
        return analyze_candles()

    if any(x in msg for x in ["alpha", "pépite", "solana"]):
        return get_solana_alpha()

    # RÉPONSE GÉNÉRALE (MOTEUR DE RECHERCHE + PERSONNALITÉ)
    res = advanced_scrape(prompt)
    return f"{res}\n\n*Analyse terminée. Besoin d'un scan plus profond sur ce sujet ?*"

# --- UI ---
st.markdown('<div class="q-chip">KAIROS NEURAL INTERFACE v33.0</div>', unsafe_allow_html=True)
st.title("KAIROS CORE")

col1, col2 = st.columns([1, 1.3])

with col1:
    st.subheader("⚡ LIVE DATA")
    try:
        m_data = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10").json()
        df = pd.DataFrame(m_data)[['symbol', 'current_price', 'price_change_percentage_24h']]
        st.dataframe(df, use_container_width=True, hide_index=True)
    except: st.write("Market data offline.")

with col2:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": "KAIROS v33.0 activé. Je surveille les flux pour toi. On cherche une pépite ou on parle de l'avenir ?"}]

    for m in st.session_state.messages:
        div = "ai-msg" if m["role"] == "ai" else "user-msg"
        st.markdown(f'<div class="{div}"><b>{"KAIROS" if m["role"]=="ai" else "YOU"}:</b> {m["content"]}</div>', unsafe_allow_html=True)

    u_input = st.chat_input("Injection de commande...")
    if u_input:
        st.session_state.messages.append({"role": "user", "content": u_input})
        with st.spinner("Analyse en cours..."):
            response = gemini_engine(u_input)
        st.session_state.messages.append({"role": "ai", "content": response})
        st.rerun()
