#!/usr/bin/env python3
"""
📋 Quadro de Avisos — OPB Sistema
Gerencia tarefas e avisos para os agentes.
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

DATA_PATH = Path(__file__).parent / "tarefas.json"


def carregar():
    if not DATA_PATH.exists():
        return {"tarefas": []}
    return json.loads(DATA_PATH.read_text(encoding='utf-8'))


def salvar(data):
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def proximo_id(tarefas):
    if not tarefas:
        return 1
    return max(t["id"] for t in tarefas) + 1


def adicionar(descricao, agente="geral", prioridade="media"):
    data = carregar()
    tarefa = {
        "id": proximo_id(data["tarefas"]),
        "agente": agente,
        "tarefa": descricao,
        "status": "pendente",
        "prioridade": prioridade,
        "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "concluido_em": None
    }
    data["tarefas"].append(tarefa)
    salvar(data)
    return tarefa


def listar(agente=None):
    data = carregar()
    tarefas = data["tarefas"]
    if agente:
        tarefas = [t for t in tarefas if t["agente"] == agente]
    return sorted(tarefas, key=lambda t: {"alta": 0, "media": 1, "baixa": 2}.get(t["prioridade"], 1))


def concluir(tarefa_id):
    data = carregar()
    for t in data["tarefas"]:
        if t["id"] == tarefa_id:
            t["status"] = "concluido"
            t["concluido_em"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            salvar(data)
            return t
    return None


def excluir(tarefa_id):
    data = carregar()
    antes = len(data["tarefas"])
    data["tarefas"] = [t for t in data["tarefas"] if t["id"] != tarefa_id]
    if len(data["tarefas"]) < antes:
        salvar(data)
        return True
    return False


def formatar_tarefa(t):
    prioridade_icone = {"alta": "🔴", "media": "🟡", "baixa": "🟢"}
    status_icone = "✅" if t["status"] == "concluido" else "📌"
    p = prioridade_icone.get(t["prioridade"], "🟡")
    return f"{status_icone} [{p}] #{t['id']} ({t['agente']}) {t['tarefa']}"


def main():
    if len(sys.argv) < 2:
        print("📋 Quadro de Avisos — OPB Sistema\n")
        print("USO:")
        print("  python main.py                          — Lista todas as pendentes")
        print("  python main.py listar [agente]          — Lista tarefas de um agente")
        print('  python main.py adicionar "tarefa" [--agente nome] [--prioridade alta|media|baixa]')
        print("  python main.py concluir <id>            — Conclui tarefa")
        print("  python main.py excluir <id>             — Exclui tarefa")
        print("  python main.py agentes                  — Lista agentes com tarefas\n")
        return

    cmd = sys.argv[1]

    if cmd == "listar":
        agente = sys.argv[2] if len(sys.argv) > 2 else None
        tarefas = listar(agente)
        pendentes = [t for t in tarefas if t["status"] == "pendente"]
        concluidas = [t for t in tarefas if t["status"] == "concluido"]
        print(f"\n📋 Quadro de Avisos{f' — {agente}' if agente else ''}")
        print(f"   Pendentes: {len(pendentes)} | Concluídas: {len(concluidas)}\n")
        if pendentes:
            print("PENDENTES:")
            for t in pendentes:
                print(f"  {formatar_tarefa(t)}")
        if concluidas:
            print(f"\nCONCLUÍDAS:")
            for t in concluidas:
                print(f"  {formatar_tarefa(t)}")
        print()

    elif cmd == "adicionar" and len(sys.argv) >= 3:
        descricao = sys.argv[2]
        agente = "geral"
        prioridade = "media"
        if "--agente" in sys.argv:
            i = sys.argv.index("--agente")
            if i + 1 < len(sys.argv):
                agente = sys.argv[i + 1]
        if "--prioridade" in sys.argv:
            i = sys.argv.index("--prioridade")
            if i + 1 < len(sys.argv):
                prioridade = sys.argv[i + 1]
        t = adicionar(descricao, agente, prioridade)
        print(f"✅ Tarefa #{t['id']} adicionada para {agente}")

    elif cmd == "concluir" and len(sys.argv) >= 3:
        t = concluir(int(sys.argv[2]))
        if t:
            print(f"✅ Tarefa #{t['id']} concluída: {t['tarefa']}")
        else:
            print("❌ Tarefa não encontrada")

    elif cmd == "excluir" and len(sys.argv) >= 3:
        if excluir(int(sys.argv[2])):
            print("🗑️ Tarefa excluída")
        else:
            print("❌ Tarefa não encontrada")

    elif cmd == "agentes":
        tarefas = listar()
        agentes = {}
        for t in tarefas:
            a = t["agente"]
            if a not in agentes:
                agentes[a] = {"pendentes": 0, "concluidas": 0}
            agentes[a]["pendentes" if t["status"] == "pendente" else "concluidas"] += 1
        print("\n📋 Agentes com tarefas:\n")
        for a, c in sorted(agentes.items()):
            print(f"  {a}: {c['pendentes']} pendentes, {c['concluidas']} concluídas")
        print()

    else:
        # Default: listar pendentes
        tarefas = listar()
        pendentes = [t for t in tarefas if t["status"] == "pendente"]
        print(f"\n📋 Quadro de Avisos — {len(pendentes)} pendentes\n")
        for t in pendentes:
            print(f"  {formatar_tarefa(t)}")
        print()


if __name__ == "__main__":
    main()
