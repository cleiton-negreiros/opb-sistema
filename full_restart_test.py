import subprocess
import sys
import time
import requests

# Mata tudo
print("Matando processos...")
subprocess.run(['taskkill', '/F', '/IM', 'ollama.exe'], capture_output=True, text=True)
subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], capture_output=True, text=True)
time.sleep(3)

# Inicia Ollama
print("Iniciando Ollama...")
ollama_proc = subprocess.Popen(['ollama', 'serve'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(5)

# Verifica modelos
try:
    r = requests.get("http://localhost:11434/api/tags", timeout=5)
    print("Ollama OK, modelos:", [m['name'] for m in r.json().get('models', [])])
except Exception as e:
    print("Ollama falhou:", e)
    sys.exit(1)

# Testa tinyllama
print("\nTestando tinyllama (cold start)...")
try:
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "tinyllama",
        "prompt": "What is marketing?",
        "stream": False
    }, timeout=120)
    print("Response:", r.json().get("response", "")[:100])
    print("tinyllama OK!")
except Exception as e:
    print("tinyllama error:", e)

# Inicia servidor Flask
print("\nIniciando servidor Flask...")
server_proc = subprocess.Popen(
    [sys.executable, r"C:\Users\cleit\Desktop\opb-sistema\api_server.py"],
    cwd=r"C:\Users\cleit\Desktop\opb-sistema"
)
time.sleep(5)

# Testa carrossel
print("\nTestando carrossel (precisa de Ollama quente)...")
try:
    r = requests.post("http://localhost:5000/api/carrossel", json={
        "tema": "Marketing Digital",
        "tipo": "educational",
        "slides": 3
    }, timeout=180)
    print("Status:", r.status_code)
    d = r.json()
    print("Sucesso:", d.get("sucesso"))
    print("Mensagem:", d.get("mensagem"))
    if d.get("saida"):
        print("Saida:", d["saida"][:300])
except Exception as e:
    print("Carrossel error:", type(e).__name__, e)

print("\nDone!")