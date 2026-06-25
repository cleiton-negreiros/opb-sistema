"""
Profile Analyzer — Detector de lacunas e análise de consistência do perfil.

Analisa:
  1. Lacunas: campos ausentes ou com conteúdo placeholder (Em desenvolvimento, etc.)
  2. Consistência: coerência entre nicho, público, posicionamento e narrativa
  3. Completude: score geral do perfil (0-100%)

Uso:
  from utils.profile_analyzer import analyze_profile
  report = analyze_profile('paz-na-conta')
"""
from typing import Dict, List, Any, Optional
from pathlib import Path
import re

PLACEHOLDER_PATTERNS = [
    r"\(em desenvolvimento\)",
    r"\(não definido\)",
    r"\(vazio\)",
    r"\(pending\)",
    r"\(todo\)",
    r"\(a definir\)",
    r"\(a preencher\)",
    r"em desenvolvimento",
    r"não definido",
    r"TODO",
    r"TBD",
    r"\.\.\.",
]

CRITICAL_FIELDS = {
    "PERFIL": ["Nome", "Tagline", "Nicho", "Problema"],
    "PUBLICO-ALVO": ["Cliente Ideal"],
    "POSICIONAMENTO": ["Diferencial", "Frase de Posicionamento"],
    "NARRATIVA": ["Missão"],
    "REGRAS-ESCRITA": ["Tom de Voz"],
}

NICH_KEYWORDS = {
    "paz-na-conta": ["finança", "dinheiro", "conta", "dívida", "investimento", "orçamento", "economia", "katolik", "fé", "igreja"],
    "toque-de-paz": ["música", "louvor", "violão", "baixo", "guitarra", "canto", "liturgia", "acorde"],
    "caminho-vida": ["fé", "espiritualidade", "oração", "escritura", "bíblia", "santo", "evangelho", "cristã", "formação"],
}


def _read_md(profile_dir: Path, section: str) -> str:
    """Lê um arquivo MD do perfil, retorna conteúdo ou string vazia."""
    md_path = profile_dir / f"{section}.md"
    if not md_path.exists():
        return ""
    try:
        text = md_path.read_text(encoding="utf-8-sig")  # Remove BOM
    except UnicodeDecodeError:
        try:
            text = md_path.read_text(encoding="latin-1")
        except Exception:
            return ""
    return text


def _is_placeholder(text: str) -> bool:
    """Verifica se o texto é placeholder."""
    text_lower = text.strip().lower()
    if not text_lower:
        return True
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False


def _extract_section_content(text: str, key: str) -> str:
    """Extrai conteúdo de uma seção markdown (## Key)."""
    lines = text.split("\n")
    target = _normalize(key)
    capturing = False
    content_lines = []
    for line in lines:
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            if _normalize(heading) == target:
                capturing = True
                continue
            elif capturing:
                break
        elif capturing:
            content_lines.append(line)
    return "\n".join(content_lines).strip()


def _normalize(s: str) -> str:
    import unicodedata
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).strip().lower()


def _score_section(text: str, fields: List[str]) -> Dict[str, Any]:
    """Analisa uma seção e retorna score + problemas."""
    issues = []
    filled = 0
    total = len(fields)

    for field in fields:
        content = _extract_section_content(text, field)
        if not content:
            issues.append({"field": field, "type": "missing", "severity": "high"})
        elif _is_placeholder(content):
            issues.append({"field": field, "type": "placeholder", "severity": "medium"})
        else:
            filled += 1

    score = int((filled / total) * 100) if total > 0 else 0
    return {"score": score, "filled": filled, "total": total, "issues": issues}


def _check_cross_consistency(profile_dir: Path, profile_id: str) -> List[Dict[str, Any]]:
    """Verifica coerência entre seções do perfil."""
    problems = []

    perfil_text = _read_md(profile_dir, "PERFIL")
    publico_text = _read_md(profile_dir, "PUBLICO-ALVO")
    posic_text = _read_md(profile_dir, "POSICIONAMENTO")
    narrativa_text = _read_md(profile_dir, "NARRATIVA")

    # 1. Nick deve aparecer no posicionamento/narrativa
    nicho = _extract_section_content(perfil_text, "Nicho")
    if nicho:
        nicho_words = set(_normalize(nicho).split())
        posic_text_norm = _normalize(posic_text)
        narrativa_norm = _normalize(narrativa_text)
        if len(nicho_words) > 2:
            overlap_posic = sum(1 for w in nicho_words if w in posic_text_norm)
            if overlap_posic < 2:
                problems.append({
                    "type": "inconsistency",
                    "severity": "medium",
                    "message": f"Nicho pouco mencionado no Posicionamento ({overlap_posic} overlap)",
                    "suggestion": "Reforce a conexão entre nicho e posicionamento",
                })

    # 2. Problema do perfil deve conectar com público
    problema = _extract_section_content(perfil_text, "Problema")
    publico_cliente = _extract_section_content(publico_text, "Cliente Ideal")
    if problema and publico_cliente:
        prob_words = set(_normalize(problema).split()) - {"de", "do", "da", "dos", "das", "e", "o", "a", "os", "as", "em", "com", "para", "por", "que", "se", "um", "uma"}
        pub_words = set(_normalize(publico_cliente).split()) - {"de", "do", "da", "dos", "das", "e", "o", "a", "os", "as", "em", "com", "para", "por", "que", "se", "um", "uma"}
        if len(prob_words) > 2 and len(pub_words) > 2:
            overlap = prob_words & pub_words
            if len(overlap) < 2:
                problems.append({
                    "type": "inconsistency",
                    "severity": "low",
                    "message": f"Pouca sobreposição entre Problema e Público ({len(overlap)} palavras em comum)",
                    "suggestion": "Verifique se o problema descrito realmente conecta com o público-alvo",
                })

    # 3. Missão deve estar na narrativa
    missao = _extract_section_content(narrativa_text, "Missão")
    if missao and _is_placeholder(missao):
        problems.append({
            "type": "gap",
            "severity": "high",
            "message": "Missão está em desenvolvimento",
            "suggestion": "Defina a missão do projeto — ela guia todo o conteúdo",
        })

    # 4. Verificar coerência do versículo com o nicho
    versiculo = _extract_section_content(perfil_text, "Versículo")
    if versiculo:
        if profile_id == "paz-na-conta" and "finança" not in _normalize(problema or ""):
            if "dinheiro" not in _normalize(problema or "") and "conta" not in _normalize(problema or ""):
                problems.append({
                    "type": "inconsistency",
                    "severity": "low",
                    "message": "Versículo pode não conectar com o nicho de finanças",
                    "suggestion": "Considere um versículo que dialogue mais diretamente com o tema financeiro",
                })

    # 5. Instagram deve estar preenchido
    instagram = _extract_section_content(perfil_text, "Instagram")
    if not instagram or instagram.startswith("@") and len(instagram) < 4:
        problems.append({
            "type": "gap",
            "severity": "medium",
            "message": "Instagram não configurado ou incompleto",
            "suggestion": "Adicione o @ do Instagram para integração com agentes",
        })

    return problems


def analyze_profile(profile_id: str) -> Dict[str, Any]:
    """
    Análise completa do perfil.

    Returns:
      {
        "profile_id": str,
        "overall_score": int (0-100),
        "sections": {
          "PERFIL": {"score": int, "issues": [...]},
          "PUBLICO-ALVO": {"score": int, "issues": [...]},
          ...
        },
        "consistency": [...],
        "total_issues": int,
        "critical_gaps": [...],
        "recommendations": [...],
      }
    """
    project_path = Path(__file__).parent.parent
    profile_dir = project_path / "perfis" / profile_id / "perfil"

    if not profile_dir.exists():
        return {
            "profile_id": profile_id,
            "overall_score": 0,
            "error": f"Perfil não encontrado: {profile_id}",
        }

    sections = {}
    total_score = 0
    total_fields = 0
    all_issues = []

    for section_name, fields in CRITICAL_FIELDS.items():
        text = _read_md(profile_dir, section_name)
        result = _score_section(text, fields)
        sections[section_name] = result
        total_score += result["score"] * len(fields)
        total_fields += len(fields)
        all_issues.extend(result["issues"])

    overall = int(total_score / total_fields) if total_fields > 0 else 0

    # Análise cross-seção
    consistency = _check_cross_consistency(profile_dir, profile_id)

    # Gaps críticos
    critical_gaps = [i for i in all_issues if i["severity"] == "high"]

    # Recomendações
    recommendations = []
    if overall < 50:
        recommendations.append("Complete as seções essenciais primeiro (PERFIL, PUBLICO-ALVO, NARRATIVA)")
    if any(i["type"] == "placeholder" for i in all_issues):
        recommendations.append("Substitua placeholders por conteúdo real")
    if any(c["type"] == "inconsistency" and c["severity"] == "medium" for c in consistency):
        recommendations.append("Revise a coerência entre nicho, público e posicionamento")

    for section_name, result in sections.items():
        if result["score"] < 50:
            recommendations.append(f"Seção {section_name} precisa de atenção ({result['score']}%)")

    return {
        "profile_id": profile_id,
        "overall_score": overall,
        "sections": sections,
        "consistency": consistency,
        "total_issues": len(all_issues),
        "critical_gaps": critical_gaps,
        "recommendations": recommendations,
    }


def analyze_all_profiles() -> Dict[str, Any]:
    """Analisa todos os perfis ativos e compara."""
    import json
    config_path = Path(__file__).parent.parent / "perfis" / "perfis.json"

    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))
        profile_ids = [p["id"] for p in config.get("perfis", []) if p.get("ativo", False)]
    else:
        profile_ids = ["paz-na-conta"]

    results = {}
    for pid in profile_ids:
        results[pid] = analyze_profile(pid)

    # Ranking
    ranking = sorted(results.items(), key=lambda x: x[1].get("overall_score", 0), reverse=True)

    return {
        "profiles": results,
        "ranking": [{"id": pid, "score": r["overall_score"]} for pid, r in ranking],
        "best": ranking[0][0] if ranking else None,
        "worst": ranking[-1][0] if ranking else None,
    }
