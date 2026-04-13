import streamlit as st
import pandas as pd
import requests
import random
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="KAIROS v30.0 OMNISCIENCE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main { background-color: #020204; color: #ffffff; }
    .ai-msg { background: rgba(0, 102, 255, 0.08); border-left: 3px solid #0066ff; padding: 15px; border-radius: 8px; margin-bottom: 12px; line-height: 1.5; }
    .user-msg { text-align: right; color: #00f2ff; font-weight: 800; margin-bottom: 12px; text-transform: uppercase; font-size: 10px; letter-spacing: 1px; }
    .q-chip { background: #0066ff; color: white; padding: 2px 8px; border-radius: 3px; font-size: 10px; font-weight: 900; margin-bottom: 5px; }
    .search-tag { color: #00f2ff; font-family: monospace; font-size: 11px; margin-bottom: 5px; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- FONCTION RECHERCHE WEB (MOTEUR) ---
def web_search(query):
    try:
        # Utilisation de l'API DuckDuckGo (Instant Answer)
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1"
        r = requests.get(url).json()
        
        abstract = r.get('AbstractText', "")
        if abstract:
            return f"🌐 **RÉSULTAT DE RECHERCHE** :\n\n{abstract}\n\n*Source: Intelligence Distribuée*"
        
        # Si pas de résumé, on cherche dans les résultats connexes
        related = r.get('RelatedTopics', [])
        if related and 'Text' in related[0]:
            return f"🌐 **INFOS TROUVÉES** :\n\n{related[0]['Text']}"
            
        return "Désolé, ma recherche web n'a pas retourné de résultat précis. Précise ta requête."
    except:
        return "Connexion au réseau de recherche interrompue."

# --- FONCTION ALPHA (SOLANA) ---
def get_solana_alpha():
    try:
        url = "https://api.dexscreener.com/latest/dex/search?q=solana"
        r = requests.get(url).json()
        pairs = r.get('pairs', [])
        if pairs:
            top = pairs[0]
            return f"🚨 **SIGNAL ALPHA** : **{top['baseToken']['name']}** ({top['baseToken']['symbol']})\n• Vol 24h: {float(top['volume']['h24']):,.0f}$\n• Liquidité: {float(top['liquidity']['usd']):,.0f}$"
    except: return "Erreur scan Solana."
    return "Rien sur Solana."

# --- DATA MARKET ---
@st.cache_data(ttl=60)
def get_market():
    try: return requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50").json()
    except: return []

market_data = get_market()

# --- MOTEUR GEMINI (LOGIQUE DE DÉCISION) ---
def gemini_engine(prompt):
    msg = prompt.lower().strip()
    
    # 1. SÉCURITÉ IDENTITÉ (Priorité Absolue)
    if any(x in msg for x in ["t'es qui", "qui es-tu", "ton nom", "c'est quoi kairos"]):
        return "Je suis **KAIROS**, ton interface Gemini-Core. Je combine un scanneur blockchain temps-réel et un moteur de recherche global."

    # 2. COMMANDE ALPHA
    if any(x in msg for x in ["alpha", "pépite", "solana"]):
        return get_solana_alpha()

    # 3. SCAN CRYPTO LOCAL
    for coin in market_data:
        if coin['symbol'].lower() == msg or coin['name'].lower() in msg:
            return f"📊 **{coin['name']}** : {coin['current_price']}$ ({coin['price_change_percentage_24h']:.2f}%)"

    # 4. MODE MOTEUR DE RECHERCHE (Si aucune commande crypto n'est détectée)
    if len(msg.split()) > 1: # Si la phrase contient plusieurs mots, on cherche sur le web
        return web_search(prompt)

    return "Instruction reçue. Tape **ALPHA** pour Solana, ou pose-moi une question sur n'importe quel sujet pour lancer une recherche web."

# --- UI ---
st.markdown('<div class="q-chip">SYSTEM: OMNISCIENCE</div>', unsafe_allow_html=True)
st.title("KAIROS v30.0")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📊 MARKET FLUX")
    if market_data:
        df = pd.DataFrame(market_data)[['symbol', 'current_price', 'price_change_percentage_24h']]
        st.dataframe(df, use_container_width=True, hide_index=True)

with col2:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": "KAIROS v30.0 en ligne. Moteur de recherche web et scanner Solana synchronisés."}]

    for m in st.session_state.messages:
        div = "ai-msg" if m["role"] == "ai" else "user-msg"
        st.markdown(f'<div class="{div}"><b>{"KAIROS" if m["role"]=="ai" else "YOU"}:</b> {m["content"]}</div>', unsafe_allow_html=True)

    u_input = st.chat_input("Rechercher sur le web ou scanner crypto...")
    if u_input:
        st.session_state.messages.append({"role": "user", "content": u_input})
        with st.spinner("Recherche en cours..."):
            response = gemini_engine(u_input)
        st.session_state.messages.append({"role": "ai", "content": response})
        st.rerun()
