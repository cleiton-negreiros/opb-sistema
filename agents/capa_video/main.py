#!/usr/bin/env python3
"""
🎬 Agente Capa de Vídeo - OPB Sistema
Gera ideias de thumbnail/capa para videos do YouTube
"""

import os
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(str(Path(__file__).parent.parent.parent / "utils"))
sys.path.append(str(Path(__file__).parent.parent.parent))

from profile_loader import load_profile
from utils.multi_profile import resolve_profile_id, parse_perfil_arg, get_acervo_path

PROJECT_PATH = Path(__file__).parent.parent.parent


def _output_path(profile_id=None) -> Path:
    """Path de saída (acervo/capas) do perfil resolvido."""
    return get_acervo_path(profile_id) / "capas"


def ensure_output(profile_id=None):
    out = _output_path(profile_id)
    out.mkdir(parents=True, exist_ok=True)
    index = out / "index.md"
    if not index.exists():
        index.write_text("""# Capas de Vídeo

> Ideas de thumbnails para YouTube

---

_Last updated: AAAA-MM-DD_
""", encoding='utf-8')


def carregar_contexto(profile_id: str = None) -> dict:
    """Carrega identidade e regras do cérebro do perfil (multi-perfil)."""
    pid = resolve_profile_id(profile_id)
    try:
        perfil = load_profile(pid)
    except Exception:
        perfil = {}

    mv = perfil.get("marca_visual", {}) or {}
    cores_raw = mv.get("cores_primarias") or mv.get("cores_primárias") or "#FF6B6B, #4ECDC4"
    if isinstance(cores_raw, list):
        cores = ", ".join(str(c).strip() for c in cores_raw)
    else:
        cores = str(cores_raw)

    return {
        "nome": perfil.get("nome") or "Você",
        "cores": cores,
        "estilo": mv.get("estilo") or "limpo e moderno",
        "tom": ", ".join(perfil.get("tom_de_voz") or []) or "direto e envolvente",
    }


def gerar_ideias_capa(tema: str, quantidade: int = 5, profile_id: str = None) -> list:
    """Gera ideias de thumbnail baseadas no tema e no perfil."""

    contexto = carregar_contexto(profile_id)
    nome = contexto.get('nome', 'Você')
    cores = contexto.get('cores', '#FF6B6B, #4ECDC4')
    estilo = contexto.get('estilo', 'limpo e moderno')
    
    templates = [
        {
            "titulo": f"{tema} em 2024",
            "descricao": "Número + Ano no centro",
            "cores": ["#FF6B6B", "#FFE66D"],
            "elementos": ["Número grande", "Ano destacado", "Logo no canto"]
        },
        {
            "titulo": f"O segredo do {tema}",
            "descricao": "Mistério e curiosidade",
            "cores": ["#2C3E50", "#E74C3C"],
            "elementos": ["Palavra 'SEGREDO'", "Olhos desconfiados", "Fundo escuro"]
        },
        {
            "titulo": f"{tema} vs não {tema}",
            "descricao": "Comparação visual forte",
            "cores": ["#27AE60", "#E74C3C"],
            "elementos": ["Divisão no meio", "Check/X emoji", "Setas opostas"]
        },
        {
            "titulo": f"Como dominar {tema}",
            "descricao": "Tutorial em thumbnail",
            "cores": ["#3498DB", "#2C3E50"],
            "elementos": ["Mão apontando", "Logo app", "Fundo azul"]
        },
        {
            "titulo": f"A verdade sobre {tema}",
            "descricao": "Revelação chocante",
            "cores": ["#9B59B6", "#2C3E50"],
            "elementos": ["Alerta/warning", "Olhos arregalados", "Texto minimalista"]
        },
        {
            "titulo": f"{tema} - passo a passo",
            "descricao": "Processo em números",
            "cores": ["#1ABC9C", "#2C3E50"],
            "elementos": ["Números 1-3", "Flechas", "Ícones de passo"]
        },
    ]
    
    return templates[:quantidade]

def salvar_capa(tema: str, ideias: list, profile_id: str = None) -> str:
    """Salva as ideias de capa em arquivo (no path do perfil)."""
    pid = resolve_profile_id(profile_id)
    ensure_output(pid)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tema_seguro = tema.replace(' ', '-')[:30]
    filename = f"{tema_seguro}_{timestamp}.md"
    filepath = _output_path(pid) / filename

    conteudo = f"""---
name: "Capas: {tema}"
tipo: capa_video
tema: {tema}
perfil: {pid}
quantidade: {len(ideias)}
data: {datetime.now().strftime("%Y-%m-%d")}
---

# {tema}

> Ideas de thumbnail geradas em {datetime.now().strftime("%Y-%m-%d")} (perfil: {pid})

"""

    for i, ideia in enumerate(ideias, 1):
        conteudo += f"""
## {i}. {ideia['titulo']}

**Estilo:** {ideia['descricao']}

**Cores:** {', '.join(ideia['cores'])}

**Elementos:** {', '.join(ideia['elementos'])}

---

"""

    conteudo += "*Gerado pelo Agente Capa de Vídeo*"

    filepath.write_text(conteudo, encoding='utf-8')
    return filename

def listar_capas(profile_id: str = None):
    """Lista capas salvas (do perfil resolvido)."""
    pid = resolve_profile_id(profile_id)
    ensure_output(pid)
    capas = sorted(_output_path(pid).glob("*.md"), reverse=True)

    print(f"\n[{len(capas)} capas salvas — perfil: {pid}]\n")
    for c in capas:
        print(f"  - {c.stem}")

def main():
    profile_id, args = parse_perfil_arg(sys.argv[1:])
    pid = resolve_profile_id(profile_id)

    if not args:
        print("""
🎬 Agente Capa de Vídeo

USO:
  python main.py "tema do video" [quantidade] [--perfil <id>]
  python main.py --listar
  python main.py --ler "nome"

EXEMPLOS:
  python main.py "IA para negocios" 5
  python main.py "Automacao de tarefas" --perfil paz-na-conta
""")
        return

    arg1 = args[0]

    if arg1 == "--listar":
        listar_capas(pid)
        return

    if arg1 == "--ler" and len(args) > 1:
        nome = args[1]
        caminho = _output_path(pid) / f"{nome}.md"
        if caminho.exists():
            print(caminho.read_text(encoding='utf-8'))
        return

    # Gerar capas
    tema = arg1
    quantidade = int(args[1]) if len(args) > 1 and args[1].isdigit() else 5

    print(f"🎬 Gerando ideias de capa para: {tema}")
    print(f"   Perfil: {pid}")

    ideias = gerar_ideias_capa(tema, quantidade, pid)

    print(f"\n[Gerado {len(ideias)} ideias]\n")
    for i, ideia in enumerate(ideias, 1):
        print(f"{i}. {ideia['titulo']}")
        print(f"   Estilo: {ideia['descricao']}")
        print(f"   Cores: {', '.join(ideia['cores'])}")
        print()

    arquivo = salvar_capa(tema, ideias, pid)
    print(f"Salvo em: {arquivo}")

if __name__ == "__main__":
    main()