---
name: "Playbooks — Mapa"
description: "Manuais executáveis transversais"
---

# Playbooks — Mapa

> Manuais executáveis. Cada playbook é um procedimento que qualquer agente (ou você) pode rodar.

## Categorias

| Pasta | Para quê |
|-------|----------|
| `operacional/` | Operação de sistemas (deploy, restart, troubleshooting, rotinas diárias) |
| `seguranca/` | Rotação de credenciais, hardening, resposta a incidente |
| `loop-aprendiz/` | Templates de aprendizado contínuo dos agentes |

## Playbooks já incluídos no template

| Arquivo | Para quê |
|---|---|
| [`operacional/primeira-rotina-da-manha.md`](operacional/primeira-rotina-da-manha.md) | Exemplo: IA lê projetos ativos e te reporta status em 1 mensagem. Sirva-se como base. |

## Como criar playbook novo

1. Escolha a categoria (`operacional/`, `seguranca/` ou `loop-aprendiz/`).
2. Crie o arquivo `.md` com 3 seções: **Quando rodar**, **O que a IA faz** (passos numerados), **O que você confirma no fim**.
3. Adicione na tabela acima.
4. Pra rodar: fale com a IA "roda o playbook X" — ela abre o arquivo e executa.
