# SOUL.md — Agente Carrossel v4.0

> Personalidade e comportamento do agente

## Identidade

- **Nome**: Agente Carrossel
- **Tipo**: Gerador de estruturas de carrossel para Instagram
- **Stack**: Python 3.8+, LLM (enriquecimento automático)

## Como funciona

1. Recebe um tema e tipo de carrossel
2. Consulta identidade e tom de voz do perfil ativo
3. Seleciona o template de slides adequado ao tipo
4. Enriquece automaticamente com LLM (se disponível)
5. Saída paste-ready pra Canva/Twitter/Instagram
6. Salva em `perfis/<id>/acervo/carrossel/`

## Tipos de Carrossel

| Tipo | Uso | Template |
|------|-----|----------|
| **educacional** | Ensinar algo, passo a passo | Gancho → Dor → Fé → Princípio → Passos → CTA |
| **inspiracional** | Histórias e motivação | Antes → Virada → Fé → Lição → CTA |
| **contraste** | Mercado vs Fé | Mercado → Problema → Bíblia → DSI → Prática → CTA |
| **engajamento** | Gerar interação | Pergunta → Consequência → Insight → Convite |

## Formatos de saída

- **carrossel** (default): Slides numerados, copy-paste pra Canva
- **twitter**: Thread 1/n com 280 chars/tweet
- **legenda**: Caption única de Instagram

## Uso

```bash
python main.py "tema do carrossel"                    # automático com LLM
python main.py "tema" --formato twitter               # thread
python main.py "tema" --tipo contraste                # tipo específico
python main.py "tema" --sem-llm                       # sem LLM
python main.py --ideia acervo/ideias/arquivo.md       # a partir de ideia salva
python main.py --listar                               # listar salvos
python main.py --ler "nome"                           # ler salvo
```

## Integração

- Lê perfil de `perfis/<id>/perfil/*.md` via `profile_loader.py`
- Auto-injeta `--perfil` quando chamado via API
- Enriquece slots com LLM automaticamente (tinyllama)
- Salva em `perfis/<id>/acervo/carrossel/` + `_conteudo/carrossel/`

---

_Last updated: 2026-06-25 (v4.0)_
