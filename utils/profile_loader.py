import json
from pathlib import Path
from typing import Dict, Any, Optional

PROJECT_PATH = Path(__file__).parent.parent

def load_profile(profile_id: Optional[str] = None) -> Dict[str, Any]:
    profile = {
        "nome": "", "descricao": "", "tom_de_voz": [], "valores": [],
        "publico_alvo": "", "missao": "", "visao": "",
        "marca_visual": {}, "regras_escrita": [], "objetivos": [],
    }
    quem_sou = _get_quem_sou_path(profile_id)
    if quem_sou and quem_sou.exists():
        content = quem_sou.read_text(encoding="utf-8")
        lines = content.split("\n")
        current_section = None
        for line in lines:
            s = line.strip()
            if s.startswith("**Nome**:"):
                profile["nome"] = s.split("**Nome**:", 1)[-1].strip().rstrip("\\")
            elif s.startswith("**Descrição**:"):
                profile["descricao"] = s.split("**Descrição**:", 1)[-1].strip().rstrip("\\")
            elif s == "## Tom de Voz": current_section = "tom"
            elif s == "## Valores": current_section = "valores"
            elif s == "## Público Alvo": current_section = "publico"
            elif s == "## Missão": current_section = "missao"
            elif s == "## Visão": current_section = "visao"
            elif s == "## Marca Visual": current_section = "marca"
            elif s == "## Regras de Escrita": current_section = "regras"
            elif s.startswith("## "): current_section = None
            elif current_section == "tom" and s.startswith("- "): profile["tom_de_voz"].append(s[2:])
            elif current_section == "valores" and s.startswith("- "): profile["valores"].append(s[2:])
            elif current_section == "publico" and s and not s.startswith("#"):
                profile["publico_alvo"] = s; current_section = None
            elif current_section == "missao" and s and not s.startswith("#"):
                profile["missao"] = s; current_section = None
            elif current_section == "visao" and s and not s.startswith("#"):
                profile["visao"] = s; current_section = None
            elif current_section == "regras" and s.startswith("- "): profile["regras_escrita"].append(s[2:])
    goals_data = _load_json(_get_context_dir(profile_id) / "goals.json")
    if goals_data:
        profile["objetivos"] = goals_data.get("objetivos", [])
    business_data = _load_json(_get_context_dir(profile_id) / "business-core.json")
    if business_data:
        if not profile["valores"]: profile["valores"] = business_data.get("valores", [])
        if not profile["tom_de_voz"]:
            tv = business_data.get("tom_de_voz", "")
            profile["tom_de_voz"] = [tv] if isinstance(tv, str) else tv
        if not profile["publico_alvo"]: profile["publico_alvo"] = business_data.get("publico_alvo", "")
        if not profile["missao"]: profile["missao"] = business_data.get("missao", "")
        if not profile["visao"]: profile["visao"] = business_data.get("visao", "")
        if not profile["marca_visual"]: profile["marca_visual"] = business_data.get("marca_visual", {})
    return profile

def _get_context_dir(profile_id=None):
    if profile_id:
        p = PROJECT_PATH / "perfis" / profile_id / "cerebro"
        if p.exists(): return p
    p = PROJECT_PATH / "context-brain"
    return p

def _get_quem_sou_path(profile_id=None):
    if profile_id:
        p = PROJECT_PATH / "perfis" / profile_id / "perfil" / "PERFIL.md"
        if p.exists(): return p
    p = PROJECT_PATH / "negocio" / "governanca" / "quem-sou.md"
    return p if p.exists() else None

def _load_json(path):
    if path and path.exists():
        try: return json.loads(path.read_text(encoding="utf-8"))
        except: pass
    return None
