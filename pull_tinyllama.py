#!/usr/bin/env python3
"""Pull a small model and test"""
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Pull tinyllama
print("Puxando tinyllama (pode demorar)...")
try:
    payload = json.dumps({"name": "tinyllama"}).encode()
    req = urllib.request.Request("http://localhost:11434/api/pull", data=payload, headers={"Content-Type": "application/json"}, method="POST")
    resp = urllib.request.urlopen(req, timeout=300)
    # Read streaming response
    for line in resp:
        data = json.loads(line.decode())
        status = data.get("status", "")
        if status:
            print(status[:80], end="\r")
    print("\nDownload concluído!")
except Exception as e:
    print("Erro ao baixar:", e)

# Test generation with tinyllama
print("\nTestando geração com tinyllama...")
try:
    payload = json.dumps({"model": "tinyllama", "prompt": "Give me a one sentence productivity tip.", "stream": False}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=payload, headers={"Content-Type": "application/json"}, method="POST")
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read())
    print("Resultado:", result.get("response", "?")[:200])
except Exception as e:
    print("Erro:", e)