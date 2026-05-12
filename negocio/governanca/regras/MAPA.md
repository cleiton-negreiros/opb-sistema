---
name: "MAPA — Regras"
description: "Índice das regras-mãe consolidadas de trabalho com IA"
tipo: referencia
---

# Regras — Mapa

> Regras-mãe que governam como a IA te trata e como responde. Cada arquivo é 1 tema único; sub-regras numeradas dentro.

## Regras já incluídas no template

| Arquivo | Tema |
|---|---|
| [`ordem-de-leitura.md`](ordem-de-leitura.md) | Sequência oficial de leitura. O que abrir primeiro, o que abrir só quando precisar. |
| [`integridade-dados.md`](integridade-dados.md) | Zero invenção, zero suposição, dados reais sempre, confiança calibrada. |
| [`ritmo-sessao.md`](ritmo-sessao.md) | Uma tarefa de cada vez, propor próximos passos, salvar progresso, não esquecer. |
| [`cerebro-manutencao.md`](cerebro-manutencao.md) | Atualizar o cérebro ao fim de sessão sem você precisar pedir. |
| [`linguagem-escrita.md`](linguagem-escrita.md) | Como a IA deve escrever pra você ler (português, frases curtas, sem jargão cru). |

## Tabela de decisão (quando criar regra nova)

| Quando precisar decidir sobre... | Abra ou crie... |
|---|---|
| Como tratar fatos | `integridade-dados.md` |
| Como escrever texto pra você ler | `linguagem-escrita.md` |
| Como escrever copy na sua voz pra clientes | `tom-voz-copy.md` (criar) |
| Ritmo da sessão | `ritmo-sessao.md` |
| Atualizar o cérebro ao fim de sessões | `cerebro-manutencao.md` |
| Ambiente técnico (versões, dependências) | `ambiente-tecnico.md` (criar) |
| Processo de execução | `processo-execucao.md` (criar) |

## Padrão de cada arquivo

```markdown
---
name: "Regra — [tema]"
description: "[1 linha]"
---

# [Tema]

## Regra-mãe
[Princípio em 1 frase]

## Sub-regras

### D-01 — [Nome]
**Adicionada:** AAAA-MM-DD
**Motivo:** [Incidente ou pedido que originou]
**Como aplicar:** [Quando dispara]
```

## Como adicionar regra nova

1. Crie o arquivo seguindo o padrão acima.
2. Volte aqui e adicione a linha na tabela "Regras já incluídas".
3. Commit no Git ao fim da sessão.

A IA pode fazer os 3 passos pra você se você disser "salva isso como regra X".
