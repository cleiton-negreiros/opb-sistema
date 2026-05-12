#!/usr/bin/env python3
"""
🤖 Agente Coordenador - OPB Sistema
Orquestra e distribui tarefas para os agentes especializados
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

class CoordinatorAgent:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.agents_dir = self.project_root / "agents"
        self.negocio_dir = self.project_root / "negocio"
        
    def load_brain_context(self):
        """Carrega contexto do cérebro"""
        context = {}
        
        # Ler quem-sou
        quem_sou = self.negocio_dir / "governanca" / "regras" / "quem-sou.md"
        if quem_sou.exists():
            lines = quem_sou.read_text(encoding='utf-8').split('\n')
            for line in lines:
                if "**Nome**:" in line:
                    context['nome'] = line.split('**Nome**:')[-1].strip()
                if "**Missao**:" in line:
                    context['missao'] = line.split('**Missao**:')[-1].strip()[:80]
        
        # Ler projetos ativos
        projetos = self.negocio_dir / "projetos" / "ativos.md"
        if projetos.exists():
            content = projetos.read_text(encoding='utf-8')
            context['projetos'] = [l for l in content.split('\n') if l.strip().startswith('- **')][:5]
        
        return context
    
    def list_agents(self):
        """Lista todos os agentes disponíveis"""
        agents = []
        for d in self.agents_dir.iterdir():
            if d.is_dir() and (d / "main.py").exists():
                soul = d / "SOUL.md"
                nome = d.name
                desc = ""
                if soul.exists():
                    lines = soul.read_text(encoding='utf-8').split('\n')
                    for line in lines:
                        if "**Nome**:" in line:
                            nome = line.split('**Nome**:')[-1].strip()
                        if "**Tipo**:" in line:
                            desc = line.split('**Tipo**:')[-1].strip()
                agents.append({
                    'folder': d.name,
                    'nome': nome,
                    'desc': desc
                })
        return agents
    
    def show_status(self):
        """Mostra status completo do sistema"""
        ctx = self.load_brain_context()
        agents = self.list_agents()
        
        print("=" * 60)
        print("  🤖 COORDENADOR - OPB SISTEMA")
        print("=" * 60)
        
        print("\n🧠 CONTEXTO:")
        nome = ctx.get('nome', 'Não definido')
        missao = ctx.get('missao', 'Não definida')
        print(f"  • Nome: {nome}")
        print(f"  • Missao: {missao}...")
        
        print("\n📋 PROJETOS ATIVOS:")
        projetos = ctx.get('projetos', [])
        if projetos:
            for p in projetos[:3]:
                print(f"  {p}")
        else:
            print("  Nenhum projeto ativo")
        
        print("\n🤖 AGENTES DISPONÍVEIS:")
        for a in agents:
            print(f"  ✅ {a['folder']}")
            if a['desc']:
                print(f"     └ {a['desc']}")
        
        print("\n" + "=" * 60)
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("=" * 60)
    
    def run_agent(self, agent_name: str):
        """Executa um agente específico"""
        agent_path = self.agents_dir / agent_name / "main.py"
        
        if not agent_path.exists():
            print(f"Agente não encontrado: {agent_name}")
            return
        
        print(f"Executando {agent_name}...")
        os.chdir(agent_path.parent)
        subprocess.run(["python", "main.py"])
    
    def run_agent_with_args(self, agent_name: str, args: list):
        """Executa um agente com argumentos"""
        agent_path = self.agents_dir / agent_name / "main.py"
        
        if not agent_path.exists():
            print(f"Agente não encontrado: {agent_name}")
            return
        
        print(f"Executando {agent_name} com args: {args}")
        os.chdir(agent_path.parent)
        subprocess.run(["python", "main.py"] + args)

def main():
    coordinator = CoordinatorAgent()
    
    if len(sys.argv) < 2:
        coordinator.show_status()
        print("""
USO:
  python main.py                    → Ver status
  python main.py run [agente]       → Executar agente
  python main.py run [agente] args  → Executar com argumentos

EXEMPLOS:
  python main.py run telegram_bot
  python main.py run transcricao "URL_VIDEO"
  python main.py run posicionamento "IA negocios"
  python main.py run capa_video "Meu Tema"
""")
        return
    
    if sys.argv[1] == "run":
        if len(sys.argv) > 2:
            agent = sys.argv[2]
            args = sys.argv[3:] if len(sys.argv) > 3 else []
            coordinator.run_agent_with_args(agent, args)
        else:
            print("Uso: python main.py run [agente] [args]")
        return
    
    if sys.argv[1] == "list":
        agents = coordinator.list_agents()
        print("Agentes disponíveis:")
        for a in agents:
            print(f"  - {a['folder']}: {a['desc']}")
        return
    
    # Argumento não reconhecido, mostrar help
    print("Use 'python main.py' para ver status")
    print("Use 'python main.py run [agente]' para executar")

if __name__ == "__main__":
    main()