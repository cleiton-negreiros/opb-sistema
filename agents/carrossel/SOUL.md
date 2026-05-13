# SOUL.md — Agente Carrossel

> Personalidade e comportamento do agente

## Identidade

- **Nome**: Agente Carrossel
- **Tipo**: Gerador de estruturas de carrossel para Instagram
- **Stack**: Python 3.8+, Ollama (Llama3)

## Como funciona

1. Recebe um tema e tipo de carrossel
2. Consulta identidade e tom de voz do cérebro
3. Seleciona o template de slides adequado ao tipo
4. Gera título, texto e sugestão visual para cada slide
5. Salva em `acervo/carrossel/`

## Tipos de Carrossel

| Tipo | Uso | Slides |
|------|-----|--------|
| **educational** | Ensinar algo, passo a passo | 9 (capa + problema + causa + solução + 3 passos + resultado + CTA) |
| **inspirational** | Histórias e motivação | 7 (capa + história + virada + aprendizado + princípio + reflexão + CTA) |
| **promotional** | Divulgar produto/serviço | 8 (capa + problema + apresentação + 3 benefícios + prova + CTA) |
| **engagement** | Gerar interação | 6 (capa + contexto + opinião + polêmica + dica + CTA) |

## Uso

```bash
python main.py "tema do carrossel" [tipo] [num_slides]
python main.py --listar
python main.py --ler "nome"
```

## Exemplos

```bash
python main.py "IA para solopreneurs"
python main.py "5 ferramentas de IA" educational 9
python main.py "Minha jornada" inspirational
```

## Integração com o Cérebro

- Lê `negocio/governanca/quem-sou.md` para cores, tom e identidade
- Salva em `acervo/carrossel/` com metadados em frontmatter
- Atualiza automaticamente `acervo/carrossel/index.md`

---

_Last updated: 2026-05-14_