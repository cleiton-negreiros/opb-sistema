import subprocess
import sys
import time
import socket
import os

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

# Mata qualquer python
subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], capture_output=True, text=True)
time.sleep(2)

# Inicia servidor (sem redirect para não bloquear)
proc = subprocess.Popen(
    [sys.executable, r"C:\Users\cleit\Desktop\opb-sistema\api_server.py"],
    cwd=r"C:\Users\cleit\Desktop\opb-sistema"
)

print("PID:", proc.pid)

# Espera
for i in range(20):
    time.sleep(0.5)
    if is_port_in_use(5000):
        print("Porta 5000 ativa!")
        break
    print(".", end="", flush=True)
else:
    print("\nPorta nao ficou ativa")

print("\nVerificando...")
import requests
try:
    r = requests.get("http://localhost:5000/api/health", timeout=5)
    print("API responde:", r.json())
except Exception as e:
    print("Erro:", e)

print("\nFim verificacao")