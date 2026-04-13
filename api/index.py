from http.server import BaseHTTPRequestHandler
import json
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        price = "0"
        try:
            url = "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT"
            # On ajoute un User-Agent pour que Binance accepte la requête
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                price = data.get('price', '0')
        except Exception as e:
            price = "API Busy"

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
