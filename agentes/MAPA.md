---
name: "Agentes — Mapa"
description: "Índice de configuração dos agentes IA"
---

# Agentes — Mapa

> Cada agente do seu ecossistema tem uma pasta aqui com personalidade, regras operacionais e estado atual.

## Estrutura padrão por agente

```
agentes/<nome-do-agente>/
├── SOUL.md      ← Personalidade, propósito, tom de voz
├── AGENTS.md    ← Regras operacionais, escopos de acesso, fluxos
└── STATUS.md    ← Estado atual, última execução, métricas
```

## Agentes ativos

| # | Nome | Função | Tipo |
|---|------|--------|------|
| _Vazio. Crie seu primeiro agente em uma subpasta._ |

## Como criar um agente novo

1. Crie a pasta `agentes/<nome>/`
2. Copie os 3 templates de `_templates/`
3. Preencha SOUL primeiro (quem é o agente)
4. AGENTS depois (o que ele pode e não pode fazer)
5. STATUS começa vazio, vai sendo escrito pela operação
6. Adicione ele na tabela acima
