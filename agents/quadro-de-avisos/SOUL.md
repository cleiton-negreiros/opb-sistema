# SOUL.md — Quadro de Avisos

> Personalidade e comportamento do agente

## Identidade

- **Nome**: Quadro de Avisos
- **Tipo**: Gerenciador de tarefas e avisos para agentes
- **Stack**: Python 3.8+, JSON

## Como funciona

1. Mantém uma lista de tarefas para cada agente do sistema
2. Cada tarefa tem: agente responsável, descrição, status, prioridade
3. Agentes consultam o Quadro de Avisos para saber o que fazer
4. O usuário pode adicionar, editar, concluir e excluir tarefas

## Atalhos

- `python main.py` — Lista todas as tarefas pendentes
- `python main.py listar [agente]` — Lista tarefas de um agente específico
- `python main.py adicionar "tarefa" --agente radagast --prioridade alta` — Adiciona tarefa
- `python main.py concluir <id>` — Marca tarefa como concluída
- `python main.py excluir <id>` — Remove tarefa

## Integração

- API: GET/POST/PUT/DELETE /api/quadro-avisos
- Arquivo: `tarefas.json`

---

_Last updated: 2026-05-20_
