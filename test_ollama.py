import subprocess
import sys
import time
import requests

# Test Ollama directly
print("Testando Ollama API...")
try:
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "tinyllama",
        "prompt": "Write one sentence about marketing.",
        "stream": False
    }, timeout=30)
    print("Ollama response:", r.json()[:200] if r.status_code == 200 else r.status_code)
except Exception as e:
    print("Ollama error:", e)

print("\nTestando carrossel direto da linha de comando...")
import os
os.chdir(r"C:\Users\cleit\Desktop\opb-sistema")
result = subprocess.run(
    [sys.executable, "agents/carrossel/main.py", "Teste", "educational", "3"],
    capture_output=True,
    text=True,
    timeout=30,
    cwd=r"C:\Users\cleit\Desktop\opb-sistema"
)
print("STDOUT:", result.stdout[:500])
print("STDERR:", result.stderr[:500] if result.stderr else "(vazio)")
print("Return code:", result.returncode)