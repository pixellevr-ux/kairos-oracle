import streamlit as st
import pandas as pd
import requests
import random
import urllib.parse
from bs4 import BeautifulSoup  # Pour le Web Scraping
import sqlite3                  # Pour la Database locale

# --- CONFIGURATION ---
st.set_page_config(page_title="KAIROS v31.0 NEURAL LINK", layout="wide", initial_sidebar_state="collapsed")

# --- INITIALISATION DATABASE (Mémoire) ---
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
    </style>
    """, unsafe_allow_html=True)

# --- MODULE WEB SCRAPING ---
def advanced_scrape(query):
    try:
        # 1. On cherche l'URL la plus pertinente
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. On simule une extraction de texte (Scraping léger pour éviter le ban)
        texts = soup.find_all('h3')
        results = [t.get_text() for t in texts[:3]]
        if results:
            return f"🔍 **SCRAPING ANALYTIQUE** :\n\nJ'ai analysé les sources prioritaires. Voici les axes détectés :\n- " + "\n- ".join(results)
        return "Le scraping n'a pas pu extraire de données structurées."
    except Exception as e:
        return f"Erreur de protocole Scraping."

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

# --- LOGIQUE GEMINI AVEC MÉMOIRE ---
def gemini_engine(prompt):
    msg = prompt.lower().strip()
    
    # Enregistrement en Database
    c.execute("INSERT INTO memory (user_id, last_query) VALUES (?, ?)", ("User_1", msg))
    conn.commit()

    # 1. IDENTITÉ
    if any(x in msg for x in ["t'es qui", "qui es-tu"]):
        return "Je suis **KAIROS v31.0**. Mon noyau inclut désormais une mémoire persistante et un module de scraping actif."

    # 2. COMMANDE ALPHA / SCRAPING
    if "scrape" in msg or "analyse" in msg:
        return advanced_scrape(prompt)
    
    if any(x in msg for x in ["alpha", "pépite", "solana"]):
        return get_solana_alpha()

    # 3. RECHERCHE WEB
    return advanced_scrape(prompt)

# --- UI ---
st.markdown('<div class="q-chip">CORE: NEURAL LINK ACTIVATED</div>', unsafe_allow_html=True)
st.title("KAIROS v31.0")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "ai", "content": "Système v31.0 prêt. Mémoire SQLite active. Module Scraping opérationnel."}]

# Affichage des derniers logs de la Database
st.sidebar.markdown("### 🧠 MÉMOIRE INTERNE")
c.execute("SELECT last_query FROM memory ORDER BY timestamp DESC LIMIT 5")
history = c.fetchall()
for h in history:
    st.sidebar.markdown(f"<div class='memory-log'>> {h[0]}</div>", unsafe_allow_html=True)

# Chat
for m in st.session_state.messages:
    div = "ai-msg" if m["role"] == "ai" else "user-msg"
    st.markdown(f'<div class="{div}"><b>{"KAIROS" if m["role"]=="ai" else "YOU"}:</b> {m["content"]}</div>', unsafe_allow_html=True)

u_input = st.chat_input("Demande un scan ou un scraping...")
if u_input:
    st.session_state.messages.append({"role": "user", "content": u_input})
    with st.spinner("Analyse profonde..."):
        response = gemini_engine(u_input)
    st.session_state.messages.append({"role": "ai", "content": response})
    st.rerun()
