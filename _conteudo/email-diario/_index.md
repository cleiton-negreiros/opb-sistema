---
created: 2026-06-10
modified: 2026-06-10
tags: email/navegacao
---

# 📧 Emails Diários

> [[_home.md|🏠 Home]] → [[_conteudo/_index.md|🎬 Conteúdo]] → Email Diário

Textos originais escritos no celular. Cada um vira [[_conteudo/carrossel/_index.md|🎠 carrossel]] + [[_conteudo/reels/_index.md|📱 reels]] + [[_conteudo/video/_index.md|🎬 vídeo]].

---

## ✏️ Criar Novo

Use o template [[_templates/email-diario.md]]:

```
Ctrl+N → escolha "email-diario" → preencha → salve aqui
```

Depois:
1. Sincronize (`opb-sync` no Termux)
2. Rode o pipeline (`pipeline-conteudo.bat` no PC)
3. Resultados em [[_conteudo/carrossel/_index.md|🎠]] [[_conteudo/reels/_index.md|📱]] [[_conteudo/video/_index.md|🎬]]

---

## 📋 Últimos Emails

```dataview
table tema as "Tema", pilar as "Pilar", date as "Data"
from "_conteudo/email-diario"
sort date desc
limit 10
```

---

_[[_home.md|🏠 Home]] • [[_conteudo/_index.md|🎬 Conteúdo]] • [[_conteudo/email-diario/_index.md|📧 Emails]]_
