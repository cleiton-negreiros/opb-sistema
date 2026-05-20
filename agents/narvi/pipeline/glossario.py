"""Aplica glossário PT-BR pós-Whisper preservando timestamps (D-T3)."""
from __future__ import annotations
from pathlib import Path
import yaml


def carregar_glossario(path: Path | None = None) -> dict[str, str]:
    """Carrega glossário YAML. Fail-soft: arquivo ausente ou YAML inválido => {}."""
    p = path or Path(__file__).resolve().parent.parent / "glossario.yaml"
    if not p.exists():
        return {}
    try:
        with open(p, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except (yaml.YAMLError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def aplicar_glossario(words: list[dict], rules: dict[str, str]) -> list[dict]:
    """Substitui texto preservando timestamps (Pitfall 5 RESEARCH).

    Comparação 1-pra-1 case-insensitive sobre `text` stripped. Whitespace
    leading é preservado (mlx-whisper retorna palavras com espaço inicial).
    """
    if not rules:
        return words
    rules_lower = {k.lower().strip(): v for k, v in rules.items()}
    out = []
    for w in words:
        text = w.get("text", "")
        stripped = text.strip()
        leading = text[: len(text) - len(text.lstrip())]
        if stripped.lower() in rules_lower:
            out.append({**w, "text": leading + rules_lower[stripped.lower()]})
        else:
            out.append(w)
    return out
