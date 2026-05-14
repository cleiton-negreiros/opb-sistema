import requests

# Testa Ollama diretamente
print("Testando Ollama com llama3:latest...")
try:
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3:latest",
        "prompt": "Write one sentence about marketing.",
        "stream": False
    }, timeout=30)
    print("Status:", r.status_code)
    if r.status_code == 200:
        data = r.json()
        print("Response:", data.get("response", "")[:200])
    else:
        print("Error:", r.text[:200])
except Exception as e:
    print("Ollama error:", type(e).__name__, e)