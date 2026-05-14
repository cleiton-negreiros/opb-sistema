#!/usr/bin/env python3
"""Setup script for OPB Sistema"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

print("=" * 50)
print("SETUP OPB SISTEMA")
print("=" * 50)
print("")

# 1. Telegram Token
print("[1/4] Token do Telegram")
token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
if token and len(token) > 20:
    print("  Token ja configurado:", token[:20] + "...")
else:
    print("  Token NAO configurado!")
    print("")
    print("  Para configurar, execute:")
    print("    setx TELEGRAM_BOT_TOKEN 'SEU_TOKEN_AQUI'")
    print("")
    print("  O token pode ser obtido com @BotFather no Telegram.")
    print("  Enviar /newbot e seguir as instrucoes.")

print("")

# 2. Ollama Model
print("[2/4] Modelo Ollama")
import urllib.request
import json

try:
    resp = urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5)
    data = json.loads(resp.read())
    models = [m.get("name", "?") for m in data.get("models", [])]
    print("  Modelos instalados:", ", ".join(models) if models else "Nenhum")

    if "tinyllama" not in models and "llama3" in models:
        print("  llama3 encontrado, mas pode ser pesado demais (4.6GB RAM)")
        print("  Recomendado: ollama pull tinyllama")
    elif "tinyllama" in models:
        print("  tinyllama disponivel - pronto para usar!")
    else:
        print("  Para instalar modelo leve: ollama pull tinyllama")
except Exception as e:
    print("  Ollama nao acessivel:", e)
    print("  Rode: ollama serve")

print("")

# 3. Check Python dependencies
print("[3/4] Dependencias Python")
deps = ["flask", "flask-cors", "requests", "beautifulsoup4"]
for dep in deps:
    try:
        __import__(dep.replace("-", "_"))
        print(f"  {dep}: OK")
    except ImportError:
        print(f"  {dep}: FALTA - pip install {dep}")

print("")

# 4. Project structure
print("[4/4] Estrutura do projeto")
from pathlib import Path
base = Path("C:/Users/cleit/Desktop/opb-sistema")
checks = {
    "api_server.py": "Servidor API",
    "agents/telegram_bot/main.py": "Bot Telegram",
    "agents/consumo/main.py": "Agente de Consumo",
    "agents/carrossel/main.py": "Agente Carrossel",
    "cerebro/perfil-empreendedor-solo/plataforma.html": "Plataforma Web",
    "context-brain/business-core.json": "Contexto (business-core)",
    "negocio/governanca/quem-sou.md": "Identidade (quem-sou.md)",
}

for path, name in checks.items():
    full = base / path
    if full.exists():
        print(f"  {name}: OK")
    else:
        print(f"  {name}: FALTA ({path})")

print("")
print("=" * 50)
print("Setup concluido!")
print("=" * 50)