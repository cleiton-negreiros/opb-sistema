import requests
import json

BASE = "http://localhost:5000"

# Test 1: Health check
r = requests.get(f"{BASE}/api/health")
print("Health:", r.json())

# Test 2: Stats
r = requests.get(f"{BASE}/api/stats")
print("Stats:", r.json())

# Test 3: Consumo API
r = requests.post(f"{BASE}/api/consumo", json={
    "input": "Teste de alimentacao do cerebro via API",
    "tipo": "completo",
    "titulo": "Teste API"
})
print("Consumo:", r.json())

# Test 4: Agentes
r = requests.get(f"{BASE}/api/agentes")
print("Agentes:", json.dumps(r.json(), indent=2, ensure_ascii=False))

# Test 5: Cerebro arvore
r = requests.get(f"{BASE}/api/cerebro/arvore")
print("Arvore:", json.dumps(r.json()[:10], indent=2, ensure_ascii=False))

print("\nTodos os endpoints testados!")