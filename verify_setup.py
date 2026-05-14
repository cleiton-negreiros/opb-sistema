import requests
import json

# Verifica se o bot conseguiu conectar
TOKEN = "8789174206:AAEFbU9kz0PQQLFlCw4vMVzIYiXSnmVRjxQ"

try:
    r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe", timeout=10)
    data = r.json()
    if data.get("ok"):
        result = data.get("result", {})
        print(f"Bot conectado: {result.get('first_name')} (@{result.get('username', 'N/A')})")
        print(f"Bot ID: {result.get('id')}")
    else:
        print("Bot NAO conectado:", data.get("description"))
except Exception as e:
    print(f"Erro ao conectar: {e}")

# Verifica webhook
try:
    r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo", timeout=10)
    print("Webhook:", r.json())
except Exception as e:
    print(f"Erro webhook: {e}")

# Testa API local
r = requests.get("http://localhost:5000/api/health")
print("API Local:", r.json())

print("\nConcluido!")