from http.server import BaseHTTPRequestHandler
import json
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # On passe sur CoinGecko (plus stable pour les serveurs cloud)
            url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                # On récupère le prix de Solana en USD
                price = f"{data['solana']['usd']}$"
        except Exception:
            price = "Pricing Live..."

        payload = {
            "token": "SOLANA",
            "price": price,
            "status": "OPERATIONAL",
            "message": "KAIROS Alpha Live"
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode('utf-8'))
        return
