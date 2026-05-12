---
name: "Permissões — Acesso por agente"
description: "Quem pode ler e escrever onde no cérebro"
---

# Permissões

| Agente | Pode ler | Pode escrever |
|--------|----------|---------------|
| _Vazio_ | | |

## Padrão sugerido

- Todo agente lê `negocio/governanca/regras/`
- Nenhum agente escreve em `pessoal/` por padrão
- Agente só escreve na própria pasta `agentes/<nome>/STATUS.md` e em pastas declaradas explicitamente acima
