---
name: "Regra — Ambiente Técnico"
description: "Configuração do ambiente de desenvolvimento e LLM"
---

# Ambiente Técnico

## Regra-mãe
O provedor LLM padrão do sistema é o **Ollama** com modelo **tinyllama**. Todo agente deve usar `utils/llm_provider.py` via `generate_text()`.

## Sub-regras

### D-01 — Provedor LLM
**Adicionada:** 2026-05-22
**Motivo:** Definição após análise comparativa com LM Studio
**Como aplicar:** Sempre usar `generate_text()` do `utils/llm_provider.py`. Não chamar Ollama diretamente. Configurações via `.env`:
- `OLLAMA_BASE_URL=http://localhost:11434`
- `OLLAMA_MODEL=tinyllama`

### D-02 — Hardware conhecido
**Adicionada:** 2026-05-22
**Motivo:** Consistentemente lento, ajuda a calibrar expectativas
**Especificação:** Intel Core i5-2400, 8GB RAM, Intel HD Graphics 3000, Windows
**Limitação conhecida:** ~2-3 tok/s com tinyllama. Timeout de 180s configurado.

### D-03 — Fallback sem LLM
**Adicionada:** 2026-05-22
**Motivo:** Ollama pode falhar por timeout ou falta de memória
**Como aplicar:** `llm_provider.py` já tem `_mock_generate()` como fallback automático. Agentes também devem ter fallback próprio (templates, respostas pré-definidas).
