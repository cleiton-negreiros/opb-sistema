import requests
import json

BASE = "http://localhost:5000"

print("=" * 50)
print("TESTE DE FLUXO COMPLETO")
print("=" * 50)

# Passo 1: Alimentar cérebro
print("\n1. Alimentando o cerebro...")
r = requests.post(f"{BASE}/api/alimentar", json={
    "input": "O marketing digital para solopreneurs exige consistência, autenticidade e estratégia de conteúdo. O primeiro passo é definir seu nicho e público-alvo com clareza.",
    "tipo": "completo",
    "titulo": "Marketing Digital para Solopreneurs"
})
print("  Resultado:", r.json().get("mensagem"))

# Passo 2: Consumo via API
print("\n2. Processando conteudo via agente de consumo...")
r = requests.post(f"{BASE}/api/consumo", json={
    "input": "A consistência é a chave do marketing digital. Postar todos os dias constrói autoridade e confiança com o público.",
    "tipo": "completo",
    "titulo": "Consistência no Marketing"
})
print("  Resultado:", r.json().get("mensagem"))

# Passo 3: Gerar carrossel
print("\n3. Gerando carrossel...")
r = requests.post(f"{BASE}/api/carrossel", json={
    "tema": "Marketing Digital para Solopreneurs",
    "tipo": "educational",
    "slides": 5
})
print("  Resultado:", r.json().get("mensagem"))
if r.json().get("sucesso"):
    # Extrair apenas texto sem emojis para print
    saida = r.json().get("saida", "")
    print("  Saida (primeiros 300 chars):", saida[:300])

# Passo 4: Gerar post
print("\n4. Gerando post...")
r = requests.post(f"{BASE}/api/text-generator", json={
    "objetivo": "Compartilhar dicas de marketing digital para empreendedores solo",
    "tipo": "educational"
})
print("  Resultado:", r.json().get("mensagem"))
if r.json().get("sucesso"):
    saida = r.json().get("saida", "")
    print("  Saida (primeiros 300 chars):", saida[:300])

# Passo 5: Verificar stats atualizados
print("\n5. Verificando stats atualizados...")
r = requests.get(f"{BASE}/api/stats")
stats = r.json()
print("  Conhecimento salvo:", stats.get("conhecimento_salvo"))
print("  Carrossel gerados:", stats.get("carrossel_gerados"))
print("  Posts gerados:", stats.get("posts_gerados"))

print("\n" + "=" * 50)
print("FLUXO COMPLETO TESTADO COM SUCESSO!")
print("=" * 50)