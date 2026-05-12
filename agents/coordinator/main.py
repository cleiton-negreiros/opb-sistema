#!/usr/bin/env python3
"""
Agente Coordenador - OPB Sistema
Orquestra e distribui tarefas para os agentes especializados
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

class CoordinatorAgent:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.context_dir = self.project_root / "context-brain"
        self.agents_dir = self.project_root / "agents"
        self.todo_file = self.project_root / "TODO.md"
        self.context = self._load_context()
    
    def _load_context(self):
        context = {}
        for file in ["business-core.json", "personal-profile.json", "goals.json"]:
            path = self.context_dir / file
            if path.exists():
                with open(path) as f:
                    context[file.replace(".json", "")] = json.load(f)
        return context
    
    def _save_todo(self, content):
        with open(self.todo_file, "w") as f:
            f.write(content)
    
    def _get_todo(self):
        if self.todo_file.exists():
            with open(self.todo_file) as f:
                return f.read()
        return ""
    
    def greet(self):
        business = self.context.get("business-core", {})
        nome = self.context.get("personal-profile", {}).get("nome", "Amigo")
        missao = business.get("missao", "automação de tarefas")
        
        print("=" * 50)
        print(f"  🤖 COORDENADOR OPB - SISTEMA")
        print("=" * 50)
        print()
        print(f"  Olá {nome}! Tudo certo?")
        print(f"  Missão: {missao[:50]}...")
        print()
        print("  📋 Tarefas disponíveis:")
        print()
    
    def list_tasks(self):
        todo = self._get_todo()
        lines = todo.split("\n")
        
        current_section = ""
        tasks = []
        
        for line in lines:
            if line.startswith("## "):
                current_section = line.replace("## ", "").strip()
            elif line.startswith("- [ ] "):
                task = line.replace("- [ ] ", "").strip()
                section = "backlog" if current_section in ["", "📋 Backlog"] else current_section
                tasks.append({"text": task, "section": section, "status": "pending"})
            elif line.startswith("- [x] "):
                task = line.replace("- [x] ", "").strip()
                section = current_section if current_section else "concluído"
                tasks.append({"text": task, "section": section, "status": "done"})
        
        return tasks
    
    def show_tasks(self):
        tasks = self.list_tasks()
        
        backlog = [t for t in tasks if t["status"] == "pending"]
        done = [t for t in tasks if t["status"] == "done"]
        
        print("  ╔══════════════════════════════════════════════════╗")
        print("  ║                    BACKLOG                       ║")
        print("  ╠══════════════════════════════════════════════════╣")
        for i, task in enumerate(backlog, 1):
            print(f"  ║  {i}. {task['text'][:40]:<40}║")
        print("  ╚══════════════════════════════════════════════════╝")
        print()
        print(f"  ✅ Já feitos: {len(done)} tarefas")
        print()
    
    def execute_task(self, task_index):
        tasks = [t for t in self.list_tasks() if t["status"] == "pending"]
        
        if task_index < 1 or task_index > len(tasks):
            print(f"  ❌ Tarefa {task_index} não encontrada")
            return
        
        task = tasks[task_index - 1]
        print()
        print(f"  ▶ Executando: {task['text']}")
        print()
        
        todo = self._get_todo()
        todo = todo.replace(f"- [ ] {task['text']}", f"- [x] {task['text']}")
        self._save_todo(todo)
        
        self._dispatch_to_agent(task["text"])
    
    def _dispatch_to_agent(self, task_text):
        task_lower = task_text.lower()
        
        if "deploy" in task_lower or "vercel" in task_lower:
            print("  → Redirecionando para Agente de Deploy...")
            self._run_deploy_agent()
        elif "carrossel" in task_lower:
            print("  → Redirecionando para Agente de Carrossel...")
            self._run_carrossel_agent()
        elif "transcri" in task_lower:
            print("  → Redirecionando para Agente de Transcrição...")
            self._run_transcription_agent()
        elif "email" in task_lower:
            print("  → Redirecionando para Agente de Email...")
            self._run_email_agent()
        elif "dashboard" in task_lower or "analytics" in task_lower:
            print("  → Redirecionando para Agente de Analytics...")
            self._run_analytics_agent()
        elif "coordenador" in task_lower:
            print("  → Sou eu! Coordenando outros agentes...")
            print("  → Para executar uma tarefa, use: python main.py run <número>")
        else:
            print("  → Tarefa genérica. Executando diretamente...")
            self._execute_generic(task_text)
    
    def _run_deploy_agent(self):
        print("  ═══════════════════════════════════════════════════")
        print("  📦 AGENTE DEPLOY")
        print("  ═══════════════════════════════════════════════════")
        print()
        print("  1. Preparando arquivos para deploy...")
        print("  2. Verificando estrutura do projeto...")
        print("  3. Criando vercel.json...")
        
        vercel_config = {
            "buildCommand": "",
            "installCommand": "",
            "devCommand": "",
            "routes": [{"src": "/(.*)", "dest": "/$1"}]
        }
        
        index_html = self.project_root / "index.html"
        hub_html = self.project_root / "hub.html"
        
        if index_html.exists() and hub_html.exists():
            print("  ✅ Arquivos HTML encontrados")
            print()
            print("  📋 Próximos passos:")
            print("  1. Crie o repo no GitHub:")
            print("     → https://github.com/new")
            print(f"     → Nome: opb-sistema")
            print()
            print("  2. No terminal, dentro da pasta:")
            print("     git init")
            print("     git remote add origin https://github.com/cleiton-negreiros/opb-sistema.git")
            print("     git add .")
            print("     git commit -m 'feat: setup inicial'")
            print("     git push -u origin main")
            print()
            print("  3. Deploy no Vercel:")
            print("     → https://vercel.com/new")
            print("     → Importe o repo do GitHub")
            print()
            print("  ⚠️ Nota: Para deploy, o hub.html usa localStorage.")
            print("  Se precisar backend, considere usar Vercel Functions.")
        else:
            print("  ❌ Arquivos não encontrados!")
    
    def _run_carrossel_agent(self):
        print("  ═══════════════════════════════════════════════════")
        print("  🎠 AGENTE CARROSSEL")
        print("  ═══════════════════════════════════════════════════")
        print()
        print("  Este agente transformará posts em estruturas de carrossel.")
        print("  Estrutura planejada:")
        print()
        print("  agents/carousel_generator/main.py")
        print("  - Input: texto do post")
        print("  - Output: estrutura JSON com slides")
        print()
        print("  Exemplo de output:")
        print("  {")
        print("    'slides': [")
        print("      {'title': '...', 'text': '...', 'image_prompt': '...'},")
        print("      ...")
        print("    ]")
        print("  }")
    
    def _run_transcription_agent(self):
        print("  ═══════════════════════════════════════════════════")
        print("  🎙️ AGENTE TRANSCRIÇÃO")
        print("  ═══════════════════════════════════════════════════")
        print()
        print("  Este agente transcreverá áudios/vídeos.")
        print("  Opções:")
        print("  - Whisper (OpenAI) via API")
        print("  - Vosk (offline)")
        print()
        print("  Estrutura planejada:")
        print("  agents/transcription/main.py")
    
    def _run_email_agent(self):
        print("  ═══════════════════════════════════════════════════")
        print("  📧 AGENTE EMAIL")
        print("  ═══════════════════════════════════════════════════")
        print()
        print("  Este agente gerará emails profissionais.")
        print("  Estrutura planejada:")
        print("  agents/email_generator/main.py")
        print("  - Templates Jinja2")
        print("  - Integração SMTP (Gmail/SendGrid)")
    
    def _run_analytics_agent(self):
        print("  ═══════════════════════════════════════════════════")
        print("  📊 AGENTE ANALYTICS")
        print("  ═══════════════════════════════════════════════════")
        print()
        print("  Dashboard de métricas do sistema.")
        print("  - Posts gerados")
        print("  - Tempo economizado")
        print("  - Taxa de conclusão")
    
    def _execute_generic(self, task_text):
        print(f"  Executando: {task_text}")
        print("  → Tarefa genérica ainda não implementada")
    
    def run_interactive(self):
        self.greet()
        self.show_tasks()
        
        print("  Comandos:")
        print("  - run <número>  : Executa tarefa do backlog")
        print("  - list           : Lista tarefas")
        print("  - status         : Mostra status geral")
        print("  - quit           : Sair")
        print()
        
        while True:
            try:
                cmd = input("  > ").strip().lower()
                
                if cmd == "quit" or cmd == "q":
                    print("  👋 Até logo!")
                    break
                elif cmd == "list" or cmd == "l":
                    self.show_tasks()
                elif cmd == "status" or cmd == "s":
                    self._show_status()
                elif cmd.startswith("run "):
                    try:
                        idx = int(cmd.split()[1])
                        self.execute_task(idx)
                    except:
                        print("  ❌ Use: run <número>")
                else:
                    print("  ❓ Comando não reconhecido")
            except KeyboardInterrupt:
                print("\n  👋 Até logo!")
                break
    
    def _show_status(self):
        metrics = self.context.get("goals", {}).get("metricas_acompanhamento", {})
        
        print()
        print("  ╔══════════════════════════════════════════════════╗")
        print("  ║                 STATUS DO SISTEMA                ║")
        print("  ╠══════════════════════════════════════════════════╣")
        print(f"  ║  Posts gerados:     {metrics.get('posts_gerados', 0):<23}║")
        print(f"  ║  Carrosséis:       {metrics.get('carousels_criados', 0):<23}║")
        print(f"  ║  Emails enviados:  {metrics.get('emails_enviados', 0):<23}║")
        print(f"  ║  Tempo economizado: {metrics.get('tempo_economizado_semanal', 0):<22}h║")
        print("  ╚══════════════════════════════════════════════════╝")
        print()


def main():
    coordinator = CoordinatorAgent()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            coordinator.show_tasks()
        elif sys.argv[1] == "status":
            coordinator._show_status()
        elif sys.argv[1] == "run" and len(sys.argv) > 2:
            try:
                coordinator.execute_task(int(sys.argv[2]))
            except:
                print("Uso: python main.py run <número>")
        else:
            coordinator.run_interactive()
    else:
        coordinator.run_interactive()


if __name__ == "__main__":
    main()
