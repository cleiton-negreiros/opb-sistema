import requests
import json

BASE = "http://localhost:5000"

print("Teste 1: Health check")
try:
    r = requests.get(f"{BASE}/api/health", timeout=5)
    print("  OK:", r.status_code == 200)
    print("  JSON:", r.json())
except Exception as e:
    print("  FALHA:", e)

print("\nTeste 2: Consumo")
try:
    r = requests.post(f"{BASE}/api/consumo", json={
        "input": "Teste de consistencia no marketing digital",
        "tipo": "completo",
        "titulo": "Teste Consumo"
    }, timeout=30)
    print("  OK:", r.status_code == 200)
    print("  JSON:", r.json())
except Exception as e:
    print("  FALHA:", e)

print("\nTeste 3: Alimentar")
try:
    r = requests.post(f"{BASE}/api/alimentar", json={
        "input": "Teste alimentar cerebro",
        "tipo": "completo",
        "titulo": "Teste Alimentar"
    }, timeout=30)
    print("  OK:", r.status_code == 200)
    print("  JSON:", r.json())
except Exception as e:
    print("  FALHA:", e)

print("\nTeste 4: Carrossel")
try:
    r = requests.post(f"{BASE}/api/carrossel", json={
        "tema": "Marketing Digital",
        "tipo": "educational",
        "slides": 3
    }, timeout=30)
    print("  Status:", r.status_code)
    print("  JSON:", r.json())
except Exception as e:
    print("  FALHA:", e)

print("\nConcluido!")