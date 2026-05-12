---
name: "Agente Designer"
description: "Designer gráfico especialista: diagramas, thumbnails, social media, mockups"
tipo: agente
updated_at: 2026-05-12
---

# Agente Designer

> Assistente de design gráfico que cria peças visuais com identidade de marca consistente

## Capacidades

- **Diagramas de acorde**: Gera SVG do braço do violão para qualquer acorde popular
- **Briefings criativos**: Conceito, composição, paleta, tipografia, cópia
- **Paletas de cor**: Gera paletas harmoniosas com justificativa emocional
- **Mockups HTML/CSS**: Protótipos visuais responsivos

## Uso

```bash
cd agents/designer
python main.py briefing "tema" --tipo post
python main.py acorde "Am"
python main.py paleta "elegante minimalista"
```

## Saída

- `acervo/designs/briefings/`
- `acervo/designs/diagramas/`
- `acervo/designs/mockups/`

## Dependências

- Ollama (Llama3) para geração de texto criativo
- Python padrão (sem dep externa, usa SVG inline)