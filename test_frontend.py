import requests

BASE = "http://localhost:5000"

# Testa pagina principal
r = requests.get(f"{BASE}/")
print("Status:", r.status_code)
print("Content-Type:", r.headers.get('Content-Type'))
print("Tamanho:", len(r.content))
print("Inicio HTML:", r.text[:200])

# Testa se plataforma carrega
if 'plataforma' in r.text.lower() or 'dashboard' in r.text.lower():
    print("\n✅ Plataforma HTML carregada com sucesso!")
else:
    print("\n⚠️ Plataforma pode ter conteudo diferente")

print("\nConcluido!")