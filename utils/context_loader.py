import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

PROJECT_PATH = Path(__file__).parent.parent

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
    ctx = load_context(profile_id)
    parts = []
    business = ctx.get("business-core", {})
    if business.get("nome"):
        parts.append(f"Negócio: {business['nome']}")
    if business.get("missao"):
        parts.append(f"Missão: {business['missao']}")
    if business.get("publico_alvo"):
        parts.append(f"Público: {business['publico_alvo']}")
    if business.get("valores"):
        vals = business["valores"]
        if isinstance(vals, list):
            parts.append(f"Valores: {', '.join(vals[:5])}")
    profile = ctx.get("personal-profile", {})
    if profile.get("tom_de_voz"):
        tom = profile["tom_de_voz"]
        if isinstance(tom, list):
            parts.append(f"Tom de voz: {', '.join(tom[:3])}")
        else:
            parts.append(f"Tom de voz: {tom}")
    goals = ctx.get("goals", {})
    if goals.get("objetivos"):
        objs = goals["objetivos"]
        if isinstance(objs, list):
            parts.append(f"Objetivos: {'; '.join(o[:80] for o in objs[:3])}")
    if not parts:
        return _fallback_context(profile_id)
    return " | ".join(parts)

def _fallback_context(profile_id: Optional[str] = None) -> str:
    from profile_loader import load_profile
    try:
        p = load_profile(profile_id)
        parts = []
        if p.get("nome"): parts.append(f"Negócio: {p['nome']}")
        if p.get("missao"): parts.append(f"Missão: {p['missao']}")
        if p.get("publico_alvo"): parts.append(f"Público: {p['publico_alvo']}")
        if p.get("valores"): parts.append(f"Valores: {', '.join(p['valores'][:5])}")
        if p.get("tom_de_voz"): parts.append(f"Tom: {', '.join(p['tom_de_voz'][:3])}")
        return " | ".join(parts) if parts else ""
    except Exception:
        return ""

def get_business_value(key: str, default=None, profile_id: Optional[str] = None):
    ctx = load_context(profile_id)
    return ctx.get("business-core", {}).get(key, default)

def get_personal_value(key: str, default=None, profile_id: Optional[str] = None):
    ctx = load_context(profile_id)
    return ctx.get("personal-profile", {}).get(key, default)

def get_goal_value(key: str, default=None, profile_id: Optional[str] = None):
    ctx = load_context(profile_id)
    return ctx.get("goals", {}).get(key, default)
