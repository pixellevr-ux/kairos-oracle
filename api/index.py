from http.server import BaseHTTPRequestHandler
import json
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        price = "0"
        try:
            # On utilise urllib au lieu de requests (plus stable sur Vercel Free)
            url = "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                price = data.get('price', '0')
        except Exception as e:
            price = "Erreur Connection"

        payload = {
            "token": "SOL/USDT",
            "price": price,
            "status": "ONLINE",
            "message": "KAIROS Alpha Live"
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode('utf-8'))
        return
