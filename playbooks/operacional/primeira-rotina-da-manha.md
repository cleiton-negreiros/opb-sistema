---
name: "Primeira rotina da manhã"
description: "Exemplo de playbook executável — IA lê projetos ativos e te reporta status em 1 mensagem"
tipo: playbook
---

# Primeira rotina da manhã

> Este é um playbook de exemplo. Serve como template pra você criar os seus. A ideia: você fala "roda a rotina da manhã" pra IA e ela executa o procedimento abaixo sem precisar lembrar dos passos.

## Quando rodar

Toda manhã antes de começar a trabalhar, ou quando você sentar pra retomar depois de uma pausa longa.

## O que a IA faz quando você fala "roda a rotina da manhã"

1. **Lê** `negocio/projetos/ativos.md` e lista os projetos em curso.
2. **Pra cada projeto**, abre a pasta dele em `negocio/projetos/<slug>/` se existir, e identifica o "próximo passo" mais recente.
3. **Verifica** `negocio/governanca/decisoes/AAAA-MM.md` (mês corrente) pra ver se há decisão pendente sem ação atribuída.
4. **Reporta** numa única mensagem, formato:

```
Bom dia. Status hoje:

Em curso (3 projetos):
  - Projeto A — próximo passo: <ação>
  - Projeto B — próximo passo: <ação>
  - Projeto C — próximo passo: <ação>

Decisões abertas:
  - <decisão sem dono>

Sugestão de foco hoje: <1 escolha>. Confirma?
```

5. **Espera você confirmar** o foco antes de mexer em qualquer coisa.

## Por que existe

Você não precisa lembrar do que estava fazendo ontem. A IA monta o briefing pra você. Reduz o atrito de "abrir o dia" e evita que projetos pequenos sumam de vista.

## Como criar o seu

Copie este arquivo, renomeie pra `<sua-rotina>.md`, e troque os passos. Padrão:

- **Quando rodar** (gatilho)
- **O que a IA faz** (passos numerados)
- **O que você confirma no fim** (handoff)

Adicione o playbook novo à tabela em `playbooks/MAPA.md`.
