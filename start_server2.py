import subprocess
import sys
import time
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

# Mata processos python
subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], capture_output=True, text=True)
time.sleep(2)

print("Iniciando servidor Flask...")
proc = subprocess.Popen(
    [sys.executable, r"C:\Users\cleit\Desktop\opb-sistema\api_server.py"],
    cwd=r"C:\Users\cleit\Desktop\opb-sistema",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    encoding='utf-8',
    errors='replace'
)

# Espera até a porta estar disponível ou 15s
for i in range(15):
    time.sleep(1)
    if is_port_in_use(5000):
        print("Servidor rodando (PID:", proc.pid, ")")
        break
else:
    out, err = proc.communicate()
    print("SERVIDOR MORREU!")
    print("STDOUT:", repr(out[:500]))
    print("STDERR:", repr(err[:500] if err else "(vazio)"))