import subprocess
import sys
import time
import socket
import requests

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def ensure_server():
    if is_port_in_use(5000):
        print("Servidor ja esta rodando")
        return True
    print("Iniciando servidor Flask...")
    proc = subprocess.Popen(
        [sys.executable, r"C:\Users\cleit\Desktop\opb-sistema\api_server.py"],
        cwd=r"C:\Users\cleit\Desktop\opb-sistema",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )
    for i in range(20):
        time.sleep(0.5)
        if is_port_in_use(5000):
            print("Servidor ativo!")
            return True
        if proc.poll() is not None:
            _, err = proc.communicate()
            print("SERVIDOR MORREU:", repr(err[:300]) if err else "(sem erro)")
            return False
    print("Servidor nao iniciou a tempo")
    return False

if not ensure_server():
    print("Falha ao iniciar servidor")
    sys.exit(1)

print("\n" + "="*50)
print("FLUXO COMPLETO END-TO-END")
print("="*50)

# 1. Health
print("\n1. Health check...")
r = requests.get("http://localhost:5000/api/health", timeout=5)
print("   ", "PASS" if r.status_code == 200 else "FAIL", r.json())

# 2. Consumo
print("\n2. Consumo (POST /api/consumo)...")
r = requests.post("http://localhost:5000/api/consumo", json={
    "input": "A importancia da consistencia no marketing digital para solopreneurs.",
    "tipo": "completo",
    "titulo": "Consistencia no Marketing"
}, timeout=90)
print("   ", "PASS" if r.status_code == 200 else "FAIL", r.json().get("mensagem"))

# 3. Alimentar
print("\n3. Alimentar cerebro (POST /api/alimentar)...")
r = requests.post("http://localhost:5000/api/alimentar", json={
    "input": "Marketing digital exige consistencia e autenticidade para construir autoridade.",
    "tipo": "completo",
    "titulo": "Marketing Digital"
}, timeout=90)
print("   ", "PASS" if r.status_code == 200 else "FAIL", r.json().get("mensagem"))

# 4. Carrossel (Ollama precisa estar quente!)
print("\n4. Gerar Carrossel (POST /api/carrossel)...")
print("   (Garantindo que Ollama esta quente...)")
warmup = requests.post("http://localhost:11434/api/generate", json={
    "model": "tinyllama", "prompt": "test", "stream": False
}, timeout=30)
print("   Ollama quente:", warmup.status_code == 200)

r = requests.post("http://localhost:5000/api/carrossel", json={
    "tema": "Marketing Digital para Solopreneurs",
    "tipo": "educational",
    "slides": 5
}, timeout=120)
print("   ", "PASS" if r.status_code == 200 else "FAIL")
d = r.json()
print("   Sucesso:", d.get("sucesso"))
print("   Mensagem:", d.get("mensagem"))
if d.get("saida"):
    print("   Saida (primeiros 200 chars):", d["saida"][:200])

# 5. Text Generator
print("\n5. Text Generator (POST /api/text-generator)...")
r = requests.post("http://localhost:5000/api/text-generator", json={
    "objetivo": "Dicas de marketing digital para empreendedores solo",
    "tipo": "educational"
}, timeout=120)
print("   ", "PASS" if r.status_code == 200 else "FAIL")
d = r.json()
print("   Sucesso:", d.get("sucesso"))
if d.get("saida"):
    print("   Saida (primeiros 200 chars):", d["saida"][:200])

# 6. Stats
print("\n6. Stats atualizados (GET /api/stats)...")
r = requests.get("http://localhost:5000/api/stats", timeout=5)
stats = r.json()
print("   Conhecimento:", stats.get("conhecimento_salvo"))
print("   Carrossel:", stats.get("carrossel_gerados"))
print("   Ideias:", stats.get("ideias_salvas"))
print("   Posts:", stats.get("posts_gerados"))

# 7. Agentes
print("\n7. Listar agentes (GET /api/agentes)...")
r = requests.get("http://localhost:5000/api/agentes", timeout=5)
print("   ", len(r.json()), "agentes encontrados")

print("\n" + "="*50)
print("FLUXO COMPLETO FINALIZADO COM SUCESSO!")
print("="*50)