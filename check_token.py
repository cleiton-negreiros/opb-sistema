#!/usr/bin/env python3
"""Check Telegram Bot token"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
if token:
    print("[OK] TELEGRAM_BOT_TOKEN esta configurado:", token[:20] + "..." if len(token) > 20 else token)
else:
    print("[AVISO] TELEGRAM_BOT_TOKEN nao esta definido!")
    print("Para configurar:")
    print("  Windows: setx TELEGRAM_BOT_TOKEN 'seu_token_aqui'")
    print("  Linux/Mac: export TELEGRAM_BOT_TOKEN='seu_token_aqui'")
    print("")
    print("Obtenha seu token no @BotFather do Telegram")