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

# Inicia servidor via cmd.exe para ver output
cmd = f'start "OPB Server" cmd /c "cd /d C:\\Users\\cleit\\Desktop\\opb-sistema && python api_server.py"'
os.system(cmd)

# Espera porta
print("Esperando servidor iniciar...")
for i in range(30):
    time.sleep(0.5)
    if is_port_in_use(5000):
        print("Servidor ativo na porta 5000!")
        break
    print(".", end="", flush=True)
else:
    print("\nFALHA: servidor nao iniciou")

print("\nVerificando API...")
import requests
try:
    r = requests.get("http://localhost:5000/api/health", timeout=5)
    print("API:", r.json())
except Exception as e:
    print("Erro:", e)