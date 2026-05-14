import requests
import json

BASE = "http://localhost:5000"

print("Teste 1: Health check")
r = requests.get(f"{BASE}/api/health", timeout=5)
print("  OK:", r.status_code == 200)

print("\nTeste 2: Stats")
r = requests.get(f"{BASE}/api/stats", timeout=5)
print("  OK:", r.status_code == 200)

print("\nTeste 3: Consumo (rapido)")
r = requests.post(f"{BASE}/api/consumo", json={
    "input": "Teste rapido",
    "tipo": "completo",
    "titulo": "Teste"
}, timeout=30)
print("  OK:", r.status_code == 200)
print("  JSON:", r.json())

print("\nTeste 4: Alimentar (rapido)")
r = requests.post(f"{BASE}/api/alimentar", json={
    "input": "Teste",
    "tipo": "completo",
    "titulo": "Teste"
}, timeout=30)
print("  OK:", r.status_code == 200)
print("  JSON:", r.json())

print("\nTodos os testes basicos passaram!")