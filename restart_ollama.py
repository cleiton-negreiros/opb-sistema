import subprocess
import time
import sys

# Mata Ollama
subprocess.run(['taskkill', '/F', '/IM', 'ollama.exe'], capture_output=True, text=True)
time.sleep(3)

# Inicia Ollama explicitamente
proc = subprocess.Popen(
    ['ollama', 'serve'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    encoding='utf-8',
    errors='replace'
)
print(f"Ollama iniciado (PID: {proc.pid})")

# Espera ficar pronto
import socket
import requests
for i in range(20):
    time.sleep(1)
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        print("Ollama pronto!")
        print("Modelos:", r.json())
        break
    except:
        print(".", end="", flush=True)
else:
    print("\nOllama nao respondeu")
    out, err = proc.communicate()
    print("STDOUT:", out[:300])
    print("STDERR:", err[:300] if err else "(vazio)")