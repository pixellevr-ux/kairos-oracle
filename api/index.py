from http.server import BaseHTTPRequestHandler
import json
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # On va chercher le prix actuel via Binance
        res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT").json()
        
        # Données envoyées au site
        payload = {
            "token": "SOL/USDT",
            "price": res['price'],
            "action": "ANALYSE EN COURS",
            "kairos_note": "KAIROS est en ligne. Prêt pour le prochain move."
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') # IMPORTANT pour Framer
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode('utf-8'))
        return
