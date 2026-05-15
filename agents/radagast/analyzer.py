#!/usr/bin/env python3
"""analyzer.py — Gera ideias de Reels usando Ollama ou Claude API."""

import json
import logging
import os
import re

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import requests
except ImportError:
    requests = None

logger = logging.getLogger("radagast.analyzer")

SYSTEM_PROMPT = """\
Voce e o Radagast, curador de conteudo para um criador de conteudo brasileiro.

QUEM E O CRIADOR:
Brasileiro adulto que produz conteudo em portugues e quer adaptar tendencias \
internacionais para o publico dele. Os perfis EN que ele segue e as keywords \
EN que ele monitora estao listados em config/inspiracoes.json e config/keywords.json \
do repositorio. Use essas listas como sinal do nicho de interesse do criador.

REGRAS:
- Todas as fontes sao em ingles. O criador adaptara para portugues brasileiro.
- Use os perfis e keywords configurados como sinal do nicho.
- Formato alvo: Instagram Reels (15-60 segundos).
- Tom: pratico, direto, sem enrolacao.
- Cada ideia deve ser adaptavel ao contexto brasileiro.
- Nunca sugerir copiar, sempre adaptar com perspectiva propria.
- Priorizar ideias com alto potencial de engajamento (controversas, praticas, ou contra-intuitivas).

FORMATO DE SAIDA (JSON puro, sem markdown):
{
    "ideas": [
        {
            "titulo": "Nome curto do Reel",
            "hook": "Frase de abertura (primeira coisa que aparece na tela)",
            "pontos": ["Ponto 1", "Ponto 2", "Ponto 3"],
            "fonte_url": "Link original em ingles",
            "fonte_autor": "Quem criou o conteudo original",
            "angulo_br": "Como adaptar para o publico brasileiro",
            "formato_sugerido": "talking head | texto na tela | antes/depois | lista"
        }
    ]
}

Gere entre 10 e 15 ideias. Responda APENAS com o JSON. Sem texto antes ou depois.
"""


def generate_reel_ideas(contents: list[dict]) -> list[dict]:
    """Envia conteudos coletados para Ollama/Claude e retorna ideias de Reels."""
    
    # Montar descricao dos conteudos coletados
    content_lines = []
    for i, c in enumerate(contents[:30], 1):  # max 30 para Ollama
        line = (
            f"{i}. [{c['source'].upper()}] {c['author']}: "
            f"{c['title'] or c['text'][:100]}"
        )
        if c.get("url"):
            line += f" | URL: {c['url']}"
        content_lines.append(line)

    user_prompt = (
        f"CONTEUDOS COLETADOS ({len(contents)} items):\n\n"
        + "\n".join(content_lines)
        + "\n\nGere 10 ideias de Reels em JSON:\n"
        + '{"ideas": [{"titulo": "...", "hook": "...", "pontos": ["..."], "fonte_url": "...", "angulo_br": "..."}]}'
    )

    # Tentar Ollama primeiro
    if requests:
        try:
            logger.info(f"Enviando {len(contents)} conteudos para Ollama...")
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi3:mini",
                    "prompt": SYSTEM_PROMPT + "\n\n" + user_prompt,
                    "stream": False,
                    "options": {"num_gpu": 0}
                },
                timeout=180
            )
            if response.status_code == 200:
                raw_text = response.json().get("response", "")
                logger.info("Resposta recebida do Ollama")
        except Exception as e:
            logger.warning(f"Ollama falhou: {e}, tentando Claude API...")
            raw_text = None
    else:
        raw_text = None

    # Se Ollama falhou, tenta Claude
    if not raw_text and anthropic:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if api_key:
            try:
                logger.info(f"Enviando {len(contents)} conteudos para Claude API...")
                client = anthropic.Anthropic(api_key=api_key)
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=4096,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": user_prompt}],
                )
                raw_text = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        raw_text += block.text
            except Exception as e:
                logger.error(f"Claude API falhou: {e}")
                return []

    if not raw_text:
        logger.error("Nenhuma API disponível")
        return []

    # Limpar artefatos
    raw_text = raw_text.strip()
    raw_text = re.sub(r'^```json\s*', '', raw_text)
    raw_text = re.sub(r'\s*```$', '', raw_text)
    raw_text = raw_text.strip()

    try:
        data = json.loads(raw_text)
        ideas = data.get("ideas", [])
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao parsear JSON: {e}")
        logger.error(f"Resposta bruta: {raw_text[:500]}...")
        ideas = []

    logger.info(f"Ideias geradas: {len(ideas)}")
    return ideas
