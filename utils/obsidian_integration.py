#!/usr/bin/env python3
"""
🔗 Obsidian Integration - OPB Sistema
Integração entre o OPB Sistema e Obsidian
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_PATH = Path(__file__).parent.parent
OBSIDIAN_PATH = PROJECT_PATH / "obsidian-vault"

def check_obsidian():
    """Verifica se Obsidian está instalado"""
    paths = [
        "C:\\Users\\cleit\\AppData\\Local\\obsidian\\Obsidian.exe",
        "C:\\Program Files\\Obsidian\\Obsidian.exe",
        os.path.expanduser("~\\AppData\\Local\\obsidian\\Obsidian.exe"),
    ]
    
    for p in paths:
        if Path(p).exists():
            return p
    
    return None

def get_obsidian_exe():
    """Retorna o caminho do executável do Obsidian"""
    return check_obsidian()

def open_in_obsidian(file_path: str = None):
    """Abre o Obsidian com o projeto ou arquivo específico"""
    exe = get_obsidian_exe()
    
    if not exe:
        print("ERRO: Obsidian nao encontrado")
        print("Instale em: https://obsidian.md/download")
        return False
    
    # Usar o projeto como vault
    vault_path = PROJECT_PATH.as_posix()
    
    try:
        if file_path:
            subprocess.Popen([exe, file_path])
        else:
            subprocess.Popen([exe, vault_path])
        print(f"Obsidian aberto: {vault_path}")
        return True
    except Exception as e:
        print(f"ERRO ao abrir Obsidian: {e}")
        return False

def open_file_in_obsidian(relative_path: str):
    """Abre um arquivo específico no Obsidian"""
    exe = get_obsidian_exe()
    
    if not exe:
        print("ERRO: Obsidian nao instalado")
        return False
    
    full_path = PROJECT_PATH / relative_path
    
    if not full_path.exists():
        print(f"ERRO: Arquivo nao encontrado: {relative_path}")
        return False
    
    try:
        subprocess.Popen([exe, full_path.as_posix()])
        print(f"Aberto: {relative_path}")
        return True
    except Exception as e:
        print(f"ERRO: {e}")
        return False

def list_brain_files():
    """Lista arquivos importantes do cérebro"""
    print("\n📁 CÉREBRO - Arquivos do Projeto\n")
    
    importantes = [
        ("MAPA.md", "Índice raiz do cérebro"),
        ("negocio/governanca/regras/quem-sou.md", "Sua identidade"),
        ("negocio/projetos/ativos.md", "Projetos ativos"),
        ("AGENTS.md", "Documentação dos agentes"),
        ("TODO.md", "Tarefas pendentes"),
        ("morning_routine.py", "Rotina matinal"),
    ]
    
    for path, desc in importantes:
        full = PROJECT_PATH / path
        status = "✅" if full.exists() else "❌"
        print(f"  {status} {path}")
        print(f"      └ {desc}")
    
    print("\n💡 Para abrir no Obsidian:")
    print("   python utils/obsidian_integration.py open quem-sou")
    print("   python utils/obsidian_integration.py open projetos")
    print("   python utils/obsidian_integration.py open brain")

def obsidian_quick_links():
    """Gera links rápidos para Obsidian"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║         🔗 Links Rápidos - Abrir no Obsidian               ║
╚══════════════════════════════════════════════════════════════╝

Para usar, execute:
  python utils/obsidian_integration.py open [comando]

Comandos disponíveis:
""")
    
    comandos = [
        ("brain", "Abrir cérebro (MAPA.md)"),
        ("quem-sou", "Ver identidade (quem-sou.md)"),
        ("projetos", "Ver projetos ativos"),
        ("regras", "Ver regras de escrita"),
        ("agentes", "Ver documentação dos agentes"),
        ("todo", "Ver tarefas pendentes"),
        ("ideias", "Ver ideias salvas"),
        ("transcricoes", "Ver transcrições"),
        ("pesquisas", "Ver pesquisas de posicionamento"),
    ]
    
    for cmd, desc in comandos:
        print(f"  python obsidian.py open {cmd:15} → {desc}")
    
    print("""
Ou abra diretamente o Obsidian com todo o projeto:
  python utils/obsidian_integration.py
""")

def obsidian_telegram_message():
    """Retorna mensagem de help para o Telegram"""
    return """🔗 *Integracao Obsidian*

Voce pode abrir arquivos no Obsidian diretamente do seu projeto.

*Arquivos Principais:*
• MAPA.md - Indice do cerebro
• quem-sou.md - Sua identidade
• projetos/ativos.md - Projetos ativos
• AGENTS.md - Agentes

*No seu PC, execute:*
```
python utils/obsidian_integration.py open quem-sou
python utils/obsidian_integration.py open brain
```

*Ou abra o Obsidian:*
```
python utils/obsidian_integration.py
```"""

def main():
    if len(sys.argv) < 2:
        exe = get_obsidian_exe()
        if exe:
            open_in_obsidian()
        else:
            print("Obsidian nao encontrado.")
            print("Baixe em: https://obsidian.md/download")
            list_brain_files()
        return
    
    arg1 = sys.argv[1]
    arg2 = sys.argv[2] if len(sys.argv) > 2 else None
    
    if arg1 == "open" and arg2:
        mapa = {
            "brain": "MAPA.md",
            "quem-sou": "negocio/governanca/regras/quem-sou.md",
            "identidade": "negocio/governanca/regras/quem-sou.md",
            "projetos": "negocio/projetos/ativos.md",
            "regras": "negocio/governanca/regras/linguagem-escrita.md",
            "agentes": "AGENTS.md",
            "todo": "TODO.md",
            "ideias": "acervo/ideias/index.md",
            "transcricoes": "acervo/transcricoes/index.md",
            "pesquisas": "acervo/pesquisas/index.md",
            "hub": "hub.html",
        }
        
        if arg2 in mapa:
            open_file_in_obsidian(mapa[arg2])
        else:
            print(f"Comando desconhecido: {arg2}")
            print("Use: python obsidian.py open [brain|quem-sou|projetos|...]")
        return
    
    if arg1 == "--help" or arg1 == "-h":
        obsidian_quick_links()
        return
    
    if arg1 == "links":
        obsidian_quick_links()
        return
    
    if arg1 == "telegram":
        print(obsidian_telegram_message())
        return
    
    print("Uso: python obsidian.py [comando]")
    print("Use --help para ver opcoes")

if __name__ == "__main__":
    main()