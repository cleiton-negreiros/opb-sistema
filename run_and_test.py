import subprocess
import sys
import time
import socket
import os

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

# Mata qualquer python que esteja rodando relacionado
subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], capture_output=True, text=True)
time.sleep(3)

if is_port_in_use(5000):
    print("ERRO: porta 5000 ainda em uso!")
    sys.exit(1)

# Inicia servidor
proc = subprocess.Popen(
    [sys.executable, r"C:\Users\cleit\Desktop\opb-sistema\api_server.py"],
    cwd=r"C:\Users\cleit\Desktop\opb-sistema",
    stdout=open(os.devnull, 'w'),
    stderr=subprocess.PIPE,
    encoding='utf-8',
    errors='replace'
)

# Espera porta ficar disponível
for i in range(20):
    time.sleep(0.5)
    if is_port_in_use(5000):
        print("Servidor iniciado com sucesso (PID:", proc.pid, ")")
        break
else:
    print("ERRO: Servidor nao iniciou a tempo")
    _, err = proc.communicate()
    print("STDERR:", repr(err[:500]) if err else "(vazio)")
    sys.exit(1)

# Agora testa
import requests

print("\n--- Testes ---")

# Health
r = requests.get("http://localhost:5000/api/health", timeout=5)
print("Health:", "PASS" if r.status_code == 200 else "FAIL")

# Consumo
r = requests.post("http://localhost:5000/api/consumo", json={
    "input": "Teste de alimentacao",
    "tipo": "completo",
    "titulo": "Teste"
}, timeout=60)
print("Consumo:", "PASS" if r.status_code == 200 else "FAIL", r.json().get("mensagem"))

# Alimentar
r = requests.post("http://localhost:5000/api/alimentar", json={
    "input": "Teste de alimentacao do cerebro",
    "tipo": "completo",
    "titulo": "Teste Alimentar"
}, timeout=60)
print("Alimentar:", "PASS" if r.status_code == 200 else "FAIL", r.json().get("mensagem"))

# Carrossel
r = requests.post("http://localhost:5000/api/carrossel", json={
    "tema": "Teste",
    "tipo": "educational",
    "slides": 3
}, timeout=60)
print("Carrossel:", "PASS" if r.status_code == 200 else "FAIL")
if r.status_code == 200:
    d = r.json()
    print("  sucesso:", d.get("sucesso"))

# Stats
r = requests.get("http://localhost:5000/api/stats", timeout=5)
print("Stats:", "PASS" if r.status_code == 200 else "FAIL")
if r.status_code == 200:
    print("  Dados:", r.json())

print("\n--- Fim dos testes ---")