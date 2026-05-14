#!/usr/bin/env python3
"""Check if Ollama is available"""
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    resp = urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5)
    data = json.loads(resp.read())
    models = [m.get("name", "?") for m in data.get("models", [])]
    print("[OK] Ollama esta rodando!")
    print("Modelos disponiveis:", ", ".join(models) if models else "Nenhum modelo instalado")
    if models:
        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=json.dumps({"model": models[0], "prompt": "Olá", "stream": False}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read())
        print("Resposta teste:", result.get("response", "?")[:100])
    else:
        print("[AVISO] Instale um modelo: ollama pull llama3")
except Exception as e:
    print("[FALHA] Ollama nao esta acessivel:", e)
    print("Instale e rode: ollama serve")
    print("Depois: ollama pull llama3")