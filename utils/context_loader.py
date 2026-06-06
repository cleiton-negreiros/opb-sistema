import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

PROJECT_PATH = Path(__file__).parent.parent


def _get_profile_dir(profile_id: Optional[str] = None) -> Optional[Path]:
    """Resolve per-profile directory (perfis/<id>/perfil/)."""
    if profile_id:
        p = PROJECT_PATH / "perfis" / profile_id / "perfil"
        if p.exists():
            return p
    return None


def _profile_value(key: str, default=None, profile_id: Optional[str] = None):
    """Get a value from load_profile() with key mapping. Returns default if not found."""
    try:
        from profile_loader import load_profile
    except ImportError:
        return default
    p = load_profile(profile_id)
    val = p.get(key)
    return val if val else default


# Map: business-core key → profile_loader key
# When business-core.json doesn't have a key, fall back to load_profile()
PROFILE_KEY_MAP = {
    "nome": "nome",
    "missao": "missao",
    "publico_alvo": "publico_alvo",
    "valores": "valores",
    "tom_de_voz": "tom_de_voz",
    "descricao": "descricao",
    "tagline": "tagline",
    "visao": "visao",
    "objetivos": "objetivos",
}


def load_context(profile_id: Optional[str] = None) -> Dict[str, Any]:
    context = {}
    context_dir = _get_context_dir(profile_id)
    if context_dir and context_dir.exists():
        for fname in ["business-core.json", "personal-profile.json", "goals.json"]:
            fp = context_dir / fname
            if fp.exists():
                try:
                    context[fname.replace(".json", "")] = json.loads(fp.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, Exception):
                    context[fname.replace(".json", "")] = {}
    return context

def _get_context_dir(profile_id: Optional[str] = None) -> Optional[Path]:
    if profile_id:
        p = PROJECT_PATH / "perfis" / profile_id / "cerebro"
        if p.exists():
            return p
    p = PROJECT_PATH / "context-brain"
    if p.exists():
        return p
    return None

def get_brain_context(profile_id: Optional[str] = None) -> str:
    """
    Build brain context string. Strategy:
      1. Try to load from business-core.json (legacy cache)
      2. Fall back to load_profile() (per-profile MD, source of truth)
      3. Format as "Field: value | Field: value" string
    """
    ctx = load_context(profile_id)
    business = ctx.get("business-core", {})
    profile_json = ctx.get("personal-profile", {})
    goals = ctx.get("goals", {})

    parts = []

    # Build a merged view: JSON takes priority, but fall back to load_profile()
    for json_src, json_field_map in [
        (business, {
            "nome": "nome",
            "missao": "missao",
            "publico_alvo": "publico_alvo",
            "valores": "valores",
        }),
        (profile_json, {
            "tom_de_voz": "tom_de_voz",
        }),
        (goals, {
            "objetivos": "objetivos",
        }),
    ]:
        for jk, pk in json_field_map.items():
            val = json_src.get(jk)
            if not val:
                # Fall back to load_profile
                val = _profile_value(pk, None, profile_id)
            if val:
                if jk == "nome":
                    parts.append(f"Negócio: {val}")
                elif jk == "missao":
                    parts.append(f"Missão: {val}")
                elif jk == "publico_alvo":
                    parts.append(f"Público: {val}")
                elif jk == "valores":
                    if isinstance(val, list):
                        parts.append(f"Valores: {', '.join(str(v) for v in val[:5])}")
                    else:
                        parts.append(f"Valores: {val}")
                elif jk == "tom_de_voz":
                    if isinstance(val, list):
                        parts.append(f"Tom de voz: {', '.join(str(v) for v in val[:3])}")
                    else:
                        parts.append(f"Tom de voz: {val}")
                elif jk == "objetivos":
                    if isinstance(val, list):
                        objs = []
                        for o in val[:3]:
                            if isinstance(o, dict):
                                first_key = next(iter(o), None)
                                if first_key:
                                    objs.append(str(o[first_key])[:80])
                            else:
                                objs.append(str(o)[:80])
                        parts.append(f"Objetivos: {'; '.join(objs)}")
                    else:
                        parts.append(f"Objetivos: {val}")

    return " | ".join(parts) if parts else ""


def get_business_value(key: str, default=None, profile_id: Optional[str] = None):
    """
    Get a business value. Tries:
      1. business-core.json (per-profile or global)
      2. load_profile() (per-profile MD, source of truth)
      3. default
    """
    ctx = load_context(profile_id)
    val = ctx.get("business-core", {}).get(key)
    if val:
        return val
    # Fall back to profile_loader
    profile_key = PROFILE_KEY_MAP.get(key, key)
    val = _profile_value(profile_key, None, profile_id)
    if val:
        return val
    return default


def get_personal_value(key: str, default=None, profile_id: Optional[str] = None):
    ctx = load_context(profile_id)
    val = ctx.get("personal-profile", {}).get(key)
    if val:
        return val
    return default


def get_goal_value(key: str, default=None, profile_id: Optional[str] = None):
    ctx = load_context(profile_id)
    val = ctx.get("goals", {}).get(key)
    if val:
        return val
    return default
