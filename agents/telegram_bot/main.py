import os
import json
import logging
from datetime import datetime
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8789174206:AAG8Ns8KJTi2cnGGRkuEYea7OGTj6pp4qW0"

ACERVO_PATH = Path(__file__).parent.parent.parent / "acervo" / "ideias"

def ensure_acervo():
    ACERVO_PATH.mkdir(parents=True, exist_ok=True)
    index_path = ACERVO_PATH / "index.md"
    if not index_path.exists():
        index_path.write_text("""# Ideias Cadastradas

> Lista de ideias capturadas via Telegram Bot

## Como usar

- Envie uma ideia pelo Telegram
- O bot salva automaticamente no cérebro
- Formato: `ideia: sua ideia aqui` ou apenas a ideia

## Lista

- _Nenhuma ideia ainda_

---
*Última atualização: AAAA-MM-DD HH:MM*
""", encoding="utf-8")

def save_ideia(texto: str, usuario: str = "telegram") -> str:
    ensure_acervo()
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}.md"
    filepath = ACERVO_PATH / filename
    
    conteudo = f"""---
name: "Ideia {timestamp}"
description: "{texto[:50]}..."
tipo: ideia
tags: []
updated_at: {datetime.now().strftime("%Y-%m-%d")}
autor: {usuario}
---

# {texto}

**Data:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Autor:** {usuario}

---

*Salvo via Telegram Bot*
"""
    filepath.write_text(conteudo, encoding="utf-8")
    logger.info(f"Ideia salva: {filename}")
    return filename

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 *NegreirosBot*\n\n"
        "Olá! Sou seu bot de captura de ideias.\n\n"
        "Como usar:\n"
        "• Envie uma ideia diretamente\n"
        "• Use /ideia [sua ideia]\n"
        "• Use /listar para ver ideias\n\n"
        "As ideias são salvas no cérebro automaticamente!",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 *Comandos disponíveis:*\n\n"
        "/start - Iniciar o bot\n"
        "/help - Ver comandos\n"
        "/ideia [texto] - Cadastrar ideia\n"
        "/listar - Ver últimas ideias\n"
        "/status - Ver status do sistema",
        parse_mode="Markdown"
    )

async def ideia_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        texto = " ".join(context.args)
        filename = save_ideia(texto, update.effective_user.name)
        await update.message.reply_text(f"✅ Ideia cadastrada!\n\n`{texto[:100]}...`", parse_mode="Markdown")
    else:
        await update.message.reply_text("用法: /ideia [sua ideia aqui]")

async def listar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ensure_acervo()
    ideias = sorted(ACERVO_PATH.glob("*.md"), reverse=True)[:5]
    
    if ideias:
        msg = "📝 *Últimas ideias:*\n\n"
        for f in ideias:
            lines = f.read_text(encoding="utf-8").split("\n")
            titulo = lines[7] if len(lines) > 7 else f.name
            msg += f"• {titulo[:60]}...\n"
    else:
        msg = "Nenhuma ideia ainda. Envie uma!"
    
    await update.message.reply_text(msg, parse_mode="Markdown")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ensure_acervo()
    total = len(list(ACERVO_PATH.glob("*.md")))
    await update.message.reply_text(
        f"📊 *Status do NegreirosBot*\n\n"
        f"• Ideias cadastradas: {total}\n"
        f"• Cérebro: ✅ conectado\n"
        f"• Pasta: `{ACERVO_PATH}`",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    
    if texto.startswith("/"):
        return
    
    if len(texto) > 5:
        filename = save_ideia(texto, update.effective_user.name)
        await update.message.reply_text(f"💡 Ideia salva!\n\n`{texto[:80]}...`", parse_mode="Markdown")
    else:
        await update.message.reply_text("Ideia muito curta. Envie mais detalhes!")

def main():
    ensure_acervo()
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ideia", ideia_command))
    app.add_handler(CommandHandler("listar", listar_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 NegreirosBot iniciado!")
    print(f"📁 Salvando ideias em: {ACERVO_PATH}")
    
    app.run_polling(poll_interval=3)

if __name__ == "__main__":
    main()