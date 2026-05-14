import requests
import json

BASE = "http://localhost:5000"

# Testa alimentar com input simples e sem caracteres especiais
print("Testando alimentar com input simples...")
r = requests.post(f"{BASE}/api/alimentar", json={
    "input": "Teste simples de alimentacao",
    "tipo": "completo",
    "titulo": "Teste Simples"
})
print("Status:", r.status_code)
print("Text:", r.text[:300])

print("\nTestando carrossel...")
r = requests.post(f"{BASE}/api/carrossel", json={
    "tema": "Teste de Carrossel",
    "tipo": "educational",
    "slides": 3
})
print("Status:", r.status_code)
print("Text:", r.text[:500])