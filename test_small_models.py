#!/usr/bin/env python3
"""Test smaller Ollama models"""
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Try small models
small_models = ["gemma:2b", "phi3:mini", "llama3:8b", "tinyllama", "codellama:7b"]

for model in small_models:
    try:
        payload = json.dumps({"model": model, "prompt": "Diga uma dica de produtividade em 1 frase.", "stream": False}).encode()
        req = urllib.request.Request("http://localhost:11434/api/generate", data=payload, headers={"Content-Type": "application/json"}, method="POST")
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        text = result.get("response", "?")[:100]
        print("OK - " + model + ": " + text)
        break
    except Exception as e:
        print("FALHA - " + model + ": " + str(e)[:80])