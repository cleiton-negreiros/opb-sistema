import requests
import json

BASE = "http://localhost:5000"

print("=" * 50)
print("TESTE DE FLUXO COMPLETO v2")
print("=" * 50)

# Passo 1: Alimentar cerebro
print("\n1. Alimentando o cerebro...")
r = requests.post(f"{BASE}/api/alimentar", json={
    "input": "Teste de alimentacao do cerebro",
    "tipo": "completo",
    "titulo": "Teste Alimentar"
})
print("  Status:", r.status_code)
print("  Resultado:", r.json().get("mensagem"))

# Passo 2: Consumo
print("\n2. Processando conteudo via consumo...")
r = requests.post(f"{BASE}/api/consumo", json={
    "input": "A importancia da consistencia no marketing digital",
    "tipo": "completo",
    "titulo": "Consistencia no Marketing"
})
print("  Status:", r.status_code)
print("  Resultado:", r.json().get("mensagem"))

# Passo 3: Carrossel
print("\n3. Gerando carrossel...")
r = requests.post(f"{BASE}/api/carrossel", json={
    "tema": "Marketing Digital",
    "tipo": "educational",
    "slides": 3
})
print("  Status:", r.status_code)
if r.status_code == 200:
    d = r.json()
    print("  Sucesso:", d.get("sucesso"))
    print("  Mensagem:", d.get("mensagem"))
else:
    print("  Erro:", r.text[:300])

# Passo 4: Stats
print("\n4. Stats atualizados...")
r = requests.get(f"{BASE}/api/stats")
stats = r.json()
print("  Conhecimento:", stats.get("conhecimento_salvo"))
print("  Carrossel:", stats.get("carrossel_gerados"))
print("  Ideias:", stats.get("ideias_salvas"))

print("\n" + "=" * 50)
print("FLUXO COMPLETO FINALIZADO!")
print("=" * 50)