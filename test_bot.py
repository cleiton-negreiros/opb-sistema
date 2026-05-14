import requests
import json

BASE = "http://localhost:5000"

# Testa inicio do bot
r = requests.post(f"{BASE}/api/bot/start")
print("Bot start status:", r.status_code)
data = r.json()
print("Sucesso:", data.get("sucesso"))
print("Mensagem:", data.get("mensagem"))
print("Status:", data.get("status"))

print("\nConcluido!")