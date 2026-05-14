import subprocess
import sys
import time
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if is_port_in_use(5000):
    print("Porta 5000 em uso - servidor esta rodando")
else:
    print("Porta 5000 livre - servidor nao esta rodando")

# Tenta health check
import requests
try:
    r = requests.get("http://localhost:5000/api/health", timeout=5)
    print("API respondendo:", r.json())
except Exception as e:
    print("Erro:", e)

# Testa alimentar
try:
    r = requests.post("http://localhost:5000/api/alimentar", json={
        "input": "Teste",
        "tipo": "completo",
        "titulo": "Teste"
    }, timeout=30)
    print("Alimentar:", r.status_code, r.json())
except Exception as e:
    print("Erro alimentar:", e)

# Testa consumo
try:
    r = requests.post("http://localhost:5000/api/consumo", json={
        "input": "Teste",
        "tipo": "completo",
        "titulo": "Teste"
    }, timeout=30)
    print("Consumo:", r.status_code, r.json())
except Exception as e:
    print("Erro consumo:", e)

print("\nFeito!")