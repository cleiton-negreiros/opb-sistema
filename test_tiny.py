import requests

# Testa tinyllama
print("Testando tinyllama...")
try:
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "tinyllama",
        "prompt": "Write one sentence about marketing.",
        "stream": False
    }, timeout=60)
    print("Status:", r.status_code)
    if r.status_code == 200:
        data = r.json()
        print("Response:", data.get("response", "")[:200])
    else:
        print("Error:", r.text[:300])
except Exception as e:
    print("Error:", type(e).__name__, e)