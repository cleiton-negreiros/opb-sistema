# 📋 Quadro de Avisos — Agente de Gestão de Tarefas

## Identidade
- **Nome:** Quadro de Avisos
- **Tipo:** Agente de gestão de tarefas e pendências
- **Tom:** Organizado, prático, direto
- **Público:** Empreendedor solo que precisa gerenciar tarefas diárias

## Propósito
Gerenciar tarefas do projeto OPB Sistema, permitindo criar, listar, concluir e excluir tarefas com prioridades e agentes responsáveis.

## Como Funciona
1. Recebe comandos: listar, adicionar, concluir, excluir
2. Salva tarefas em arquivo JSON
3. Mantém histórico de tarefas concluídas
4. Filtra por agente responsável e prioridade

## Comandos
```bash
python main.py listar                    # Lista todas as tarefas
python main.py listar --agente carrossel # Filtra por agente
python main.py adicionar "Criar carrossel sobre dízimo"
python main.py adicionar "Tarefa" --agente carrossel --prioridade alta
python main.py concluir 1                # Conclui tarefa pelo ID
python main.py excluir 1                 # Exclui tarefa pelo ID
```

## Prioridades
| Prioridade | Cor | Uso |
|------------|-----|-----|
| Alta | 🔴 | Urgente, prazo curto |
| Média | 🟡 | Importante, sem urgência |
| Baixa | 🟢 | Nice-to-have, sem prazo |

## Estrutura da Tarefa
```json
{
  "id": 1,
  "tarefa": "Descrição da tarefa",
  "agente": "carrossel",
  "prioridade": "alta",
  "status": "pendente",
  "criado_em": "2026-05-21 10:30",
  "concluido_em": null
}
```

## Integrações
- **Telegram Bot:** `/tarefas`, `/tarefa`, `/concluir`
- **API:** `/api/quadro-avisos` endpoints
- **Plataforma Web:** Widget no dashboard

---

*Última atualização: 2026-05-21*
