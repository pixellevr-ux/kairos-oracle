import requests
import json
import random
import os

class KairosOracle:
    def __init__(self):
        self.name = "KAIROS"
        self.memory_path = 'brain_data.json'
        self.load_memory()

    def load_memory(self):
        try:
            with open(self.memory_path, 'r') as f:
                self.memory = json.load(f)
        except:
            self.memory = {
                "win_rate": 0.85,
                "total_swaps": 0,
                "learned_lessons": ["Initialisation du système KAIROS."]
            }

    def get_alpha_signal(self):
        # Scan réel de Binance (Prix actuel)
        url = "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT"
        res = requests.get(url).json()
        
        # Simulation du calcul "Deep Learning"
        signal = {
            "token": "SOL/USDT",
            "price": res['price'],
            "action": "HOLD" if float(res['price']) < 150 else "SWAP TO STABLE",
            "confidence": f"{self.memory['win_rate'] * 100}%",
            "kairos_note": "Le moment opportun est proche, reste vigilant."
        }
        return signal

if __name__ == "__main__":
    kairos = KairosOracle()
    print(json.dumps(kairos.get_alpha_signal()))
