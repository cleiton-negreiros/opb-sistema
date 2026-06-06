"""
Perfil Quiz - Schema de perguntas guiadas para construir o perfil do usuário.

Design:
  - Uma pergunta por vez (chat-style), adaptada ao estado atual
  - Cada pergunta tem um peso (essencial = 1.0, nice-to-have = 0.5)
  - Progress = sum(answered_weights) / sum(all_weights)
  - Salva incremental em perfis/<id>/perfil/*.md (multi-perfil ready)

Uso:
  from utils.perfil_quiz import get_quiz_schema, compute_progress
  schema = get_quiz_schema()
  progress = compute_progress(profile_id='paz-na-conta')
"""
from typing import Dict, List, Optional, Any
from pathlib import Path

# ==============================
# QUESTION SCHEMA
# ==============================

QUIZ_SCHEMA = [
    # -------- PERFIL (básico) --------
    {
        "id": "perfil.nome",
        "section": "PERFIL",
        "key": "Nome",
        "weight": 1.0,
        "type": "text",
        "prompt": "Qual o nome do seu projeto?",
        "helper": "Pode ser o nome fantasia, marca ou como quer ser chamado.",
        "placeholder": "Ex: Paz na Conta",
    },
    {
        "id": "perfil.autores",
        "section": "PERFIL",
        "key": "Autores",
        "weight": 0.5,
        "type": "text",
        "prompt": "Quem está por trás desse projeto?",
        "helper": "Você sozinho, casal, equipe, etc.",
        "placeholder": "Ex: Ingrid e Cleiton",
    },
    {
        "id": "perfil.tagline",
        "section": "PERFIL",
        "key": "Tagline",
        "weight": 1.0,
        "type": "text",
        "prompt": "Em uma frase, como você se apresenta?",
        "helper": "Tagline que vai na bio do Instagram, e-mail, etc.",
        "placeholder": "Ex: Finanças à luz da fé católica",
    },
    {
        "id": "perfil.nicho",
        "section": "PERFIL",
        "key": "Nicho",
        "weight": 1.0,
        "type": "text",
        "prompt": "Qual é o seu nicho?",
        "helper": "A área específica em que você atua.",
        "placeholder": "Ex: Finanças Católicas — educação financeira com base na fé",
    },
    {
        "id": "perfil.problema",
        "section": "PERFIL",
        "key": "Problema",
        "weight": 1.0,
        "type": "textarea",
        "prompt": "Que problema você resolve para seu público?",
        "helper": "Em poucas frases, explique o que muda na vida dele.",
        "placeholder": "Ex: Ajudar católicos a organizar finanças com fé, sem culpa e sem prosperidade falsa.",
    },
    {
        "id": "perfil.versiculo",
        "section": "PERFIL",
        "key": "Versículo",
        "weight": 0.5,
        "type": "text",
        "prompt": "Tem um versículo ou frase que guia seu trabalho?",
        "helper": "Opcional, mas ajuda a dar profundidade ao tom.",
        "placeholder": 'Ex: "Buscai primeiro o Reino de Deus" (Mt 6,33)',
    },
    # -------- PÚBLICO-ALVO --------
    {
        "id": "publico.cliente_ideal",
        "section": "PUBLICO-ALVO",
        "key": "Cliente Ideal",
        "weight": 1.0,
        "type": "textarea",
        "prompt": "Quem é seu cliente ideal?",
        "helper": "Descreva a pessoa: idade, contexto, dor, momento de vida.",
        "placeholder": "Ex: Católicos praticantes com contas no vermelho, querendo se organizar sem culpa.",
    },
    {
        "id": "publico.problemas",
        "section": "PUBLICO-ALVO",
        "key": "Problemas",
        "weight": 0.5,
        "type": "textarea",
        "prompt": "Quais os 3 principais problemas dele?",
        "helper": "Lista de dores que seu conteúdo resolve.",
        "placeholder": "Ex: Dívidas, ansiedade financeira, conflitos familiares por dinheiro.",
    },
    # -------- POSICIONAMENTO --------
    {
        "id": "posicionamento.diferencial",
        "section": "POSICIONAMENTO",
        "key": "Diferencial",
        "weight": 1.0,
        "type": "textarea",
        "prompt": "O que te diferencia de quem faz parecido?",
        "helper": "Por que escolher VOCÊ e não outro?",
        "placeholder": "Ex: Único que combina fé católica com finanças de forma leve e prática.",
    },
    {
        "id": "posicionamento.frase",
        "section": "POSICIONAMENTO",
        "key": "Frase de Posicionamento",
        "weight": 0.5,
        "type": "textarea",
        "prompt": "Escreva 1 frase de posicionamento (a tese que te define):",
        "helper": "Frase-mãe — repete em todo lugar.",
        "placeholder": "Ex: Ajudamos católicos a organizar as finanças com fé, sem culpa e sem prosperidade falsa.",
    },
    # -------- NARRATIVA --------
    {
        "id": "narrativa.missao",
        "section": "NARRATIVA",
        "key": "Missão",
        "weight": 1.0,
        "type": "textarea",
        "prompt": "Qual é a sua missão? (Por que você faz o que faz?)",
        "helper": "A causa maior, não o produto.",
        "placeholder": "Ex: Ajudar católicos a terem paz nas contas para servir melhor a Deus e ao próximo.",
    },
    {
        "id": "narrativa.origem",
        "section": "NARRATIVA",
        "key": "Origem",
        "weight": 0.5,
        "type": "textarea",
        "prompt": "Como começou sua história nesse projeto?",
        "helper": "O que te tirou da inércia e te fez começar?",
        "placeholder": "Ex: Casal que viveu a falta de organização e decidiu mudar.",
    },
    {
        "id": "narrativa.visao",
        "section": "NARRATIVA",
        "key": "Visão",
        "weight": 0.5,
        "type": "text",
        "prompt": "Onde você quer chegar em 3-5 anos?",
        "helper": "A visão de futuro do projeto.",
        "placeholder": "Ex: Ser a referência em finanças católicas no Brasil.",
    },
    # -------- HABILIDADES --------
    {
        "id": "habilidades.lista",
        "section": "HABILIDADES",
        "key": "Habilidades",
        "weight": 0.5,
        "type": "textarea",
        "prompt": "Quais suas principais habilidades? (uma por linha)",
        "helper": "Técnicas, humanas, conhecimentos — tudo conta.",
        "placeholder": "Ex:\n- Programação Python\n- Nutrição clínica\n- Comunicação",
    },
    {
        "id": "habilidades.resumo",
        "section": "HABILIDADES",
        "key": "Resumo",
        "weight": 0.5,
        "type": "textarea",
        "prompt": "Resuma suas competências em poucas frases:",
        "helper": "Como elas te diferenciam?",
        "placeholder": "Ex: Combino formação técnica em TI com sensibilidade em nutrição e organização familiar.",
    },
    # -------- HISTÓRIAS --------
    {
        "id": "historias.profissional",
        "section": "HISTORIAS",
        "key": "História Profissional",
        "weight": 0.5,
        "type": "textarea",
        "prompt": "Conte sua história profissional em poucas frases:",
        "helper": "O caminho que te trouxe até aqui.",
        "placeholder": "Ex: Cleiton trabalha com TI desde 1999, atuou em bandeiras Visa e Mastercard, hoje se dedica a infoprodutos.",
    },
    {
        "id": "historias.experiencias",
        "section": "HISTORIAS",
        "key": "Experiências",
        "weight": 0.5,
        "type": "textarea",
        "prompt": "Quais 3-5 experiências de vida te marcaram?",
        "helper": "Podem ser profissionais, pessoais, familiares.",
        "placeholder": "Ex: Casamento, compra do apartamento, nascimento do Davi, exoneração da Ingrid.",
    },
    # -------- COSMOVISÃO --------
    {
        "id": "cosmovisao.valores",
        "section": "COSMOVISAO",
        "key": "Valores",
        "weight": 0.5,
        "type": "text",
        "prompt": "Quais seus 5 valores inegociáveis?",
        "helper": "Separe por vírgula. O que nunca você negocia?",
        "placeholder": "Ex: fé, organização, paz, serviço, propósito",
    },
    {
        "id": "cosmovisao.crencas",
        "section": "COSMOVISAO",
        "key": "Crenças",
        "weight": 0.5,
        "type": "textarea",
        "prompt": "Em que você acredita profundamente (que talvez poucos concordem)?",
        "helper": "Suas crenças que sustentam decisões corajosas.",
        "placeholder": "Ex: A pobreza material não é virtude — e a riqueza também não é sinal de bênção.",
    },
    # -------- REGRAS DE ESCRITA --------
    {
        "id": "regras.tom",
        "section": "REGRAS-ESCRITA",
        "key": "Tom de Voz",
        "weight": 1.0,
        "type": "textarea",
        "prompt": "Qual o tom de voz dos seus textos? (uma característica por linha)",
        "helper": "Como você quer soar?",
        "placeholder": "Ex:\n- Leve (finanças não precisa ser peso)\n- Direto (sem enrolação)\n- Próximo (como conversa de café)",
    },
    {
        "id": "regras.regras",
        "section": "REGRAS-ESCRITA",
        "key": "Regras de Escrita",
        "weight": 0.5,
        "type": "textarea",
        "prompt": "Que regras você segue ao escrever?",
        "helper": "O que nunca pode faltar? O que nunca pode aparecer?",
        "placeholder": "Ex: usar 'a gente', nunca travessão, sempre terminar com aplicação prática.",
    },
]


# ==============================
# PROGRESS / STATE
# ==============================

def _strip_accents(s: str) -> str:
    import unicodedata
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _normalize_key(s: str) -> str:
    return _strip_accents(s).strip().lower()


def get_quiz_schema() -> List[Dict[str, Any]]:
    """Retorna a lista de perguntas do quiz."""
    return QUIZ_SCHEMA


def _get_profile_dir(profile_id: str) -> Path:
    """Resolve o diretório de perfil."""
    from pathlib import Path
    project_path = Path(__file__).parent.parent
    return project_path / "perfis" / profile_id / "perfil"


def _is_question_answered(question: Dict[str, Any], profile_id: str) -> bool:
    """Verifica se a pergunta já foi respondida, lendo o MD file."""
    profile_dir = _get_profile_dir(profile_id)
    md_path = profile_dir / f"{question['section']}.md"
    if not md_path.exists():
        return False

    try:
        text = md_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            text = md_path.read_text(encoding="latin-1")
        except Exception:
            return False

    # Procura pela seção. Aceita com ou sem acento, em qualquer nível (## ou ###)
    target_key = _normalize_key(question["key"])
    for line in text.split("\n"):
        if line.startswith("#"):
            section_name = line.lstrip("#").strip()
            if _normalize_key(section_name) == target_key:
                return True
    return False


def compute_progress(profile_id: str) -> Dict[str, Any]:
    """
    Calcula o progresso do quiz para um perfil.

    Returns:
      {
        "answered": int,
        "total": int,
        "percent": int (0-100),
        "answered_ids": [str, ...],
        "missing_ids": [str, ...],
        "next_question": dict | None,
      }
    """
    schema = get_quiz_schema()
    answered_ids = []
    missing_ids = []
    total_weight = 0.0
    answered_weight = 0.0

    for q in schema:
        total_weight += q["weight"]
        if _is_question_answered(q, profile_id):
            answered_ids.append(q["id"])
            answered_weight += q["weight"]
        else:
            missing_ids.append(q["id"])

    # Próxima pergunta = a de MAIOR peso entre as faltantes
    next_q = None
    if missing_ids:
        missing_questions = [q for q in schema if q["id"] in missing_ids]
        # Ordena por peso desc; desempate por ordem original
        next_q = max(missing_questions, key=lambda q: (q["weight"], -schema.index(q)))

    percent = int((answered_weight / total_weight) * 100) if total_weight > 0 else 0

    return {
        "answered": len(answered_ids),
        "total": len(schema),
        "percent": percent,
        "answered_ids": answered_ids,
        "missing_ids": missing_ids,
        "next_question": next_q,
    }


def save_answer(profile_id: str, question_id: str, value: str) -> Dict[str, Any]:
    """
    Salva a resposta em perfis/<id>/perfil/<SECTION>.md.

    Cria o arquivo se não existir.
    Substitui a seção se já existir (pela chave).
    Cria a seção se não existir.

    Returns:
      {"success": True, "section": "PERFIL", "key": "Nome", "path": "..."}
      ou {"success": False, "error": "..."}
    """
    # Encontra a pergunta
    question = next((q for q in QUIZ_SCHEMA if q["id"] == question_id), None)
    if not question:
        return {"success": False, "error": f"Pergunta não encontrada: {question_id}"}

    profile_dir = _get_profile_dir(profile_id)
    profile_dir.mkdir(parents=True, exist_ok=True)
    md_path = profile_dir / f"{question['section']}.md"

    # Lê o arquivo atual
    if md_path.exists():
        text = md_path.read_text(encoding="utf-8")
    else:
        # Cria novo arquivo com frontmatter
        text = f"""---
name: "{question['section']}"
description: "{question['section']} do perfil"
updated_at: "2026-06-06"
---

# {question['section']}

"""

    # Procura pela seção e substitui OU adiciona
    lines = text.split("\n")
    target_key = _normalize_key(question["key"])

    # Encontra a linha da seção
    section_line_idx = None
    next_section_idx = None
    for i, line in enumerate(lines):
        if line.startswith("#"):
            section_name = line.lstrip("#").strip()
            if _normalize_key(section_name) == target_key:
                section_line_idx = i
            elif section_line_idx is not None and next_section_idx is None:
                # Próxima seção após a encontrada
                next_section_idx = i
                break

    if section_line_idx is not None:
        # Substitui o conteúdo da seção (até a próxima seção ou fim)
        end_idx = next_section_idx if next_section_idx is not None else len(lines)
        # Mantém o cabeçalho, substitui o conteúdo
        new_content = list(lines[:section_line_idx + 1])
        new_content.append("")  # linha em branco
        new_content.append(value.strip())
        new_content.append("")  # linha em branco
        new_content.extend(lines[end_idx:])
        new_text = "\n".join(new_content)
    else:
        # Adiciona nova seção no final
        new_text = text.rstrip() + f"\n\n## {question['key']}\n\n{value.strip()}\n"

    # Atualiza updated_at no frontmatter
    import re
    from datetime import datetime
    new_text = re.sub(
        r'(updated_at:\s*")[^"]*(")',
        rf'\g<1>{datetime.now().strftime("%Y-%m-%d")}\g<2>',
        new_text,
        count=1,
    )

    md_path.write_text(new_text, encoding="utf-8")

    return {
        "success": True,
        "section": question["section"],
        "key": question["key"],
        "path": str(md_path),
    }
