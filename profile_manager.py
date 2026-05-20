"""
OPB Sistema - Profile Manager
Multi-profile support with isolated data per business
"""

import os
import json
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.resolve()
PERFIS_PATH = PROJECT_PATH / "perfis"
PERFIS_CONFIG = PERFIS_PATH / "perfis.json"

def get_active_profile():
    """Get active profile from config file"""
    if not PERFIS_CONFIG.exists():
        return "paz-na-conta"

    try:
        data = json.loads(PERFIS_CONFIG.read_text(encoding='utf-8'))
        return data.get("ativo", "paz-na-conta")
    except Exception:
        return "paz-na-conta"

def set_active_profile(profile_id):
    """Set active profile"""
    if not PERFIS_CONFIG.exists():
        return {"success": False, "error": "perfis.json not found"}

    try:
        data = json.loads(PERFIS_CONFIG.read_text(encoding='utf-8'))
        valid_ids = [p["id"] for p in data.get("perfis", [])]

        if profile_id not in valid_ids:
            return {"success": False, "error": f"Perfil '{profile_id}' não existe"}

        data["ativo"] = profile_id
        PERFIS_CONFIG.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return {"success": True, "profile_id": profile_id}
    except Exception as e:
        return {"success": False, "error": str(e)}

def list_profiles():
    """List all available profiles"""
    if not PERFIS_CONFIG.exists():
        return []

    try:
        data = json.loads(PERFIS_CONFIG.read_text(encoding='utf-8'))
        return data.get("perfis", [])
    except Exception:
        return []

def get_profile_config(profile_id=None):
    """Get profile config from its config.json"""
    if profile_id is None:
        profile_id = get_active_profile()

    config_path = PERFIS_PATH / profile_id / "perfil" / "config.json"
    if not config_path.exists():
        return None

    try:
        return json.loads(config_path.read_text(encoding='utf-8'))
    except Exception:
        return None

def get_profile_path(profile_id=None, subdir=None):
    """Get path to profile directory"""
    if profile_id is None:
        profile_id = get_active_profile()

    base = PERFIS_PATH / profile_id
    if subdir:
        base = base / subdir

    return base

def get_acervo_path(profile_id=None):
    """Get acervo path for profile"""
    return get_profile_path(profile_id, "acervo")

def get_cerebro_path(profile_id=None):
    """Get cerebro path for profile"""
    return get_profile_path(profile_id, "cerebro")

def get_output_path(profile_id=None):
    """Get output path for profile"""
    return get_profile_path(profile_id, "output")

def get_perfil_path(profile_id=None):
    """Get perfil path for profile"""
    return get_profile_path(profile_id, "perfil")
