#!/usr/bin/env python3
"""
🧠 Morning Routine - OPB Sistema
Script completo para iniciar o dia: carrega contexto e mostra status dos agentes
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_PATH = Path(__file__).parent

def print_header():
    print("""
╔══════════════════════════════════════════════════════════════╗
║          🌅 BOM DIA! - OPB Sistema Starting...              ║
╚══════════════════════════════════════════════════════════════╝
""")

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def load_brain_summary():
    """Carrega resumo do cérebro"""
    print_section("🧠 CÉREBRO - Contexto do Dia")
    
    # Ler quem-sou
    quem_sou_path = PROJECT_PATH / "negocio" / "governanca" / "regras" / "quem-sou.md"
    if quem_sou_path.exists():
        print("📋 IDENTIDADE:")
        lines = quem_sou_path.read_text(encoding='utf-8').split('\n')
        nome = ""
        missao = ""
        for i, line in enumerate(lines):
            if "**Nome**:" in line:
                nome = line.split("**Nome**:")[-1].strip()
            if "**Missao**:" in line and not missao:
                missao = line.split("**Missao**:")[-1].strip()[:80]
        if nome:
            print(f"   • Nome: {nome}")
        if missao:
            print(f"   • Missao: {missao}...")
    
    # Ler projetos ativos
    projetos_path = PROJECT_PATH / "negocio" / "projetos" / "ativos.md"
    if projetos_path.exists():
        print("\n📋 PROJETOS ATIVOS:")
        content = projetos_path.read_text(encoding='utf-8')
        in_curso = False
        for line in content.split('\n'):
            if "## Em curso" in line:
                in_curso = True
            elif in_curso and line.strip().startswith('- '):
                if "Nada" in line or "vazio" in line.lower():
                    break
                print(f"   {line.strip()}")
            elif line.strip().startswith('##'):
                in_curso = False

def get_git_status():
    """Verifica status do Git"""
    print_section("📊 GIT & DEPLOY")
    
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, cwd=PROJECT_PATH
        )
        commit = result.stdout.strip() if result.returncode == 0 else "N/A"
        print(f"   • Commit: {commit}")
    except:
        print("   • Commit: N/A")
    
    # Ver última atualização
    github = "https://github.com/cleiton-negreiros/opb-sistema"
    vercel = "https://opb-sistema.vercel.app"
    print(f"   • GitHub: {github}")
    print(f"   • Vercel: {vercel}")

def list_agents():
    """Lista todos os agentes disponíveis"""
    print_section("🤖 AGENTES DISPONÍVEIS")
    
    agents_path = PROJECT_PATH / "agents"
    if not agents_path.exists():
        print("   Nenhum agente encontrado")
        return
    
    agentes = []
    for item in agents_path.iterdir():
        if item.is_dir():
            main_py = item / "main.py"
            soul_md = item / "SOUL.md"
            
            nome = item.name
            status = "✅" if main_py.exists() else "❌"
            desc = ""
            
            if soul_md.exists():
                lines = soul_md.read_text(encoding='utf-8').split('\n')
                for line in lines:
                    if "**Nome**:" in line:
                        desc = line.split("**Nome**:")[-1].strip()
                    if "**Tipo**:" in line:
                        desc += " - " + line.split("**Tipo**:")[-1].strip()
            
            agentes.append((nome, status, desc))
    
    for nome, status, desc in sorted(agentes):
        print(f"   {status} {nome}")
        if desc:
            print(f"      └ {desc}")

def list_acervo_stats():
    """Estatísticas do acervo"""
    print_section("📁 ACERVO - Dados do Sistema")
    
    acervo = PROJECT_PATH / "acervo"
    if not acervo.exists():
        print("   Acervo vazio")
        return
    
    pastas = {
        "ideias": "💡 Ideias",
        "pesquisas": "🔍 Pesquisas", 
        "transcricoes": "🎥 Transcrições",
    }
    
    for pasta, label in pastas.items():
        caminho = acervo / pasta
        if caminho.exists():
            arquivos = list(caminho.glob("*.md"))
            print(f"   {label}: {len(arquivos)} arquivos")
        else:
            print(f"   {label}: 0 arquivos")

def show_commands():
    """Mostra comandos disponíveis"""
    print_section("📝 COMANDOS RÁPIDOS")
    
    print("""
   AGENTES:
   python agents/telegram_bot/main.py        → Iniciar Telegram Bot
   python agents/posicionamento/main.py    → Pesquisar perfis
   python agents/transcricao/main.py        → Transcrever vídeo
   
   HUB:
   python server.py                          → Servidor local
   http://localhost:8088/hub.html          → Hub Produtividade
   
   TELEGRAM:
   Envie /start para o bot para ver comandos
   /ideia [texto] → Cadastrar ideia
   /status       → Ver status do sistema
   /agents       → Ver agentes
""")

def run_coordinator_cycle():
    """Executa o ciclo do coordenador (consulta ao consultor + sugestao de acao)."""
    print_section("🤖 COORDENADOR - Ciclo de Orquestracao")
    coord_script = PROJECT_PATH / "agents" / "coordinator" / "main.py"
    if coord_script.exists():
        result = subprocess.run(
            [sys.executable, str(coord_script), "morning"],
            capture_output=True, text=True, timeout=180
        )
        print(result.stdout[-2000:] if result.stdout else "")
        if result.stderr:
            print(f"  [coordinator stderr]: {result.stderr[:300]}")
    else:
        print("  ⚠️  Coordenador nao encontrado")

def run_full_routine():
    """Executa a rotina completa"""
    print_header()
    
    load_brain_summary()
    get_git_status()
    list_agents()
    list_acervo_stats()
    run_audit()
    run_coordinator_cycle()
    show_commands()
    
    print(f"\n{'='*60}")
    print(f"  ✅ Rotina Matinal Concluída - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    print("""
   💡 Dicas para o dia:
   • Use o Telegram Bot para capturar ideias: /ideia [sua ideia]
   • Execute agentes pelo terminal
   • Acesse o hub para produtividade
   • Mantenha o cérebro atualizado!
   """)

def quick_status():
    """Status rápido via Telegram"""
    agents_path = PROJECT_PATH / "agents"
    agentes = [d.name for d in agents_path.iterdir() if d.is_dir() and (d / "main.py").exists()]
    
    acervo = PROJECT_PATH / "acervo"
    ideias = len(list((acervo / "ideias").glob("*.md"))) if (acervo / "ideias").exists() else 0
    transcricoes = len(list((acervo / "transcricoes").glob("*.md"))) if (acervo / "transcricoes").exists() else 0
    
    return f"""🌅 *Bom Dia! - OPB Sistema*

📊 *Status:*
• Agentes: {len(agentes)}
• Ideias: {ideias}
• Transcricoes: {transcricoes}
• Deploy: ✅ online

📁 *Links:*
• Hub: https://opb-sistema.vercel.app/hub.html
• GitHub: https://github.com/cleiton-negreiros/opb-sistema

💡 *Comandos:*
/ideia [texto] - Nova ideia
/agents - Ver agentes
/status - Este status
/iniciar - Rotina matinal
"""

def run_audit():
    print_section("🔍 AUDITORIA DE CÓDIGO")
    audit_script = PROJECT_PATH / "audit" / "auditoria_diaria.py"
    if audit_script.exists():
        result = subprocess.run(
            [sys.executable, str(audit_script), "--quick"],
            capture_output=True, text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print("  ⚠️  Auditoria encontrou problemas críticos")
    else:
        print("  ⚠️  Script de auditoria não encontrado")

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--status" or arg == "--quick":
            print(quick_status())
            return
        
        if arg == "--audit":
            run_audit()
            run_coordinator_cycle()
            return
        
        if arg == "--help":
            print("""
🧠 Morning Routine - OPB Sistema

USO:
   python morning_routine.py
   python morning_routine.py --status
   python morning_routine.py --quick
   python morning_routine.py --audit
   python morning_routine.py --help

OPCOES:
   (vazio)    → Rotina completa com contexto
   --status   → Status resumido
   --quick    → Status rapido (para Telegram)
   --audit    → + Auditoria de código completa
   --help     → Esta ajuda
""")
            return
    
    run_full_routine()

if __name__ == "__main__":
    main()