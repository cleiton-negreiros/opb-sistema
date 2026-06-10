---
created: 2026-06-10
modified: 2026-06-10
tags: email/navegacao
---

# 📧 Emails Diários

Seus textos originais escritos no celular. Cada arquivo vira 4 formatos de conteúdo.

## Template
Use [[_templates/email-diario.md]] para criar um novo email.

## Como usar
1. `Ctrl+N` → escolha `email-diario`
2. Preencha: tema, versículo, reflexão, aplicação
3. Salve nesta pasta
4. Sincronize (`opb-sync` no Termux)
5. Rode o pipeline (`pipeline-conteudo.bat`)

## Emails Recentes

```dataview
table tema as "Tema", pilar as "Pilar", date as "Data"
from "_conteudo/email-diario"
sort date desc
limit 10
```
