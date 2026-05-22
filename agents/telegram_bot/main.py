import os
import sys
import json
import logging
import subprocess
import socket
from datetime import datetime
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent.parent / ".env")
except ImportError:
    pass  # python-dotenv not installed, use system env vars

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not set! Create a .env file or set the environment variable.")
    sys.exit(1)

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

def run_agent(agent_path: str, args: list = None, timeout: int = 60) -> str:
    """Executa um agente Python e retorna stdout."""
    full_path = PROJECT_PATH / agent_path
    if not full_path.exists():
        return f"❌ Agente não encontrado: {agent_path}"
    try:
        cmd = [sys.executable, str(full_path)] + (args or [])
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=str(PROJECT_PATH))
        if result.returncode == 0:
            return result.stdout[:2000] if result.stdout else "✅ Concluído (sem output)"
        else:
            return f"❌ Erro: {(result.stderr or result.stdout or 'desconhecido')[:1000]}"
    except subprocess.TimeoutExpired:
        return f"⏱️ Timeout ({timeout}s). Tente manualmente."
    except Exception as e:
        return f"❌ Erro: {str(e)[:200]}"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 *NegreirosBot — Paz na Conta*\n\n"
        "Olá! Seu assistente do OPB Sistema.\n\n"
        "🧠 *CÉREBRO:*\n"
        "• /cerebro — Resumo completo\n"
        "• /regras — Quem sou\n"
        "• /projetos — Projetos ativos\n"
        "• /posicionamento — Posicionamento atual\n\n"
        "💡 *IDEIAS:*\n"
        "• /ideia [texto] — Cadastrar ideia\n"
        "• /ideias — Ver ideias\n"
        "• Envie texto direto → salva como ideia\n\n"
        "🎤 *ÁUDIO:*\n"
        "• Envie áudio de voz → transcreve automaticamente!\n\n"
        "🎬 *VÍDEO:*\n"
        "• /cortarsilencio [video] — Corta silêncios do vídeo\n"
        "• /reels [tema] — Gera roteiro para Reels/Shorts\n\n"
        "📱 *CONTEÚDO:*\n"
        "• /carrossel [tema] — Gerar carrossel\n"
        "• /texto [objetivo] — Gerar post Instagram\n"
        "• /hashtags [tema] — Gerar hashtags otimizadas\n"
        "• /capavideo [tema] — Ideias de capa\n"
        "• /liturgico — Temas do calendário litúrgico\n\n"
        "📋 *TAREFAS:*\n"
        "• /tarefas — Ver pendências\n"
        "• /tarefa [desc] — Nova tarefa\n"
        "• /concluir [id] — Concluir tarefa\n\n"
        "⚙️ /status — Status do sistema\n"
        "🌐 /iniciar — Iniciar serviços\n"
        "📺 /transcrever — Transcrição YouTube\n"
        "🆔 /meuid — Seu Chat ID",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *Ajuda — NegreirosBot*\n\n"
        "🧠 *CÉREBRO*\n"
        "• /cerebro — Status do diretório cérebro\n"
        "• /regras — Exibe quem-sou.md\n"
        "• /projetos — Lista projetos\n"
        "• /posicionamento — Posicionamento atual\n\n"
        "📅 *PLANEJAMENTO*\n"
        "• /plano — Ver cronograma do mês\n"
        "• /briefing [tema] [formato] — Gerar briefing estratégico\n\n"
        "🎠 *AGENTES DE CONTEÚDO*\n"
        "• /carrossel [tema] — Gera carrossel Instagram\n"
        "• /texto [objetivo] — Gera post para Instagram\n"
        "• /capavideo [tema] [qtd] — Ideias de capa\n"
        "• /consumo [texto] — Processa conteúdo\n"
        "• /radagast — Executa curadoria\n\n"
        "📋 *QUADRO DE AVISOS*\n"
        "• /tarefas — Lista pendências\n"
        "• /tarefa [desc] — Adiciona tarefa\n"
        "• /concluir [id] — Conclui tarefa\n\n"
        "💡 *IDEIAS*\n"
        "• /ideia [texto] — Nova ideia\n"
        "• /ideias — Listar ideias\n"
        "• Texto/áudio direto → processa automaticamente\n\n"
        "⚙️ *SISTEMA*\n"
        "• /status — Status completo\n"
        "• /iniciar — Inicia API + servidor\n"
        "• /agents — Listar agentes\n"
        "• /meuid — Seu Chat ID\n"
        "• /transcrever — Transcrição YouTube\n"
        "• /hub — Hub produtividade\n"
        "• /obsidian — Obsidian\n"
        "• /executar [cmd] — Executa comando no PC",
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
    """Recebe mensagem de voz e transcreve automaticamente"""
    await update.message.reply_text("🎤 *Processando áudio...*", parse_mode="Markdown")
    
    try:
        # Baixar o arquivo de voz
        file = await context.bot.get_file(update.message.voice.file_id)
        file_path = PROJECT_PATH / "acervo" / "temp" / f"voice_{update.message.message_id}.ogg"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        await file.download_to_drive(str(file_path))
        
        await update.message.reply_text("🎤 *Transcrevendo áudio...*", parse_mode="Markdown")
        
        # Transcrever usando o agente
        out = run_agent("agents/transcrever-audio/main.py", [str(file_path)], timeout=120)
        
        if out and "❌" not in out:
            # Salvar transcrição
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            trans_path = ACERVO_PATH.parent / "transcricoes" / f"voz_{timestamp}.md"
            trans_path.parent.mkdir(parents=True, exist_ok=True)
            
            content = f"""---
name: "Transcrição {timestamp}"
tipo: transcricao_voz
autor: {update.effective_user.name}
data: {datetime.now().strftime("%Y-%m-%d")}
---

# 🎤 Transcrição de Voz

**Autor:** {update.effective_user.name}
**Data:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Status:** ✅ Transcrito

---

{out}

---

*Transcrito via NegreirosBot*"""
            
            trans_path.write_text(content, encoding='utf-8')
            
            # Enviar transcrição
            if len(out) > 4000:
                out = out[:4000] + "\n\n... (truncado)"
            
            await update.message.reply_text(
                f"📝 *Transcrição:*\n\n```\n{out}\n```",
                parse_mode="Markdown"
            )
            
            # Salvar como ideia também
            save_ideia(out[:200], update.effective_user.name)
        else:
            await update.message.reply_text(
                f"⚠️ *Não foi possível transcrever.*\n\n"
                f"Erro: {out[:200]}\n\n"
                f"💡 *Dica:* Envie a ideia em texto!",
                parse_mode="Markdown"
            )
        
        # Limpar arquivo temporário
        if file_path.exists():
            file_path.unlink()
            
    except Exception as e:
        await update.message.reply_text(
            f"❌ *Erro ao processar áudio:*\n\n`{str(e)[:200]}`",
            parse_mode="Markdown"
        )

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
    """Executa rotina matinal — sobe API + Bot + plataforma + Radagast"""
    await update.message.reply_text("🌅 *Iniciando OPB Sistema...*", parse_mode="Markdown")

    resultados = []
    inicio = datetime.now()

    # 1. Morning routine
    try:
        r = subprocess.run(
            [sys.executable, str(PROJECT_PATH / "morning_routine.py")],
            capture_output=True, text=True, timeout=30,
            cwd=str(PROJECT_PATH)
        )
        resultados.append(f"🧠 Contexto: {'✅' if r.returncode == 0 else '❌'}")
    except Exception as e:
        resultados.append(f"🧠 Contexto: ❌ {str(e)[:60]}")

    # 2. API server (se não estiver rodando)
    api_rodando = False
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        api_rodando = s.connect_ex(("127.0.0.1", 5000)) == 0
        s.close()
    except:
        pass

    if not api_rodando:
        try:
            subprocess.Popen(
                [sys.executable, str(PROJECT_PATH / "api_server.py")],
                cwd=str(PROJECT_PATH),
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            resultados.append("🌐 API Server: ✅ iniciado")
        except Exception as e:
            resultados.append(f"🌐 API Server: ❌ {str(e)[:60]}")
    else:
        resultados.append("🌐 API Server: ✅ já rodando")

    # 3. Telegram Bot (self-check)
    resultados.append("🤖 Telegram Bot: ✅ ativo (você está falando comigo)")

    # 4. Radagast
    try:
        r = subprocess.run(
            [sys.executable, str(PROJECT_PATH / "agents" / "radagast" / "radagast.py")],
            capture_output=True, text=True, timeout=120,
            cwd=str(PROJECT_PATH / "agents" / "radagast")
        )
        if r.returncode == 0:
            resultados.append(f"📡 Radagast: ✅ executado")
            # Envia resumo do Radagast
            if r.stdout:
                lines = [l for l in r.stdout.split('\n') if l.strip()]
                resume = '\n'.join(lines[-5:])
                await update.message.reply_text(
                    f"📡 *Radagast - Resumo*\n```\n{resume[:1500]}\n```",
                    parse_mode="Markdown"
                )
        else:
            resultados.append(f"📡 Radagast: ⚠️ erro (veja logs)")
    except Exception as e:
        resultados.append(f"📡 Radagast: ❌ {str(e)[:60]}")

    tempo = (datetime.now() - inicio).total_seconds()

    msg = f"""🌅 *Sistema Iniciado!* ({tempo:.0f}s)

{chr(10).join(resultados)}

📌 *Acesse:*
• Plataforma: http://localhost:5000
• Hub: https://opb-sistema.vercel.app/hub.html

💡 *Comandos:*
/status - Status completo
/agents - Listar agentes
/radagast - Rodar curadoria agora

*Bom trabalho!* 🚀"""

    await update.message.reply_text(msg, parse_mode="Markdown")

async def radagast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roda Radagast e envia resultado."""
    await update.message.reply_text("📡 *Executando Radagast...* (pode levar 2-3 min)", parse_mode="Markdown")
    try:
        r = subprocess.run(
            [sys.executable, str(PROJECT_PATH / "agents" / "radagast" / "radagast.py")],
            capture_output=True, text=True, timeout=180,
            cwd=str(PROJECT_PATH / "agents" / "radagast")
        )
        if r.returncode == 0:
            out = r.stdout[-2000:] if r.stdout else "✅ Curadoria concluida (sem output)"
            await update.message.reply_text(
                f"📡 *Radagast - Concluido*\n```\n{out}\n```",
                parse_mode="Markdown"
            )
        else:
            err = (r.stderr or r.stdout or "Erro desconhecido")[:1500]
            await update.message.reply_text(
                f"📡 *Radagast - Erro*\n```\n{err}\n```",
                parse_mode="Markdown"
            )
    except subprocess.TimeoutExpired:
        await update.message.reply_text("⏱️ Radagast excedeu 3 min. Tente executar manualmente:\n`python agents/radagast/radagast.py`", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {str(e)[:200]}")

async def meuid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra o chat_id do usuário."""
    cid = update.effective_chat.id
    await update.message.reply_text(
        f"🆔 Seu Chat ID: `{cid}`\n\n"
        f"Use este ID para configurar Radagast:\n"
        f"1. Abra `agents/radagast/.env`\n"
        f"2. Adicione: `RADAGAST_CHAT_ID={cid}`\n"
        f"3. Adicione: `RADAGAST_BOT_TOKEN={TOKEN}`",
        parse_mode="Markdown"
    )

# ============================================
# AGENTES — Comandos
# ============================================

async def carrossel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gera carrossel via agente Carrossel."""
    if not context.args:
        await update.message.reply_text("🎠 *Carrossel*\n\nUso: `/carrossel [tema]`\nEx: `/carrossel Dízimo e organização financeira`", parse_mode="Markdown")
        return
    tema = " ".join(context.args)
    await update.message.reply_text(f"🎠 Gerando carrossel: `{tema[:60]}...`", parse_mode="Markdown")
    out = run_agent("agents/carrossel/main.py", [tema, "educational", "5"], timeout=60)
    await update.message.reply_text(f"🎠 *Carrossel*\n```\n{out[:2000]}\n```", parse_mode="Markdown")

async def consumo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa conteúdo via Agente Consumo."""
    if not context.args:
        await update.message.reply_text("📖 *Consumo*\n\nUso: `/consumo [texto]`\nProcessa texto e salva no acervo.", parse_mode="Markdown")
        return
    texto = " ".join(context.args)
    await update.message.reply_text(f"📖 Processando conteúdo... ({len(texto)} caracteres)", parse_mode="Markdown")
    out = run_agent("agents/consumo/main.py", [f"'{texto[:1500]}'", "resumo", "Telegram"], timeout=60)
    await update.message.reply_text(f"📖 *Consumo*\n```\n{out[:1500]}\n```", parse_mode="Markdown")

async def textogen_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gera post para Instagram via Text Generator."""
    if not context.args:
        await update.message.reply_text("✍️ *Text Generator*\n\nUso: `/texto [objetivo]`\nEx: `/texto Como economizar no supermercado`", parse_mode="Markdown")
        return
    objetivo = " ".join(context.args)
    await update.message.reply_text(f"✍️ Gerando texto...", parse_mode="Markdown")
    out = run_agent("agents/text_generator/main.py", [objetivo, "educational"], timeout=60)
    await update.message.reply_text(f"✍️ *Texto Gerado*\n```\n{out[:2000]}\n```", parse_mode="Markdown")

async def capavideo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gera ideias de capa via Capa Vídeo."""
    if not context.args:
        await update.message.reply_text("📸 *Capa Vídeo*\n\nUso: `/capavideo [tema] [qtd]`\nEx: `/capavideo Finanças católicas 5`", parse_mode="Markdown")
        return
    args = context.args
    tema = " ".join(args[:-1]) if len(args) > 1 else args[0]
    qtd = args[-1] if len(args) > 1 and args[-1].isdigit() else "5"
    await update.message.reply_text(f"📸 Gerando capas para: `{tema[:60]}`...", parse_mode="Markdown")
    out = run_agent("agents/capa_video/main.py", [tema, qtd], timeout=60)
    await update.message.reply_text(f"📸 *Capas*\n```\n{out[:2000]}\n```", parse_mode="Markdown")

async def posicionamento_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra o posicionamento atual."""
    path = PROJECT_PATH / "negocio" / "governanca" / "quem-sou.md"
    if not path.exists():
        await update.message.reply_text("❌ Arquivo de posicionamento não encontrado.")
        return
    content = path.read_text(encoding="utf-8")
    # Extrair só seção de posicionamento
    if "## Posicionamento" in content:
        pos = content.split("## Posicionamento")[1].split("##")[0].strip()
        await update.message.reply_text(f"📍 *Posicionamento*\n\n{pos[:2000]}", parse_mode="Markdown")
    else:
        await update.message.reply_text("Seção de posicionamento não encontrada em quem-sou.md")

async def tarefas_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista tarefas do Quadro de Avisos."""
    out = run_agent("agents/quadro-de-avisos/main.py", ["listar"], timeout=15)
    await update.message.reply_text(f"📋 *Quadro de Avisos*\n```\n{out[:2000]}\n```", parse_mode="Markdown")

async def plano_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra o cronograma de conteúdo."""
    await update.message.reply_text("📅 *Consultando cronograma...*", parse_mode="Markdown")
    out = run_agent("agents/content_planner/main.py", ["load_plan"], timeout=30)
    try:
        plan = json.loads(out)
        msg = "📅 *Cronograma de Conteúdo*\n\n"
        for item in plan["cronograma"]:
            msg += f"📍 *{item['semana']}*\n"
            msg += f"📺 YT: {item['youtube']}\n"
            msg += f"📸 IG: {item['instagram']}\n\n"
        await update.message.reply_text(msg, parse_mode="Markdown")
    except:
        await update.message.reply_text(f"❌ Erro ao carregar plano:\n```\n{out[:500]}\n```", parse_mode="Markdown")

async def briefing_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gera briefing estratégico para um tema."""
    if len(context.args) < 2:
        await update.message.reply_text("📅 *Gerar Briefing*\n\nUso: `/briefing [tema] [formato]`\nEx: `/briefing Dívidas carrossel`", parse_mode="Markdown")
        return
    
    formato = context.args[-1]
    tema = " ".join(context.args[:-1])
    
    await update.message.reply_text(f"📅 Gerando briefing estratégico para: `{tema}`...", parse_mode="Markdown")
    out = run_agent("agents/content_planner/main.py", [tema, formato], timeout=30)
    
    try:
        brief = json.loads(out)
        msg = f"🎯 *Briefing Estratégico*\n\n"
        msg += f"📝 *Tema:* {brief['theme']}\n"
        msg += f"🎨 *Formato:* {brief['format']}\n\n"
        msg += f"🔍 *Detalhes:*\n{brief['details'][:3000]}"
        await update.message.reply_text(msg, parse_mode="Markdown")
    except:
        await update.message.reply_text(f"❌ Erro ao gerar briefing:\n```\n{out[:1000]}\n```", parse_mode="Markdown")

async def tarefa_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Adiciona tarefa ao Quadro de Avisos."""
    if not context.args:
        await update.message.reply_text("📋 *Nova Tarefa*\n\nUso: `/tarefa [descrição]`\nEx: `/tarefa Produzir carrossel sobre dízimo`\n\nPara definir agente/prioridade:\n`/tarefa [desc] --agente carrossel --prioridade alta`", parse_mode="Markdown")
        return
    texto = " ".join(context.args)
    out = run_agent("agents/quadro-de-avisos/main.py", ["adicionar", texto], timeout=15)
    await update.message.reply_text(f"📋 {out}", parse_mode="Markdown")

async def concluir_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Conclui tarefa do Quadro de Avisos."""
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("📋 *Concluir Tarefa*\n\nUso: `/concluir [id]`\nVeja os IDs com /tarefas", parse_mode="Markdown")
        return
    tid = context.args[0]
    out = run_agent("agents/quadro-de-avisos/main.py", ["concluir", tid], timeout=15)
    await update.message.reply_text(f"📋 {out}", parse_mode="Markdown")

async def cortarsilencio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Corta silêncios de um vídeo."""
    await update.message.reply_text(
        "🎬 *Cortar Silêncios*\n\n"
        "Envie o vídeo como documento ou use:\n\n"
        "No PC/Termux:\n"
        "```\n"
        "python agents/corta-silencio/main.py video.mp4\n"
        "```\n\n"
        "Opções:\n"
        "• `--threshold -30` (sensibilidade dB)\n"
        "• `--min-duration 0.5` (duração mínima silêncio)\n"
        "• `--keep-silence 0.3` (transição natural)",
        parse_mode="Markdown"
    )

async def reels_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gera roteiro para Reels/Shorts."""
    if not context.args:
        await update.message.reply_text(
            "🎬 *Roteiro para Reels/Shorts*\n\n"
            "Uso: `/reels [tema]`\n\n"
            "Exemplos:\n"
            "• `/reels 3 erros financeiros que católicos cometem`\n"
            "• `/reels como organizar orçamento familiar`\n"
            "• `/reels dizimo é obrigatório`\n\n"
            "Opções:\n"
            "• `--duracao 60` (30, 60 ou 90 segundos)\n"
            "• `--formato shorts` (reels, shorts ou tiktok)",
            parse_mode="Markdown"
        )
        return

    tema = " ".join(context.args)
    await update.message.reply_text(f"🎬 *Gerando roteiro:*\n\n`{tema[:80]}...`", parse_mode="Markdown")
    out = run_agent("agents/reels_script/main.py", [tema], timeout=60)
    if out and len(out) > 4000:
        out = out[:4000] + "\n\n... (truncado)"
    await update.message.reply_text(f"🎬 *Roteiro:*\n\n```\n{out}\n```", parse_mode="Markdown")

async def hashtags_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gera hashtags otimizadas."""
    if not context.args:
        await update.message.reply_text(
            "🏷️ *Gerador de Hashtags*\n\n"
            "Uso: `/hashtags [tema]`\n\n"
            "Exemplos:\n"
            "• `/hashtags dízimo e organização financeira`\n"
            "• `/hashtags --pilar espiritual`\n"
            "• `/hashtags --pilar pratico --blocos 3`",
            parse_mode="Markdown"
        )
        return

    tema = " ".join(context.args)
    await update.message.reply_text(f"🏷️ *Gerando hashtags:*\n\n`{tema[:80]}`", parse_mode="Markdown")
    out = run_agent("agents/hashtags/main.py", [tema], timeout=30)
    if out and len(out) > 4000:
        out = out[:4000] + "\n\n... (truncado)"
    await update.message.reply_text(f"🏷️ *Hashtags:*\n\n```\n{out}\n```", parse_mode="Markdown")

async def liturgico_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra temas do calendário litúrgico."""
    await update.message.reply_text("📅 *Consultando calendário litúrgico...*", parse_mode="Markdown")
    out = run_agent("agents/liturgico/main.py", ["hoje"], timeout=30)
    if out and len(out) > 4000:
        out = out[:4000] + "\n\n... (truncado)"
    await update.message.reply_text(f"📅 *Calendário Litúrgico:*\n\n```\n{out}\n```", parse_mode="Markdown")

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
    
    # Resetar sessão no servidor do Telegram
    import requests, time
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=10)
        time.sleep(3)
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
    app.add_handler(CommandHandler("radagast", radagast_command))
    app.add_handler(CommandHandler("meuid", meuid_command))
    app.add_handler(CommandHandler("transcrever", transcrever_help_command))
    app.add_handler(CommandHandler("obsidian", obsidian_command))
    app.add_handler(CommandHandler("cerebro", cerebro_command))
    app.add_handler(CommandHandler("ideias", ideias_command))
    app.add_handler(CommandHandler("carrossel", carrossel_command))
    app.add_handler(CommandHandler("consumo", consumo_command))
    app.add_handler(CommandHandler("texto", textogen_command))
    app.add_handler(CommandHandler("capavideo", capavideo_command))
    app.add_handler(CommandHandler("posicionamento", posicionamento_command))
    app.add_handler(CommandHandler("plano", plano_command))
    app.add_handler(CommandHandler("briefing", briefing_command))
    app.add_handler(CommandHandler("tarefas", tarefas_command))
    app.add_handler(CommandHandler("tarefa", tarefa_command))
    app.add_handler(CommandHandler("concluir", concluir_command))
    app.add_handler(CommandHandler("cortarsilencio", cortarsilencio_command))
    app.add_handler(CommandHandler("reels", reels_command))
    app.add_handler(CommandHandler("hashtags", hashtags_command))
    app.add_handler(CommandHandler("liturgico", liturgico_command))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, voice_command))
    app.add_handler(CommandHandler("transcreveraudio", transcrever_help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 NegreirosBot iniciado!")
    print(f"📁 Projeto: {PROJECT_PATH}")
    print(f"📁 Ideias: {ACERVO_PATH}")
    
    app.run_polling(poll_interval=3, drop_pending_updates=True)

if __name__ == "__main__":
    main()