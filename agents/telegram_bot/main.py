import os
import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, VoiceHandler

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
        "🎯 *NegreirosBot - OPB Sistema*\n\n"
        "Olá! Sou seu assistant daily driver.\n\n"
        "🧠 *CÉREBRO:*\n"
        "• /cerebro - Resumo completo\n"
        "• /iniciar - Rotina matinal\n"
        "• /regras - Quem sou\n"
        "• /projetos - Projetos ativos\n\n"
        "💡 *IDEIAS:*\n"
        "• Envie ideia diretamente\n"
        "• /ideia [texto]\n"
        "• /ideias - Ver ideias\n"
        "• 🎤 Envie áudio (gravação) → salva nota de voz\n\n"
        "🎬 *TRANSCRIÇÃO:*\n"
        "• /transcrever - Como transcrever YouTube\n\n"
        "🤖 *AGENTES:*\n"
        "• /status - Status completo\n"
        "• /agents - Ver agentes\n\n"
        "🔗 *LINKS:*\n"
        "• /hub - Hub produtividade\n"
        "• /obsidian - Obsidian\n\n"
        "⚠️ /executar - Executar (PC)",
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

async def cerebro_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra resumo completo do cérebro"""
    
    # 1. Identidade
    quem_sou = ""
    quem_sou_path = PROJECT_PATH / "negocio" / "governanca" / "regras" / "quem-sou.md"
    if quem_sou_path.exists():
        lines = quem_sou_path.read_text(encoding="utf-8").split("\n")
        for line in lines:
            if "**Nome**:" in line:
                quem_sou += f"• *Nome:* {line.split('**Nome**:')[-1].strip()}\n"
            if "**Missao**:" in line:
                quem_sou += f"• *Missao:* {line.split('**Missao**:')[-1].strip()[:60]}...\n"
            if "**Tom de Voz**:" in line or "tom_de_voz" in line.lower():
                quem_sou += f"• *Tom:* {line.split(':')[-1].strip()[:40]}...\n"
            if "**Valores**:" in line:
                valores = line.split('**Valores**:')[-1].strip()[:50]
                quem_sou += f"• *Valores:* {valores}...\n"
    
    # 2. Projetos
    projetos = ""
    projetos_path = PROJECT_PATH / "negocio" / "projetos" / "ativos.md"
    if projetos_path.exists():
        content = projetos_path.read_text(encoding="utf-8")
        for line in content.split("\n"):
            if line.strip().startswith("- **") and "**—" in line:
                projeto = line.split("**")[1] if len(line.split("**")) > 1 else ""
                projetos += f"• {projeto}\n"
            elif line.strip().startswith("- **") and "**" in line:
                # Pegar só o nome do projeto
                pass
    
    # 3. Stats
    agentes = len([d for d in (PROJECT_PATH / "agents").iterdir() if d.is_dir() and (d / "main.py").exists()])
    ideias = len(list((ACERVO_PATH).glob("*.md"))) if ACERVO_PATH.exists() else 0
    transcricoes = len(list((PROJECT_PATH / "acervo" / "transcricoes").glob("*.md"))) if (PROJECT_PATH / "acervo" / "transcricoes").exists() else 0
    
    msg = f"""🧠 *CÉREBRO COMPLETO*

📋 *IDENTIDADE:*
{quem_sou or "Nao definido"}

📁 *PROJETOS:*
{projetos or "Nenhum projeto ativo"}

📊 *ESTATÍSTICAS:*
• Agentes: {agentes}
• Ideias: {ideias}
• Transcrições: {transcricoes}

🔗 *LINKS:*
• Hub: https://opb-sistema.vercel.app/hub.html
• GitHub: https://github.com/cleiton-negreiros/opb-sistema

💡 *Ver detalhes:*
/regras - Ver identidade completa
/projetos - Ver projetos detalhados
/agents - Ver agentes
/ideias - Ver ideias"""
    
    await update.message.reply_text(msg, parse_mode="Markdown")

async def ideias_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista ideias cadastradas"""
    ensure_acervo()
    ideias = sorted(ACERVO_PATH.glob("*.md"), reverse=True)[:10]
    
    if ideias:
        msg = "💡 *Últimas Ideias:*\n\n"
        for f in ideias:
            content = f.read_text(encoding="utf-8")
            # Extrair título
            for line in content.split("\n"):
                if line.startswith("# "):
                    titulo = line.replace("# ", "")[:60]
                    break
            else:
                titulo = f.name
            
            # Data
            for line in content.split("\n"):
                if "**Data**:" in line:
                    data = line.split("**Data**:")[-1].strip()[:10]
                    break
            else:
                data = ""
            
            msg += f"• {titulo} ({data})\n"
    else:
        msg = "💡 Nenhuma ideia ainda.\n\nEnvie uma ideia!"
    
    await update.message.reply_text(msg, parse_mode="Markdown")

async def voice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe mensagem de voz e salva (precisa ser transcrita manualmente)"""
    await update.message.reply_text(
        "🎤 *Mensagem de voz recebida!*\n\n"
        "Infelizmente ainda não consigo transcrever áudio automaticamente.\n\n"
        "Por enquanto:\n"
        "• Transcreva a ideia em texto\n"
        "• Ou use `/transcrever` para transcrever vídeos do YouTube\n\n"
        "💡 *Dica:* Fale o que pensou e depois mande em texto!",
        parse_mode="Markdown"
    )
    
    # Salvar como nota de voz (para futura transcrição)
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = ACERVO_PATH / f"voz_{timestamp}.md"
    
    user = update.effective_user.name
    content = f"""---
name: "Nota de Voz {timestamp}"
tipo: nota_voz
autor: {user}
data: {datetime.now().strftime("%Y-%m-%d")}
---

# 🎤 Nota de Voz

**Autor:** {user}
**Data:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Status:** ⏳ Aguardando transcrição

---

*Envie a transcrição desta ideia para atualizar.*"""

    filepath.write_text(content, encoding='utf-8')

async def transcrever_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎥 *Transcrever Video do YouTube*\n\n"
        "No seu PC/celular, execute:\n\n"
        "```\n"
        "cd agents/transcricao\n"
        "python main.py \"URL_DO_VIDEO\"\n"
        "```\n\n"
        "Exemplo:\n"
        "```\n"
        "python main.py \"https://youtu.be/VIDEO_ID\"\n"
        "```\n\n"
        "O video sera transcrito e salvo em `acervo/transcricoes/`",
        parse_mode="Markdown"
    )

async def obsidian_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔗 *Obsidian Integration*\n\n"
        "O cerebro do OPB Sistema usa arquivos markdown compatíveis com Obsidian!\n\n"
        "*No seu PC:*\n"
        "```\n"
        "python utils/obsidian_integration.py open quem-sou\n"
        "python utils/obsidian_integration.py open projetos\n"
        "python utils/obsidian_integration.py\n"
        "```\n\n"
        "*Arquivos principais:*\n"
        "• MAPA.md - Indice do cerebro\n"
        "• quem-sou.md - Sua identidade\n"
        "• projetos/ativos.md - Projetos\n"
        "• AGENTS.md - Documentacao\n\n"
        "*Dica:* Abra o projeto como vault no Obsidian!",
        parse_mode="Markdown"
    )

async def iniciar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Executa rotina matinal"""
    await update.message.reply_text("🌅 *Carregando Rotina Matinal...*", parse_mode="Markdown")
    
    # Carregar contexto do cérebro
    quem_sou = ""
    quem_sou_path = PROJECT_PATH / "negocio" / "governanca" / "regras" / "quem-sou.md"
    if quem_sou_path.exists():
        lines = quem_sou_path.read_text(encoding="utf-8").split("\n")
        for line in lines:
            if "**Nome**:" in line:
                quem_sou = line.split("**Nome**:")[-1].strip()
    
    # Projetos ativos
    projetos = ""
    projetos_path = PROJECT_PATH / "negocio" / "projetos" / "ativos.md"
    if projetos_path.exists():
        content = projetos_path.read_text(encoding="utf-8")
        for line in content.split("\n"):
            if line.strip().startswith("- **") and "**—" in line:
                projetos += line.strip() + "\n"
    
    # Contadores
    agentes = len([d for d in (PROJECT_PATH / "agents").iterdir() if d.is_dir()])
    ideias = len(list((ACERVO_PATH).glob("*.md"))) if ACERVO_PATH.exists() else 0
    transcricoes = len(list((PROJECT_PATH / "acervo" / "transcricoes").glob("*.md"))) if (PROJECT_PATH / "acervo" / "transcricoes").exists() else 0
    
    msg = f"""🌅 *Bom Dia! - OPB Sistema*

🧠 *Contexto:*
• Nome: {quem_sou or 'Nao definido'}
• Acesse `/regras` para ver perfil completo

📋 *Projetos:*
{projetos or 'Nenhum projeto ativo'}

📊 *Estatisticas:*
• Agentes: {agentes}
• Ideias: {ideias}
• Transcricoes: {transcricoes}

🔗 *Links:*
• Hub: https://opb-sistema.vercel.app/hub.html
• GitHub: https://github.com/cleiton-negreiros/opb-sistema

💡 *Acoes Rapidas:*
/ideia [texto] - Nova ideia
/transcrever - Como transcrever video
/agents - Ver todos os agentes
/status - Status completo

*Tenha um otimo dia!*"""
    
    await update.message.reply_text(msg, parse_mode="Markdown")

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
    
    # Limpar conflitos anteriores
    import requests
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset=-1")
    except:
        pass
    
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
    app.add_handler(CommandHandler("iniciar", iniciar_command))
    app.add_handler(CommandHandler("transcrever", transcrever_help_command))
    app.add_handler(CommandHandler("obsidian", obsidian_command))
    app.add_handler(CommandHandler("cerebro", cerebro_command))
    app.add_handler(CommandHandler("ideias", ideias_command))
    app.add_handler(MessageHandler(filters.VOICE, voice_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 NegreirosBot iniciado!")
    print(f"📁 Projeto: {PROJECT_PATH}")
    print(f"📁 Ideias: {ACERVO_PATH}")
    
    app.run_polling(poll_interval=3)

if __name__ == "__main__":
    main()