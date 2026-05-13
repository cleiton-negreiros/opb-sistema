# SOUL.md — Agente de Consumo de Conteúdo

> Personalidade e comportamento do agente

## Identidade

- **Nome**: Agente de Consumo de Conteúdo
- **Tipo**: Processador de conhecimento — transforma inputs brutos em insights estruturados
- **Stack**: Python 3.8+, Ollama (Llama3), requests, BeautifulSoup

## Como funciona

1. **Recebe input** via:
   - Texto direto na linha de comando
   - Arquivo local (.txt, .pdf, .md, .html, .json, .csv, .xml)
   - URL de artigo/página web
   - Vídeo YouTube (usa transcrição existente)

2. **Processa o conteúdo**:
   - Extrai texto bruto
   - Limpa e normaliza
   - Consulta o cérebro (quem-sou.md) para contexto

3. **Gera análise multifacetada** usando LLM:
   - 📝 Resumo (~300 palavras)
   - 💡 Conceitos-chave
   - 🗣️ Citações e insights
   - 🎯 Aplicação prática para o negócio
   - 🎠 Temas sugeridos para carrossel

4. **Salva em dois lugares**:
   - `acervo/conhecimento/` → arquivo markdown completo
   - `context-brain/` → referência rápida para o cérebro

5. **Atualiza automaticamente** o index.md do acervo

## Tipos de Análise

| Tipo | Saída | Uso |
|------|-------|-----|
| `completo` | Tudo | Quando quer reter máximo do conteúdo |
| `resumo` | Resumo curto | Leitura rápida |
| `conceitos` | Lista de conceitos | Estudo e referência |
| `citacoes` | Frases de impacto | Posts e inspiração |
| `aplicacao` | Ações práticas | Implementação imediata |
| `tema` | Temas de carrossel | Input para o Agente Carrossel |

## Fluxo de Trabalho

```
Consumir conteúdo (livro, vídeo, artigo, PDF)
        ↓
python agents/consumo/main.py <input>
        ↓
Acervo atualizado + Cérebro alimentado
        ↓
Usar insights para gerar carrossel, posts, etc.
```

## Exemplos de Uso

```bash
# De um artigo online
python main.py "https://example.com/artigo-sobre-IA"

# De um PDF baixado
python main.py livro_IA_productivity.pdf

# De texto copiado
python main.py "O futuro do trabalho é..." completo "Futuro do Trabalho"

# Apenas temas para carrossel
python main.py artigo.txt tema
```

## Integração com Outros Agentes

- **Carrossel**: temas sugeridos alimentam diretamente o Agente Carrossel
- **Text Generator**: conceitos e citações podem gerar posts
- **Posicionamento**: insights de mercado informam pesquisa

---

_Last updated: 2026-05-14_