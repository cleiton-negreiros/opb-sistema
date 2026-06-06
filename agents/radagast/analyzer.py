"""
analyzer.py — Gerador de ideias de conteúdo para OPB Sistema (multi-perfil).

Substitui o SYSTEM_PROMPT hardcoded de Paz na Conta por um builder
profile-aware. O contexto (marca, nicho, público, tom, pilares)
vem de `utils.profile_loader.load_profile()` + `utils.multi_profile.get_profile_config()`.
"""
import json
import logging
import os
import re
import requests
from typing import Optional

logger = logging.getLogger("radagast.analyzer")

# Pilares default por id de perfil — usados quando o perfil não define os próprios.
# Mantém compatibilidade com o comportamento antigo do Paz na Conta.
PILARES_DEFAULT = {
    "paz-na-conta": [
        ("dica-pratica", "Dica pratica (anzol) — orcamento, dividas, poupanca, em termos simples"),
        ("fe-nas-financas", "Fe nas financas — reflexao sobre dinheiro e fe, DSI em linguagem simples"),
        ("casal-pac", "Casal PAC — bastidores, decisoes financeiras reais de Ingrid e Cleiton"),
        ("contraste", "Contraste — 'O que a Biblia diz vs o que os influencers falam'"),
        ("viral", "Conteudo viral — um guia / resolva um problema especifico"),
    ],
    "toque-de-paz": [
        ("musica-nova", "Musica nova — divulgacao de lancamento, video clipe ou letra"),
        ("devocional", "Devocional — reflexao espiritual ligada a uma musica ou salmo"),
        ("bastidores", "Bastidores — composicao, gravacao, estudio, rotina do ministerio"),
        ("comunidade", "Comunidade — historias de quem foi tocado pela musica"),
        ("ensino", "Ensino — como a musica pode ser ferramenta de evangelizacao"),
    ],
    "caminho-vida": [
        ("reflexao", "Reflexao biblica — meditacao sobre uma passagem do dia"),
        ("oracao", "Oracao — guia pratico de oracao para o dia a dia"),
        ("estudo", "Estudo — aprofundamento de um tema da doutrina catolica"),
        ("vida-crista", "Vida crista — como viver a fe no trabalho, familia, rotina"),
        ("sacramentos", "Sacramentos — explicacao acessivel eucarista, confissao, etc"),
    ],
}


def _pilares_para(perfil_id: str) -> list[tuple[str, str]]:
    """Retorna lista (id, descricao) dos pilares do perfil."""
    return PILARES_DEFAULT.get(perfil_id, [
        ("dica-pratica", "Dica pratica — conteudo util e aplicavel"),
        ("reflexao", "Reflexao — pensamento mais profundo, inspiracao"),
        ("bastidores", "Bastidores — rotina, jornada, vida real"),
        ("comunidade", "Comunidade — interacao com o publico, perguntas"),
        ("viral", "Viral — gancho forte, lista, contraste, polemica saudavel"),
    ])


def build_system_prompt(perfil: dict, profile_config: Optional[dict] = None,
                        perfil_id: str = "paz-na-conta") -> str:
    """Constroi o SYSTEM_PROMPT dinamicamente a partir do perfil carregado.

    Args:
        perfil: dict retornado por `profile_loader.load_profile(pid)`.
                Campos: nome, descricao, tom_de_voz, valores, publico_alvo,
                missao, visao, regras_escrita.
        profile_config: dict do `perfis/<id>/perfil/config.json` (id, nome, icone,
                instagram, versiculo, etc).
        perfil_id: id do perfil (para escolher pilares default).

    Returns:
        String com o prompt completo, pronto para Ollama.
    """
    profile_config = profile_config or {}
    nome = (perfil.get("nome") or profile_config.get("nome") or "Seu Perfil").strip()
    handle = profile_config.get("instagram", "@seuarroba")
    versiculo = profile_config.get("versiculo", "").strip()
    descricao = (perfil.get("descricao") or profile_config.get("descricao") or "").strip()
    missao = (perfil.get("missao") or "").strip()
    publico = (perfil.get("publico_alvo") or "").strip()
    tom_list = perfil.get("tom_de_voz") or ["leve, direto, proximo"]
    tom = ", ".join(tom_list) if isinstance(tom_list, list) else str(tom_list)
    valores = perfil.get("valores") or []
    valores_str = ", ".join(valores) if isinstance(valores, list) else "autenticidade, respeito, pratica"
    regras = perfil.get("regras_escrita") or []
    regras_str = "\n- ".join(regras) if isinstance(regras, list) else ""

    pilares = _pilares_para(perfil_id)
    pilares_lista = "\n".join(f"  {i+1}. [{pid}] {pdesc}" for i, (pid, pdesc) in enumerate(pilares))
    pilares_ids = " | ".join(pid for pid, _ in pilares)

    # Formatos de saida por pilar (heuristica simples, sobrescrevivel)
    formato_por_pilar = ", ".join(
        f"{pid}=carrossel|post|reel|story" for pid, _ in pilares
    )

    prompt = f"""Voce e o Radagast, curador de conteudo para {nome} ({handle}).

IDENTIDADE DO PERFIL:
- Marca: {nome}
- Handle: {handle}
- Nicho: {descricao or 'definido pela descricao do perfil'}
- Missao: {missao or 'ajudar o publico a aplicar os principios do nicho na vida real'}
- Publico: {publico or 'publico definido pelo perfil'}
- Tom de voz: {tom}
- Valores: {valores_str}
{f'- Versiculo-chave: {versiculo}' if versiculo else ''}

PILARES DE CONTEUDO (usar SOMENTE estes IDs):
{pilares_lista}

FORMATOS POR PILAR (use o mais adequado ao contexto):
{formato_por_pilar}

REGRAS DE ESCRITA:
- Linguagem simples e direta, sem jargoes desnecessarios
- Fe/identidade aparece naturalmente, nao forcado
- Termine cada ideia com uma aplicacao pratica
- Conecte a um proposito maior, nao so a um "dica legal"
- Frases curtas
- Sem promessas vazias nem "luz no fim do tunel" generico
{f'- Regras especificas do perfil:{chr(10)}- ' + regras_str if regras_str else ''}

FORMATO DE SAIDA (JSON puro, sem markdown):
{{
    "ideas": [
        {{
            "titulo": "Titulo curto do post/carrossel",
            "hook": "Frase de abertura (primeira coisa que aparece na tela)",
            "pontos": ["Ponto 1", "Ponto 2", "Ponto 3"],
            "fonte_url": "Link original",
            "fonte_autor": "Quem criou o conteudo original",
            "pilar": "{pilares_ids}",
            "formato": "carrossel | post | reel | story",
            "angulo_perfil": "Como aplicar a identidade / nicho / versiculo do perfil neste tema"
        }}
    ]
}}

Gere entre 5 e 8 ideias. Responda APENAS com o JSON. Sem texto antes ou depois.
"""
    return prompt


def _carregar_contexto_perfil(profile_id: str) -> tuple[dict, Optional[dict], str]:
    """Helper que carrega perfil + config e retorna (perfil, profile_config, prompt).

    Nunca quebra: se algum load falhar, retorna dados minimos e um prompt de fallback.
    """
    try:
        sys_path = os.path.dirname(os.path.abspath(__file__))
        base = os.path.dirname(sys_path)
        if base not in os.sys.path:
            os.sys.path.insert(0, base)
            utils_path = os.path.join(base, "utils")
            if utils_path not in os.sys.path:
                os.sys.path.insert(0, utils_path)

        from profile_loader import load_profile
        from multi_profile import get_profile_config

        perfil = load_profile(profile_id) or {}
        pconfig = get_profile_config(profile_id)
    except Exception as e:
        logger.warning(f"Falha ao carregar perfil: {e}")
        perfil, pconfig = {}, None

    prompt = build_system_prompt(perfil, pconfig, profile_id)
    return perfil, pconfig, prompt


def generate_reel_ideas(contents: list[dict], profile_id: str = "paz-na-conta",
                        profile_context: str = "") -> list[dict]:
    """Envia conteudos coletados para Ollama e retorna ideias para o perfil resolvido.

    Args:
        contents: lista de dicts com 'source', 'author', 'title', 'text', 'url'.
        profile_id: id do perfil. Se None, usa o ativo.
        profile_context: contexto adicional (opcional) a ser inserido no prompt.
    """
    pid = (profile_id or "paz-na-conta").strip()
    perfil, pconfig, system_prompt = _carregar_contexto_perfil(pid)

    content_lines = []
    max_items = min(len(contents), 3)
    for i, c in enumerate(contents[:max_items], 1):
        line = (
            f"{i}. [{c['source'].upper()}] {c['author']}: "
            f"{c['title'] or c['text'][:100]}"
        )
        if c.get("url"):
            line += f" | URL: {c['url']}"
        content_lines.append(line)

    contexto_extra = ""
    if profile_context:
        contexto_extra = f"\n\nCONTEXTO ADICIONAL DO PERFIL:\n{profile_context}\n\n"

    user_prompt = (
        f"CONTEUDOS COLETADOS ({max_items} items):\n\n"
        + "\n".join(content_lines)
        + contexto_extra
        + "\n\nGere 5 ideias no formato JSON, respeitando os pilares e o tom acima."
    )

    OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
    MODEL = os.environ.get("OLLAMA_MODEL", "tinyllama")

    try:
        logger.info(f"Enviando {max_items} conteudos para Ollama ({MODEL}) [perfil: {pid}]...")
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": system_prompt + "\n\n" + user_prompt,
                "stream": False,
                "options": {"num_gpu": 0}
            },
            timeout=600,
        )
        if response.status_code == 200:
            raw_text = response.json().get("response", "")
            logger.info("Resposta recebida do Ollama")
        else:
            logger.error(f"Ollama retornou status {response.status_code}: {response.text[:200]}")
            raw_text = None
    except Exception as e:
        logger.error(f"Ollama falhou: {e}")
        return []

    if not raw_text:
        logger.error("Nenhuma resposta do Ollama")
        return []

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

    logger.info(f"Ideias geradas: {len(ideas)} [perfil: {pid}]")
    return ideas
