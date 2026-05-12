---
name: "Manutenção do cérebro"
description: "Quando e como atualizar o cérebro ao final de sessões — decisões, lições, regras"
tipo: regra
---

# Manutenção do cérebro

> Cérebro estático morre rápido. O que faz o cérebro ficar vivo é a IA escrever de volta nele depois de cada sessão importante.

## Regra-mãe

Ao final de sessões relevantes, a IA atualiza o cérebro **sem esperar você pedir**. Decisões, lições, regras novas e mudanças de funcionamento precisam ser registradas durante a sessão, antes de fechar.

## Sub-regras

### D-01 — Atualização ao fim de cada sessão relevante

Antes de encerrar, a IA verifica se houve:

- **Decisão estratégica** ("vamos usar plataforma X em vez de Y"). Vai pra `negocio/governanca/decisoes/AAAA-MM.md`.
- **Lição aprendida** (algo deu errado e você não quer repetir). Vai pra `negocio/governanca/licoes/AAAA-MM.md`.
- **Regra nova** (você corrigiu a IA: "nunca faça X"). Vai pra `negocio/governanca/regras/<tema>.md` como sub-regra D-XX.
- **Sistema externo descoberto** (uma API nova, uma plataforma nova). Vai pra `negocio/governanca/referencias/`.
- **Mudança em projeto ativo** (concluiu, pausou, mudou prioridade). Atualiza `negocio/projetos/ativos.md`.

**Não esperar você pedir.** Antes de encerrar, perguntar: "atualizo o cérebro com X, Y e Z?". Listar o que vai escrever, deixar você revisar, escrever, salvar.

### D-02 — Padrão de cada arquivo

Toda regra/decisão/lição segue o mesmo formato:

```markdown
---
name: "Título curto"
description: "1 linha sobre por que esse arquivo existe"
tipo: regra | decisao | licao | referencia
---

# Título

> Frase única que captura a essência.

## Regra-mãe (ou Decisão / Lição)

Parágrafo único que resume.

## Sub-regras (ou Detalhes)

### D-01 — [Nome curto]
Por quê. Como aplicar.

### D-02 — ...
```

### D-03 — Atualizar o MAPA quando criar arquivo

Toda vez que criar arquivo novo, **atualizar o `MAPA.md` da pasta** apontando pra ele. Sem entrada no mapa, o arquivo é fantasma — a IA pode até achar, mas a chance de usar é menor.

### D-04 — Commit no fim de sessão

Se o cérebro está em Git (e está, por padrão), fazer `git add . && git commit -m "sessao: <resumo>"` ao fim de cada sessão. Histórico de commits = histórico de decisões. Se você precisar voltar atrás algum dia, está tudo lá.
