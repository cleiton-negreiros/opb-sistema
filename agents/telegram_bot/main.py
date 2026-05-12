import os
import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8789174206:AAG8Ns8KJTi2cnGGRkuEYea7OGTj6pp4qW0")

PROJECT_PATH = Path(__file__).parent.parent.parent
ACERVO_PATH = PROJECT_PATH / "acervo" / "ideias"

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

def execute_command(cmd: str) -> str:
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        output = result.stdout if result.returncode == 0 else f"Erro: {result.stderr}"
        return output[:1500] if output else "Comando executado (sem output)"
    except Exception as e:
        return f"Erro: {str(e)[:200]}"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 *NegreirosBot*\n\n"
        "Olá! Sou seu bot de captura de ideias e execução remota.\n\n"
        "📝 *Captura de ideias:*\n"
        "• Envie uma ideia diretamente\n"
        "• Use /ideia [sua ideia]\n\n"
        "💻 *Comandos do sistema:*\n"
        "• /listar - Ver últimas ideias\n"
        "• /status - Status do sistema\n"
        "• /agents - Ver agentes disponíveis\n"
        "• /hub - Abrir hub de produtividade\n"
        "• /executar [comando] - Executar comando\n\n"
        "⚠️ *Executar comando roda no dispositivo onde o bot está rodando!*",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 *Todos os comandos:*\n\n"
        "*Ideias:*\n"
        "/ideia [texto] - Cadastrar ideia\n"
        "/listar - Ver últimas ideias\n\n"
        "*Sistema:*\n"
        "/status - Ver status\n"
        "/agents - Listar agentes\n"
        "/hub - Ver hub\n"
        "/executar [cmd] - Executar comando\n"
        "/projetos - Ver projetos ativos\n"
        "/regras - Ver regras do cérebro",
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
    
    agents_path = PROJECT_PATH / "agents"
    agentes = [d.name for d in agents_path.iterdir() if d.is_dir() and (d / "main.py").exists()]
    
    await update.message.reply_text(
        f"📊 *Status do NegreirosBot*\n\n"
        f"• Ideias cadastradas: {total}\n"
        f"• Agentes disponíveis: {len(agentes)}\n"
        f"• Pasta do projeto: `{PROJECT_PATH}`\n"
        f"• Modo: {'Termux' if 'com.termux' in str(PROJECT_PATH) else 'PC'}",
        parse_mode="Markdown"
    )

async def agents_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    agents_path = PROJECT_PATH / "agents"
    agentes = [d.name for d in agents_path.iterdir() if d.is_dir()]
    
    msg = "🤖 *Agentes disponíveis:*\n\n"
    for ag in agentes:
        soul_path = agents_path / ag / "SOUL.md"
        if soul_path.exists():
            linhas = soul_path.read_text(encoding="utf-8").split("\n")
            nome = linhas[3].replace("**Nome**: ", "") if len(linhas) > 3 else ag
        else:
            nome = ag
        msg += f"• `{ag}` - {nome}\n"
    
    await update.message.reply_text(msg, parse_mode="Markdown")

async def hub_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 *Hub de Produtividade*\n\n"
        "O hub contém:\n"
        "• 🍅 Pomodoro Timer\n"
        "• 📋 Planner Diário\n"
        "• 💰 Finanças\n"
        "• 💡 Ideias\n\n"
        f"URL: https://opb-sistema.vercel.app/hub.html",
        parse_mode="Markdown"
    )

async def executar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        cmd = " ".join(context.args)
        await update.message.reply_text(f"⏳ Executando: `{cmd}`...", parse_mode="Markdown")
        
        result = execute_command(cmd)
        
        if len(result) > 3000:
            result = result[:3000] + "\n\n... (truncado)"
        
        await update.message.reply_text(f"📤 *Resultado:*\n\n```\n{result}\n```", parse_mode="Markdown")
    else:
        await update.message.reply_text("用法: /executar [comando]\n\nExemplo: /executar ls -la")

async def projetos_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    projetos_path = PROJECT_PATH / "negocio" / "projetos" / "ativos.md"
    if projetos_path.exists():
        conteudo = projetos_path.read_text(encoding="utf-8")
        await update.message.reply_text(f"📋 *Projetos Ativos:*\n\n{conteudo[:2000]}", parse_mode="Markdown")
    else:
        await update.message.reply_text("Nenhum projeto encontrado.")

async def regras_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    regras_path = PROJECT_PATH / "negocio" / "governanca" / "regras" / "quem-sou.md"
    if regras_path.exists():
        conteudo = regras_path.read_text(encoding="utf-8")
        await update.message.reply_text(f"📜 *Quem Sou:*\n\n{conteudo[:2000]}", parse_mode="Markdown")
    else:
        await update.message.reply_text("Arquivo de regras não encontrado.")

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
    app.add_handler(CommandHandler("agents", agents_command))
    app.add_handler(CommandHandler("hub", hub_command))
    app.add_handler(CommandHandler("executar", executar_command))
    app.add_handler(CommandHandler("projetos", projetos_command))
    app.add_handler(CommandHandler("regras", regras_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 NegreirosBot iniciado!")
    print(f"📁 Projeto: {PROJECT_PATH}")
    print(f"📁 Ideias: {ACERVO_PATH}")
    
    app.run_polling(poll_interval=3)

if __name__ == "__main__":
    main()