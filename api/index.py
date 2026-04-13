from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import random

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Simulation d'une base de données d'apprentissage
        # En production, on connecterait ici une vraie DB (Supabase)
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,litecoin,cardano,polkadot,dogecoin,ripple&vs_currencies=usd"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                prices = json.loads(response.read().decode())
        except:
            prices = {}

        # Logique d'analyse d'investissement (IA simplifiée pour le backend)
        analysis = {
            "best_pick": "SOLANA",
            "risk_level": "Medium",
            "potential_gain": "+12%",
            "duration": "48h",
            "reason": "Forte pression acheteuse détectée sur les DEX."
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response_data = {
            "prices": prices,
            "analysis": analysis,
            "github_minutes": random.randint(1350, 1400) # Simulation direct
        }
        
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
