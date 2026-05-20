import json
from pathlib import Path
from typing import Dict, Any

PROJECT_PATH = Path(__file__).parent.parent


def load_profile() -> Dict[str, Any]:
    profile = {
        "nome": "",
        "descricao": "",
        "tom_de_voz": [],
        "valores": [],
        "publico_alvo": "",
        "missao": "",
        "visao": "",
        "marca_visual": {},
        "regras_escrita": [],
        "objetivos": [],
    }

    quem_sou = PROJECT_PATH / "negocio" / "governanca" / "quem-sou.md"
    if quem_sou.exists():
        content = quem_sou.read_text(encoding="utf-8")
        lines = content.split("\n")

        current_section = None
        tom_lines = []
        regras_lines = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("**Nome**:"):
                profile["nome"] = stripped.split("**Nome**:", 1)[-1].strip().rstrip("\\")
            elif stripped.startswith("**Descrição**:"):
                profile["descricao"] = stripped.split("**Descrição**:", 1)[-1].strip().rstrip("\\")
            elif stripped == "## Tom de Voz":
                current_section = "tom"
            elif stripped == "## Valores":
                current_section = "valores"
            elif stripped == "## Público Alvo":
                current_section = "publico"
            elif stripped == "## Missão":
                current_section = "missao"
            elif stripped == "## Visão":
                current_section = "visao"
            elif stripped == "## Marca Visual":
                current_section = "marca"
            elif stripped == "## Regras de Escrita":
                current_section = "regras"
            elif stripped.startswith("## "):
                current_section = None
            elif current_section == "tom" and stripped.startswith("- "):
                tom_lines.append(stripped[2:])
            elif current_section == "valores" and stripped.startswith("- "):
                profile["valores"].append(stripped[2:])
            elif current_section == "publico" and stripped and not stripped.startswith("#") and not stripped.startswith(">"):
                profile["publico_alvo"] = stripped
                current_section = None
            elif current_section == "missao" and stripped and not stripped.startswith("#") and not stripped.startswith(">"):
                profile["missao"] = stripped
                current_section = None
            elif current_section == "visao" and stripped and not stripped.startswith("#") and not stripped.startswith(">"):
                profile["visao"] = stripped
                current_section = None
            elif current_section == "marca" and "|" in stripped and stripped.count("|") == 2:
                parts = [p.strip() for p in stripped.split("|")]
                if len(parts) == 3 and parts[0] and parts[1]:
                    key = parts[0].lower().replace(" ", "_")
                    profile["marca_visual"][key] = parts[1]
            elif current_section == "regras" and stripped.startswith("- "):
                regras_lines.append(stripped[2:])

        profile["tom_de_voz"] = tom_lines
        profile["regras_escrita"] = regras_lines

    context_brain = PROJECT_PATH / "context-brain"
    goals_path = context_brain / "goals.json"
    if goals_path.exists():
        try:
            goals_data = json.loads(goals_path.read_text(encoding="utf-8"))
            profile["objetivos"] = goals_data.get("objetivos", [])
        except (json.JSONDecodeError, Exception):
            pass

    business_path = context_brain / "business-core.json"
    if business_path.exists():
        try:
            business_data = json.loads(business_path.read_text(encoding="utf-8"))
            if not profile["valores"]:
                profile["valores"] = business_data.get("valores", [])
            if not profile["tom_de_voz"]:
                profile["tom_de_voz"] = [business_data.get("tom_de_voz", "")]
            if not profile["publico_alvo"]:
                profile["publico_alvo"] = business_data.get("publico_alvo", "")
            if not profile["missao"]:
                profile["missao"] = business_data.get("missao", "")
            if not profile["visao"]:
                profile["visao"] = business_data.get("visao", "")
            if not profile["marca_visual"]:
                profile["marca_visual"] = business_data.get("marca_visual", {})
        except (json.JSONDecodeError, Exception):
            pass

    return profile
