"""
Profile Loader — fonte única: perfis/<id>/perfil/*.md (multi-perfil)

Convenção de leitura:
  - PERFIL.md          → nome, descricao, tagline, autores, versiculo
  - REGRAS-ESCRITA.md  → tom_de_voz, valores, regras_escrita, marca_visual
  - NARRATIVA.md       → missao, visao, origem, objetivos
  - PUBLICO-ALVO.md    → publico_alvo
  - POSICIONAMENTO.md  → diferencial, proposta, frase
  - HABILIDADES.md     → habilidades, resumo
  - HISTORIAS.md       → historia_profissional, experiencias
  - COSMOVISAO.md      → valores, crencas (refina REGRAS-ESCRITA)

Aliases de seção (case-insensitive, sem acento):
  - "Público Alvo" / "Público-Alvo" / "Cliente Ideal"  → publico_alvo
  - "Missão" / "Misso" / "Missao"                       → missao
  - "Visão" / "Visao" / "Visão de Futuro"              → visao
  - "História Profissional" / "Historia Profissional"  → historia_profissional
  - "Tom de Voz" / "Tom"                                → tom_de_voz
  - "Valores" / "Valores Inegociáveis"                 → valores
  - "Regras de Escrita" / "Regras"                      → regras_escrita
  - "Proposta de Valor" / "Proposta"                    → proposta_valor
  - "Ponto de Vista" / "Ponto de Vista Único"          → pvu
  - "Cliente Ideal" / "Cliente" / "Público"            → cliente_ideal
"""
import json
import re
import unicodedata
from pathlib import Path
from typing import Dict, Any, Optional, List

PROJECT_PATH = Path(__file__).parent.parent


# ==============================
# ENCODING / NORMALIZATION
# ==============================

def _strip_accents(s: str) -> str:
    """Remove acentos para match tolerante (Público == Publico == P�blico)."""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _normalize_key(s: str) -> str:
    """Lowercase + sem acento + colapsa whitespace + strip trailing :."""
    s = _strip_accents(s).strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = s.rstrip(":")
    return s


# ==============================
# SECTION ALIASES
# ==============================

# Map: normalized section name → canonical key
SECTION_ALIASES = {
    # público-alvo
    "publico alvo": "publico_alvo",
    "publico-alvo": "publico_alvo",
    "publico": "publico_alvo",
    "cliente ideal": "publico_alvo",
    "cliente": "publico_alvo",
    "cliente ideal (descricao)": "publico_alvo",
    "audience": "publico_alvo",
    # missão
    "missao": "missao",
    "missao (descricao)": "missao",
    "proposito": "missao",
    # visão
    "visao": "visao",
    "visao de futuro": "visao",
    "objetivo final": "visao",
    # tom
    "tom de voz": "tom_de_voz",
    "tom": "tom_de_voz",
    "voz": "tom_de_voz",
    # valores
    "valores": "valores",
    "valores inegociaveis": "valores",
    "principios": "valores",
    # regras
    "regras de escrita": "regras_escrita",
    "regras": "regras_escrita",
    "diretrizes": "regras_escrita",
    # história
    "historia profissional": "historia_profissional",
    "historia pessoal": "historia_pessoal",
    "experiencias": "experiencias",
    "experiencias marcantes": "experiencias",
    # posicionamento
    "diferencial": "diferencial",
    "diferencial competitivo": "diferencial",
    "proposta de valor": "proposta_valor",
    "proposta": "proposta_valor",
    "frase de posicionamento": "frase_posicionamento",
    "frase": "frase_posicionamento",
    "frase-mae": "frase_posicionamento",
    "tese": "frase_posicionamento",
    "ponto de vista unico": "pvu",
    "ponto de vista": "pvu",
    "inimigo comum": "inimigo",
    # marca visual
    "marca visual": "marca_visual",
    "identidade visual": "marca_visual",
    # habilidades
    "habilidades": "habilidades",
    "resumo": "resumo",
    "resumo de habilidades": "resumo",
    # narrativa
    "origem": "origem",
    "historia de origem": "origem",
    "verdade": "verdade",
    "problema central": "problema_central",
    "problema superficial": "problema_superficial",
    "problema real": "problema_real",
    "inimigo": "inimigo",
    # crenças/valores
    "crencas": "crencas",
    "credo": "crencas",
    # objetivos
    "objetivos": "objetivos",
    "objetivos do negocio": "objetivos",
    "metas": "objetivos",
    # visão/negócio
    "descricao": "descricao",
    "descrição": "descricao",
    "tagline": "tagline",
    "autores": "autores",
    "instagram": "instagram",
    "telegram": "telegram",
    "versiculo": "versiculo",
    "nicho": "nicho",
    "problema": "problema",
}


def _resolve_section(name: str) -> Optional[str]:
    """Resolve um nome de seção (com qualquer variação/typo) para a chave canônica."""
    norm = _normalize_key(name)
    if norm in SECTION_ALIASES:
        return SECTION_ALIASES[norm]
    # Try with trailing content removed (e.g., "Nome (descrição)" → "nome")
    base = norm.split("(")[0].strip()
    if base in SECTION_ALIASES:
        return SECTION_ALIASES[base]
    return None


# ==============================
# MD PARSER
# ==============================

def _parse_md_sections(text: str) -> Dict[str, Any]:
    """
    Parse MD file using a section-based approach: split by ## headers, then parse each section.

    For each section, classify content as:
      - list (starts with "- ", "* ", or "1. ")
      - table (rows starting with "|")
      - text (everything else, joined as a paragraph)

    Returns dict: {section_key: str | list[str] | list[dict]}
    """
    # Strip frontmatter (--- at start of file)
    text = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL)

    out: Dict[str, Any] = {}

    # Split by H2/H3/H4 headers
    # Use lookahead: keep the headers as markers
    sections = re.split(r"^(#{2,4})\s+(.+?)\s*$", text, flags=re.MULTILINE)

    # sections[0] is content before first header (ignored)
    # Then triplets: (header_level, header_text, section_content)
    i = 1
    while i < len(sections):
        header_level = sections[i]
        header_text = sections[i + 1].strip()
        content = sections[i + 2] if i + 2 < len(sections) else ""
        i += 3

        key = _resolve_section(header_text) or _normalize_key(header_text)
        parsed = _parse_section_content(content)
        if parsed is not None and parsed != "" and parsed != []:
            out[key] = parsed

    return out


def _parse_section_content(content: str) -> Any:
    """
    Parse the body of a section. Returns:
      - list[str] if all non-empty lines are list items
      - list[dict] if it's a table
      - str (paragraph) otherwise
      - None if empty
    """
    if not content or not content.strip():
        return None

    # Strip horizontal rules (---) and HTML comments
    lines = []
    for line in content.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r"^[-_*]{3,}\s*$", stripped):  # horizontal rule
            continue
        if stripped.startswith("<!--") and stripped.endswith("-->"):
            continue
        if stripped.startswith(">"):  # blockquote — keep as text
            stripped = stripped.lstrip(">").strip()
        if stripped.startswith("**") and stripped.endswith("**") and stripped.count("**") == 2:
            # Standalone bold line (decorative) — skip
            continue
        lines.append(stripped)

    if not lines:
        return None

    # Check if it's a table
    if all(l.startswith("|") and l.endswith("|") for l in lines):
        if len(lines) >= 2 and re.match(r"^\|[\s\-:|]+\|$", lines[1]):
            header = [c.strip() for c in lines[0].strip("|").split("|")]
            rows = []
            for line in lines[2:]:
                cells = [c.strip() for c in line.strip("|").split("|")]
                if cells:
                    rows.append(dict(zip(header, cells)))
            return rows
        return "\n".join(lines)

    # Check if it's a list
    list_pattern = re.compile(r"^([-*+]|\d+\.)\s+")
    if all(list_pattern.match(l) for l in lines):
        items = []
        for l in lines:
            content_str = list_pattern.sub("", l)
            items.append(content_str.strip())
        return items

    # Otherwise, join as text
    return "\n".join(lines)


def _read_md(path: Path) -> Dict[str, Any]:
    """Read MD file and parse sections. Returns empty dict if file doesn't exist."""
    if not path.exists():
        return {}
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            text = path.read_text(encoding="latin-1")
        except Exception:
            return {}
    return _parse_md_sections(text)


# ==============================
# PER-FILE MAPPERS
# ==============================

def _read_perfil_basico(profile_dir: Path) -> Dict[str, Any]:
    """Read PERFIL.md → nome, descricao, tagline, autores, versiculo, nicho, problema."""
    data = _read_md(profile_dir / "PERFIL.md")
    out = {}
    if "nome" in data:
        out["nome"] = data["nome"] if isinstance(data["nome"], str) else str(data["nome"])
    if "descricao" in data:
        out["descricao"] = data["descricao"]
    if "tagline" in data:
        out["tagline"] = data["tagline"]
    if "autores" in data:
        out["autores"] = data["autores"]
    if "instagram" in data:
        out["instagram"] = data["instagram"]
    if "telegram" in data:
        out["telegram"] = data["telegram"]
    if "versiculo" in data:
        out["versiculo"] = data["versiculo"]
    if "nicho" in data:
        out["nicho"] = data["nicho"]
    if "problema" in data:
        out["problema"] = data["problema"]
    # Fallback: tagline from description if not present
    if "tagline" not in out and "descricao" in out:
        out["tagline"] = out["descricao"]
    # Fallback: nome from autores if "Paz na Conta" is the org name
    if "nome" not in out and "autores" in out:
        out["nome"] = "Paz na Conta"
    return out


def _read_regras_escrita(profile_dir: Path) -> Dict[str, Any]:
    """Read REGRAS-ESCRITA.md → tom_de_voz, valores, regras_escrita, marca_visual."""
    data = _read_md(profile_dir / "REGRAS-ESCRITA.md")
    out = {}
    if "tom_de_voz" in data:
        v = data["tom_de_voz"]
        out["tom_de_voz"] = v if isinstance(v, list) else [str(v)]
    if "valores" in data:
        v = data["valores"]
        out["valores"] = v if isinstance(v, list) else [str(v)]
    if "regras_escrita" in data:
        v = data["regras_escrita"]
        out["regras_escrita"] = v if isinstance(v, list) else [str(v)]
    if "marca_visual" in data:
        v = data["marca_visual"]
        if isinstance(v, list) and v and isinstance(v[0], dict):
            # Convert table rows to dict
            out["marca_visual"] = v
        elif isinstance(v, str):
            out["marca_visual"] = {"raw": v}
    return out


def _read_narrativa(profile_dir: Path) -> Dict[str, Any]:
    """Read NARRATIVA.md → missao, visao, origem, objetivos."""
    data = _read_md(profile_dir / "NARRATIVA.md")
    out = {}
    if "missao" in data:
        out["missao"] = data["missao"]
    if "visao" in data:
        out["visao"] = data["visao"]
    if "origem" in data:
        out["origem"] = data["origem"]
    if "objetivos" in data:
        v = data["objetivos"]
        out["objetivos"] = v if isinstance(v, list) else [str(v)]
    return out


def _read_publico(profile_dir: Path) -> Dict[str, Any]:
    """Read PUBLICO-ALVO.md → publico_alvo."""
    data = _read_md(profile_dir / "PUBLICO-ALVO.md")
    out = {}
    if "publico_alvo" in data:
        out["publico_alvo"] = data["publico_alvo"]
    if "problemas" in data:
        out["problemas_publico"] = data["problemas"]
    return out


def _read_posicionamento(profile_dir: Path) -> Dict[str, Any]:
    """Read POSICIONAMENTO.md → diferencial, proposta_valor, frase_posicionamento, pvu."""
    data = _read_md(profile_dir / "POSICIONAMENTO.md")
    out = {}
    if "diferencial" in data:
        out["diferencial"] = data["diferencial"]
    if "proposta_valor" in data:
        out["proposta_valor"] = data["proposta_valor"]
    if "frase_posicionamento" in data:
        out["frase_posicionamento"] = data["frase_posicionamento"]
    if "pvu" in data:
        out["pvu"] = data["pvu"]
    return out


def _read_habilidades(profile_dir: Path) -> Dict[str, Any]:
    """Read HABILIDADES.md → habilidades, resumo."""
    data = _read_md(profile_dir / "HABILIDADES.md")
    out = {}
    if "habilidades" in data:
        v = data["habilidades"]
        out["habilidades"] = v if isinstance(v, list) else [str(v)]
    if "resumo" in data:
        out["resumo_habilidades"] = data["resumo"]
    return out


def _read_historias(profile_dir: Path) -> Dict[str, Any]:
    """Read HISTORIAS.md → historia_profissional, experiencias."""
    data = _read_md(profile_dir / "HISTORIAS.md")
    out = {}
    if "historia_profissional" in data:
        out["historia_profissional"] = data["historia_profissional"]
    if "experiencias" in data:
        out["experiencias"] = data["experiencias"]
    if "historia_pessoal" in data:
        out["historia_pessoal"] = data["historia_pessoal"]
    return out


def _read_cosmovisao(profile_dir: Path) -> Dict[str, Any]:
    """Read COSMOVISAO.md → valores, crencas (refina REGRAS-ESCRITA)."""
    data = _read_md(profile_dir / "COSMOVISAO.md")
    out = {}
    if "valores" in data:
        v = data["valores"]
        out["valores_cosmovisao"] = v if isinstance(v, list) else [str(v)]
    if "crencas" in data:
        v = data["crencas"]
        out["crencas"] = v if isinstance(v, list) else [str(v)]
    return out


# ==============================
# MAIN LOADER
# ==============================

def _get_profile_dir(profile_id: Optional[str] = None) -> Optional[Path]:
    """Resolve profile directory. Returns None if not found."""
    if profile_id:
        p = PROJECT_PATH / "perfis" / profile_id / "perfil"
        if p.exists():
            return p
    return None


def _get_legacy_quem_sou() -> Optional[Path]:
    """Legacy: negocio/governanca/quem-sou.md."""
    p = PROJECT_PATH / "negocio" / "governanca" / "quem-sou.md"
    return p if p.exists() else None


def load_profile(profile_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Carrega perfil completo. Estratégia:
      1. Ler de perfis/<id>/perfil/*.md (multi-perfil, fonte de verdade)
      2. Fallback para negocio/governanca/quem-sou.md (legado)

    Retorna dict com chaves: nome, descricao, tagline, autores, instagram, telegram,
    versiculo, nicho, problema, tom_de_voz, valores, regras_escrita, marca_visual,
    publico_alvo, problemas_publico, missao, visao, origem, objetivos,
    diferencial, proposta_valor, frase_posicionamento, pvu,
    habilidades, resumo_habilidades, historia_profissional, experiencias, crencas.
    """
    profile: Dict[str, Any] = {
        "nome": "", "descricao": "", "tagline": "", "autores": "",
        "instagram": "", "telegram": "", "versiculo": "",
        "nicho": "", "problema": "",
        "tom_de_voz": [], "valores": [], "regras_escrita": [], "marca_visual": {},
        "publico_alvo": "", "problemas_publico": "",
        "missao": "", "visao": "", "origem": "", "objetivos": [],
        "diferencial": "", "proposta_valor": "", "frase_posicionamento": "", "pvu": "",
        "habilidades": [], "resumo_habilidades": "",
        "historia_profissional": "", "experiencias": "", "historia_pessoal": "",
        "crencas": [],
    }

    profile_dir = _get_profile_dir(profile_id)
    if profile_dir:
        # Ler de cada arquivo (com fallback entre eles)
        for data in [
            _read_perfil_basico(profile_dir),
            _read_regras_escrita(profile_dir),
            _read_narrativa(profile_dir),
            _read_publico(profile_dir),
            _read_posicionamento(profile_dir),
            _read_habilidades(profile_dir),
            _read_historias(profile_dir),
            _read_cosmovisao(profile_dir),
        ]:
            for k, v in data.items():
                if v and (not profile.get(k) or (isinstance(profile.get(k), (list, str)) and not profile[k])):
                    profile[k] = v
                elif v and isinstance(profile.get(k), list) and isinstance(v, list):
                    # Merge lists (deduplicate, preserve order)
                    existing = profile[k]
                    for item in v:
                        if item not in existing:
                            existing.append(item)

    # Fallback: legacy quem-sou.md (only fills empty fields)
    legacy = _get_legacy_quem_sou()
    if legacy and profile_id is None:  # only fallback if no specific profile_id
        legacy_data = _read_md(legacy)
        for k, v in legacy_data.items():
            if k in profile and v and (not profile[k] or (isinstance(profile[k], (list, str)) and not profile[k])):
                profile[k] = v

    return profile


def get_profile_summary(profile_id: Optional[str] = None) -> str:
    """
    Retorna um resumo textual do perfil para usar em prompts de LLM.
    """
    p = load_profile(profile_id)
    lines = []
    if p.get("nome"):
        lines.append(f"# {p['nome']}")
    if p.get("tagline"):
        lines.append(f"_{p['tagline']}_")
    if p.get("autores"):
        lines.append(f"**Autores:** {p['autores']}")
    if p.get("versiculo"):
        lines.append(f"**Versículo:** {p['versiculo']}")
    if p.get("nicho"):
        lines.append(f"**Nicho:** {p['nicho']}")
    if p.get("problema"):
        lines.append(f"**Problema que resolve:** {p['problema']}")
    if p.get("publico_alvo"):
        lines.append(f"**Público-alvo:** {p['publico_alvo']}")
    if p.get("missao"):
        lines.append(f"**Missão:** {p['missao']}")
    if p.get("visao"):
        lines.append(f"**Visão:** {p['visao']}")
    if p.get("diferencial"):
        lines.append(f"**Diferencial:** {p['diferencial']}")
    if p.get("frase_posicionamento"):
        lines.append(f"**Frase de posicionamento:** {p['frase_posicionamento']}")
    if p.get("valores"):
        lines.append(f"**Valores:** {', '.join(str(v) for v in p['valores'])}")
    if p.get("tom_de_voz"):
        lines.append(f"**Tom de voz:** {', '.join(str(v) for v in p['tom_de_voz'])}")
    if p.get("regras_escrita"):
        lines.append(f"**Regras de escrita:** {'; '.join(str(v) for v in p['regras_escrita'])}")
    if p.get("objetivos"):
        obj_strs = []
        for obj in p["objetivos"]:
            if isinstance(obj, dict):
                # Tabela: extrair primeira coluna
                first_key = next(iter(obj), None)
                if first_key:
                    obj_strs.append(str(obj[first_key]))
            else:
                obj_strs.append(str(obj))
        if obj_strs:
            lines.append(f"**Objetivos:** {', '.join(obj_strs)}")
    if p.get("historia_profissional"):
        lines.append(f"**História profissional:** {p['historia_profissional']}")
    if p.get("origem"):
        lines.append(f"**Origem:** {p['origem']}")
    return "\n".join(lines)


# ==============================
# BACKWARD-COMPAT EXPORTS
# ==============================

def _get_context_dir(profile_id=None):
    if profile_id:
        p = PROJECT_PATH / "perfis" / profile_id / "cerebro"
        if p.exists():
            return p
    p = PROJECT_PATH / "context-brain"
    return p


def _get_quem_sou_path(profile_id=None):
    if profile_id:
        p = PROJECT_PATH / "perfis" / profile_id / "perfil" / "PERFIL.md"
        if p.exists():
            return p
    p = PROJECT_PATH / "negocio" / "governanca" / "quem-sou.md"
    return p if p.exists() else None


def _load_json(path):
    if path and path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None
