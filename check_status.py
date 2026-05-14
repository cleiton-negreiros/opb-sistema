import subprocess
import sys
import time
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

print("Porta 5000 ativa?", is_port_in_use(5000))

# Procura processos python
result = subprocess.run(['tasklist', '/FI', 'imagename eq python.exe'], capture_output=True, text=True, encoding='utf-8', errors='replace')
print("Processos Python:")
for line in result.stdout.split('\n')[:15]:
    print(" ", line)

print("\nDone")