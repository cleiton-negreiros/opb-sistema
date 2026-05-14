import subprocess
import sys
import time
import socket
import requests

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

print("Iniciando servidor Flask (sem matar processos)...")
proc = subprocess.Popen(
    [sys.executable, r"C:\Users\cleit\Desktop\opb-sistema\api_server.py"],
    cwd=r"C:\Users\cleit\Desktop\opb-sistema",
    stdout=subprocess.DEVNULL,
    stderr=subprocess.PIPE
)

print("Esperando porta 5000...")
started = False
for i in range(30):
    time.sleep(0.5)
    if is_port_in_use(5000):
        started = True
        break
    if proc.poll() is not None:
        _, err = proc.communicate()
        print("SERVIDOR MORREU:", repr(err[:500]) if err else "sem erro")
        break

if started:
    print("Servidor ativo!")
    # Testa endpoints
    r = requests.get("http://localhost:5000/api/health", timeout=5)
    print("Health:", r.json())

    r = requests.post("http://localhost:5000/api/consumo", json={
        "input": "Teste de marketing digital",
        "tipo": "completo",
        "titulo": "Teste"
    }, timeout=60)
    d = r.json()
    print("Consumo:", d.get("mensagem"))

    r = requests.post("http://localhost:5000/api/alimentar", json={
        "input": "Teste de alimentacao do cerebro",
        "tipo": "completo",
        "titulo": "Teste Alimentar"
    }, timeout=90)
    d = r.json()
    print("Alimentar:", d.get("mensagem"))

    r = requests.post("http://localhost:5000/api/carrossel", json={
        "tema": "Teste Marketing",
        "tipo": "educational",
        "slides": 3
    }, timeout=60)
    d = r.json()
    print("Carrossel:", d.get("mensagem"), "sucesso:", d.get("sucesso"))

    r = requests.get("http://localhost:5000/api/stats", timeout=5)
    print("Stats:", r.json())

    print("\n=== TODOS OS TESTES CONCLUIDOS ===")
else:
    print("FALHA: servidor nao iniciou")
    _, err = proc.communicate()
    print("STDERR:", repr(err[:1000]) if err else "(vazio)")