#!/usr/bin/env python3
"""
Agente Coordenador OPB — Orquestracao Diaria de Agentes

Uso:
    python main.py                          → Status do sistema
    python main.py morning                  → Ciclo matinal completo
    python main.py run [agente] [args]      → Executar agente especifico
    python main.py orchestrate              → Sugerir sequencia de agentes
    python main.py list                     → Listar agentes disponiveis
"""

import os
import sys
import subprocess
import json
from datetime import datetime, date
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

PROJECT = Path(__file__).parent.parent.parent


class Coordinator:
    def __init__(self):
        self.agents_dir = PROJECT / "agents"
        self.negocio_dir = PROJECT / "negocio"
        self.output_dir = PROJECT / "output"
        self.log = []

    # --------------------------------------------------------
    # CONTEXTO
    # --------------------------------------------------------
    def load_brain_context(self) -> dict:
        ctx = {}
        quem_sou = self.negocio_dir / "governanca" / "quem-sou.md"
        if quem_sou.exists():
            text = quem_sou.read_text(encoding='utf-8')
            ctx["quem_sou"] = True
            ctx["nome"] = self._extract(text, r"## Identidade\n\n\*\*Nome\*\*:\s*(.+)")
            ctx["missao"] = self._extract(text, r"## Miss[ãa]o\n\n(.+)")
        projetos = self.negocio_dir / "projetos" / "ativos.md"
        if projetos.exists():
            ctx["projetos"] = projetos.read_text(encoding='utf-8')[:500]
        return ctx

    def _extract(self, text: str, pattern: str) -> str:
        import re
        m = re.search(pattern, text)
        return m.group(1).strip() if m else ""

    # --------------------------------------------------------
    # AGENTES
    # --------------------------------------------------------
    def list_agents(self) -> list:
        agents = []
        for d in sorted(self.agents_dir.iterdir()):
            if d.is_dir() and (d / "main.py").exists():
                soul = d / "SOUL.md"
                nome = d.name
                desc = ""
                if soul.exists():
                    for line in soul.read_text(encoding='utf-8').split('\n'):
                        if "**Nome**:" in line:
                            nome = line.split("**Nome**:")[-1].strip()
                        if "**Tipo**:" in line:
                            desc = line.split("**Tipo**:")[-1].strip()
                agents.append({"pasta": d.name, "nome": nome, "desc": desc})
        return agents

    def run_agent(self, agent_name: str, args: list = None) -> dict:
        agent_path = self.agents_dir / agent_name / "main.py"
        if not agent_path.exists():
            return {"ok": False, "error": f"Agente nao encontrado: {agent_name}"}
        cmd = [sys.executable, str(agent_path)]
        if args:
            cmd.extend(args)
        print(f"[coordinator] Executando: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=agent_path.parent)
            out = result.stdout[-1500:] if result.stdout else ""
            err = result.stderr[-500:] if result.stderr else ""
            self.log.append({"agente": agent_name, "ok": result.returncode == 0, "ts": datetime.now().isoformat()})
            return {"ok": result.returncode == 0, "stdout": out, "stderr": err}
        except subprocess.TimeoutExpired:
            self.log.append({"agente": agent_name, "ok": False, "error": "timeout"})
            return {"ok": False, "error": "timeout"}
        except Exception as e:
            self.log.append({"agente": agent_name, "ok": False, "error": str(e)})
            return {"ok": False, "error": str(e)}

    # --------------------------------------------------------
    # CICLO MATINAL
    # --------------------------------------------------------
    def morning_coordination(self):
        """Ciclo matinal completo: auditoria → insight → acao."""
        print("=" * 60)
        print(f"  CICLO MATINAL - OPB Sistema")
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("=" * 60)

        # Step 1: Audit
        print("\n[1/5] Auditoria de codigo...")
        audit_r = subprocess.run(
            [sys.executable, str(PROJECT / "audit" / "auditoria_diaria.py"), "--quick"],
            capture_output=True, text=True, timeout=30
        )
        if audit_r.returncode == 0:
            print("  OK - Auditoria passou")
        else:
            print(f"  Atencao - Auditoria com problemas:\n{audit_r.stdout[-300:]}")

        # Step 2: List agents
        print("\n[2/5] Verificando agentes...")
        agents = self.list_agents()
        for a in agents:
            print(f"  + {a['pasta']}")
        print(f"  Total: {len(agents)} agentes disponiveis")

        # Step 3: Context review via consultor
        print("\n[3/5] Insight diario (consultor-negocios)...")
        consultor_r = self.run_agent("consultor-negocios", ["insight_diario"])
        if consultor_r["ok"]:
            out = consultor_r.get("stdout", "")
            # Extract just the key lines
            for line in out.split('\n'):
                if line.strip().startswith("## Insight") or line.strip().startswith("## Acao"):
                    print(f"  {line.strip()}")
        print(f"  Detalhes salvos em output/consultoria/")

        # Step 4: Check brain health
        print("\n[4/5] Saude do cerebro...")
        ctx = self.load_brain_context()
        indicators = []
        if ctx.get("quem_sou"): indicators.append("+ Identidade carregada")
        if ctx.get("missao"): indicators.append("+ Missao definida")
        if ctx.get("projetos"): indicators.append("+ Projetos ativos")
        for ind in indicators:
            print(f"  {ind}")
        print(f"  Indicadores: {len(indicators)}/3")

        # Step 5: Suggest next steps
        print("\n[5/5] Proximos passos sugeridos:")
        print("""
  1. Execute agentes de conteudo: python agents/coordinator/main.py run text_generator
  2. Capture ideias: /ideia [texto] no Telegram
  3. Processe conteudo: python agents/coordinator/main.py run consumo
  4. Faca curadoria: python agents/coordinator/main.py run radagast
""")

        # Save coordination log
        log_dir = PROJECT / "output" / "coordenacao"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / f"morning_{date.today().isoformat()}.json"
        log_path.write_text(json.dumps({
            "data": date.today().isoformat(),
            "agentes": [a["pasta"] for a in agents],
            "log": self.log,
            "status": "concluido"
        }, indent=2, ensure_ascii=False), encoding='utf-8')

        print(f"\n  Log salvo em: {log_path}")
        print("=" * 60)

    def orchestrate(self):
        """Usa o consultor para sugerir sequencia otimizada de agentes."""
        print("[coordinator] Solicitando sugestao de orquestracao...")
        result = self.run_agent("consultor-negocios", ["coordenacao_agentes"])
        if result["ok"]:
            print(result.get("stdout", ""))
        else:
            print(f"Erro: {result.get('error', 'desconhecido')}")

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------
    def show_status(self):
        ctx = self.load_brain_context()
        agents = self.list_agents()
        print("=" * 60)
        print("  COORDENADOR - OPB SISTEMA")
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("=" * 60)
        print(f"\n  Nome: {ctx.get('nome', 'Nao definido')}")
        print(f"  Missao: {ctx.get('missao', 'Nao definida')[:60]}...")

        print(f"\n  Agentes ({len(agents)}):")
        for a in agents:
            print(f"    {a['pasta']:25s} {a['desc'][:40]}")

        # Check last coordination
        log_dir = PROJECT / "output" / "coordenacao"
        if log_dir.exists():
            logs = sorted(log_dir.glob("morning_*.json"), reverse=True)
            if logs:
                last = json.loads(logs[0].read_text(encoding='utf-8'))
                print(f"\n  Ultima coordenacao: {last.get('data', 'N/A')}")
                print(f"  Agentes executados: {len(last.get('log', []))}")

        print("\n" + "=" * 60)


def main():
    coord = Coordinator()

    if len(sys.argv) < 2:
        coord.show_status()
        print("""
Uso:
  python main.py                   → Status
  python main.py morning           → Ciclo matinal completo
  python main.py orchestrate       → Sugerir sequencia de agentes
  python main.py list              → Listar agentes
  python main.py run [agente]      → Executar agente
  python main.py run [agente] args → Executar com argumentos
""")
        return

    cmd = sys.argv[1]

    if cmd == "morning":
        coord.morning_coordination()
    elif cmd == "orchestrate":
        coord.orchestrate()
    elif cmd == "list":
        agents = coord.list_agents()
        for a in agents:
            print(f"  {a['pasta']:25s} {a['desc'][:50]}")
        print(f"\n  Total: {len(agents)} agentes")
    elif cmd == "run" and len(sys.argv) > 2:
        agent = sys.argv[2]
        args = sys.argv[3:] if len(sys.argv) > 3 else []
        result = coord.run_agent(agent, args)
        if result["ok"]:
            out = result.get("stdout", "")
            if out:
                print(out)
        else:
            print(f"Erro: {result.get('error', 'desconhecido')}")
    else:
        print(f"Comando desconhecido: {cmd}")
        print("Use: morning | orchestrate | list | run [agente]")


if __name__ == "__main__":
    main()
