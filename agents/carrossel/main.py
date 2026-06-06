#!/usr/bin/env python3
"""
🎠 Agente Carrossel — OPB Sistema (v3.0: Templates paste-ready)

Gera texto pronto pra colar no Canva/Twitter/Instagram, alinhado com
cada perfil (Paz na Conta, Toque de Paz, Caminho Vida). Estrutura é
determinística (templates); LLM só enricher opcional pra preencher
slots específicos.

Uso:
    python main.py "Moda, consumismo, sobriedade"
    python main.py "Moda, consumismo, sobriedade" --formato twitter
    python main.py "Moda, consumismo, sobriedade" --formato legenda
    python main.py --ideia acervo/ideias/radagast_2026-06-06_10-08-22.md
    python main.py "ideia" --perfil paz-na-conta --tipo contraste
    python main.py "ideia" --enriquecer       # LLM preenche os slots
    python main.py --listar
    python main.py --ler "nome-do-carrossel"

Tipos:    educacional | inspiracional | contraste | engajamento
Formatos: carrossel (default) | twitter | legenda
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_PATH = Path(__file__).parent.parent.parent

sys.path.append(str(PROJECT_PATH))
sys.path.append(str(PROJECT_PATH / "utils"))

try:
    from utils.multi_profile import resolve_profile_id, parse_perfil_arg, get_acervo_path
    from utils.profile_loader import load_profile
    HAS_CEREBRO = True
except Exception as _e:
    HAS_CEREBRO = False
    _import_error = _e

import templates as T


# =====================================================================
# CONTEXTO DO PERFIL
# =====================================================================

def carregar_contexto(perfil_id: str) -> dict:
    """Carrega contexto mínimo do perfil (nome, handle, desc)."""
    if not HAS_CEREBRO:
        return {"nome": "Perfil", "handle": "@perfil", "versiculo": ""}

    try:
        perfil = load_profile(perfil_id) or {}
    except Exception:
        perfil = {}

    try:
        from utils.multi_profile import get_profile_config
        cfg = get_profile_config(perfil_id) or {}
    except Exception:
        cfg = {}

    return {
        "nome": cfg.get("nome") or perfil.get("nome") or "Perfil",
        "handle": cfg.get("instagram", "@perfil"),
        "versiculo": cfg.get("versiculo", ""),
        "descricao": cfg.get("descricao") or perfil.get("descricao") or "",
        "tom": ", ".join(perfil.get("tom_de_voz") or []) or "leve, direto, próximo",
        "publico": perfil.get("publico_alvo") or "",
        "perfil_id": perfil_id,
    }


# =====================================================================
# CARREGAR IDEIA SALVA
# =====================================================================

def carregar_ideia(caminho: str) -> dict:
    """Carrega uma ideia salva de um arquivo MD e extrai:
    - 'titulo': primeira linha H1 ou nome do frontmatter
    - 'hook': hook do frontmatter (se houver)
    - 'pilar': pilar (se houver)
    - 'angulo_catolico' / 'angulo_perfil': ângulo (se houver)
    - 'descricao': texto markdown principal (sem frontmatter/H1)

    Aceita caminhos absolutos ou relativos a PROJECT_PATH ou a home.
    """
    p = Path(caminho)
    if not p.is_absolute():
        candidates = [PROJECT_PATH / caminho, Path.home() / caminho, Path.cwd() / caminho]
        for c in candidates:
            if c.exists():
                p = c
                break
    if not p.exists():
        raise FileNotFoundError(f"Ideia nao encontrada: {caminho}")

    text = p.read_text(encoding="utf-8")

    # Frontmatter
    fm = {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()

    # Conteúdo sem frontmatter
    body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, flags=re.DOTALL).strip()

    # H1 (primeiro)
    h1_match = re.search(r"^#\s+(.+?)$", body, re.MULTILINE)
    h1 = h1_match.group(1).strip() if h1_match else ""

    return {
        "arquivo": str(p),
        "titulo": fm.get("name") or h1 or p.stem,
        "hook": fm.get("hook", "") or fm.get("description", ""),
        "pilar": fm.get("pilar", ""),
        "angulo": fm.get("angulo_catolico", "") or fm.get("angulo_perfil", "") or fm.get("angulo_br", ""),
        "tags": fm.get("tags", ""),
        "body": body[:1500],  # primeiros 1500 chars
    }


# =====================================================================
# ENRIQUECIMENTO OPCIONAL (LLM)
# =====================================================================

def _tentar_enriquecer(perfil_id: str, tema: str, slots: list[dict],
                       contexto: dict) -> dict[str, str]:
    """Tenta usar o LLM pra preencher os placeholders principais de cada slot.

    Retorna dict {placeholder: texto_gerado}. Se LLM falhar, retorna {}.
    """
    if not HAS_CEREBRO:
        return {}

    try:
        from utils.llm_provider import generate_text
    except Exception:
        return {}

    # Monta um pedido compacto: 1 linha por slot
    pedidos = []
    for s in slots:
        pedidos.append(f"- {s['placeholder_principal']}")

    prompt = (
        f"Voce escreve para o perfil '{contexto['nome']}' ({contexto.get('handle','')}).\n"
        f"Tema da publicacao: {tema}\n"
        f"Tom: {contexto.get('tom','leve, direto')}\n"
        f"Publico: {contexto.get('publico','')}\n\n"
        f"Preencha CADA item abaixo com 1-2 frases objetivas em portugues, sem enrolacao.\n"
        f"Se for versiculo, use aspas e referencia. Se for dado, use numero concreto.\n\n"
        + "\n".join(pedidos)
        + "\n\nResponda no formato:\n"
        "DADO: ...\n"
        "CONSEQUÊNCIA: ...\n"
        "(etc, um por linha, usando o rotulo que veio antes dos dois-pontos)\n"
    )

    try:
        raw = generate_text(prompt)
    except Exception as e:
        print(f"   ⚠ LLM falhou: {e}", file=sys.stderr)
        return {}

    if not raw or len(raw) < 20:
        return {}

    # Parse do formato "ROTULO: texto"
    out = {}
    for line in raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip().upper()
            v = v.strip()
            if v:
                out[k] = v

    return out


# =====================================================================
# FORMATAÇÃO POR FORMATO DE SAÍDA
# =====================================================================

def _aplicar_slot(template: str, slot: dict, enrichments: dict) -> str:
    """Aplica o enrichment ao template do slot, deixando placeholders
    em CAIXA ALTA onde o enrichment nao cobriu."""
    txt = template
    placeholder = slot.get("placeholder_principal", "")
    if placeholder:
        # A chave no enrichment é a primeira "palavra" do placeholder
        key = re.split(r"[\s:—-]", placeholder, maxsplit=1)[0].strip().upper()
        if key in enrichments:
            txt = txt.replace(placeholder, enrichments[key])
    return txt


def _tema_curto(tema: str, max_len: int = 28) -> str:
    if len(tema) <= max_len:
        return tema
    return tema[: max_len - 3].rstrip() + "..."


def formatar_carrossel_canva(tema: str, slides: list[dict], perfil_id: str,
                            enrichments: dict, contexto: dict) -> str:
    """Saída PASTE-READY pra Canva: cada slide com separador visual."""
    titulo_visual = f"💸 {tema}"
    if "toque" in perfil_id:
        titulo_visual = f"🎵 {tema}"
    elif "caminho" in perfil_id:
        titulo_visual = f"🌿 {tema}"

    out = []
    out.append(f"# 🎠 CARROSSEL — {titulo_visual}")
    out.append(f"# Perfil: {contexto.get('nome','?')} ({contexto.get('handle','')})")
    out.append(f"# Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    out.append("")
    out.append("═" * 60)
    out.append("INSTRUÇÕES: copie o bloco de cada slide e cole no Canva como")
    out.append("texto. Ajuste o tamanho, centralize e pronto.")
    out.append("═" * 60)
    out.append("")

    for i, s in enumerate(slides, 1):
        txt = _aplicar_slot(s.get("template", ""), s, enrichments)
        if "tema_curto" in s.get("template", ""):
            txt = txt.replace("{tema_curto}", _tema_curto(tema))

        out.append("─" * 60)
        out.append(f"SLIDE {i}/{len(slides)} — {s.get('titulo', s.get('slot','').upper())}")
        out.append("─" * 60)
        out.append("")
        out.append(txt.strip())
        out.append("")

    out.append("═" * 60)
    out.append(f"# FIM — {len(slides)} slides · {contexto.get('handle','')}")
    out.append("═" * 60)
    return "\n".join(out)


def formatar_twitter(tema: str, slides: list[dict], perfil_id: str,
                     enrichments: dict, contexto: dict) -> str:
    """Saída PASTE-READY pra Twitter: thread 1/n."""
    n = len(slides)
    out = []
    out.append(f"# 🧵 THREAD — {tema}")
    out.append(f"# Perfil: {contexto.get('handle','')}")
    out.append(f"# Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    out.append("")
    out.append("═" * 60)
    out.append("INSTRUÇÕES: cada bloco é 1 tweet. Cole um por um no Twitter/X.")
    out.append("Mantenha a ordem. O número (X/{n}) é parte do tweet.".format(n=n))
    out.append("═" * 60)
    out.append("")

    for i, s in enumerate(slides, 1):
        txt = _aplicar_slot(s.get("template", ""), s, enrichments)
        if "tema_curto" in s.get("template", ""):
            txt = txt.replace("{tema_curto}", _tema_curto(tema))

        out.append("─" * 60)
        out.append(f"TWEET {i}/{n}")
        out.append("─" * 60)
        out.append("")
        out.append(txt.strip())
        out.append("")

    out.append("═" * 60)
    out.append(f"# FIM — {n} tweets")
    out.append("═" * 60)
    return "\n".join(out)


def formatar_legenda(tema: str, slides: list[dict], perfil_id: str,
                     enrichments: dict, contexto: dict) -> str:
    """Saída PASTE-READY pra Instagram (caption única)."""
    out = []
    out.append(f"# 📝 LEGENDA INSTAGRAM — {tema}")
    out.append(f"# Perfil: {contexto.get('handle','')}")
    out.append(f"# Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    out.append("")
    out.append("═" * 60)
    out.append("INSTRUÇÕES: copie o bloco abaixo e cole como legenda do post.")
    out.append("═" * 60)
    out.append("")

    # Pega o template do slot "legenda" (ou o primeiro)
    slot = slides[0] if slides else {}
    txt = _aplicar_slot(slot.get("template", ""), slot, enrichments)
    if "TITULO" in txt:
        txt = txt.replace("{TITULO}", tema.upper())
    out.append(txt.strip())
    out.append("")

    out.append("═" * 60)
    out.append("# FIM")
    out.append("═" * 60)
    return "\n".join(out)


# =====================================================================
# SALVAR
# =====================================================================

def _output_path(perfil_id: str) -> Path:
    """Path de saída (acervo/carrossel) do perfil resolvido."""
    return get_acervo_path(perfil_id) / "carrossel"


def ensure_output(perfil_id: str):
    p = _output_path(perfil_id)
    p.mkdir(parents=True, exist_ok=True)
    index = p / "index.md"
    if not index.exists():
        index.write_text(f"""# 🎠 Carrosséis — {perfil_id}

> Gerados pelo Agente Carrossel v3.0 (templates paste-ready).

---

## Índice

_Last updated: AAAA-MM-DD_
""", encoding="utf-8")


def salvar_saida(tema: str, texto: str, formato: str, perfil_id: str) -> str:
    """Salva a saída em arquivo MD, com index."""
    ensure_output(perfil_id)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tema_seguro = re.sub(r"[^\w\s-]", "", tema).strip().replace(" ", "-").lower()[:30]
    if not tema_seguro:
        tema_seguro = "carrossel"
    filename = f"{tema_seguro}_{formato}_{timestamp}.md"
    filepath = _output_path(perfil_id) / filename

    # Adiciona frontmatter
    conteudo = f"""---
tema: {tema}
formato: {formato}
perfil: {perfil_id}
data: {datetime.now().strftime("%Y-%m-%d %H:%M")}
gerado_por: carrossel-v3.0
---

{texto}
"""
    filepath.write_text(conteudo, encoding="utf-8")

    # Atualiza index
    try:
        index = filepath.parent / "index.md"
        existing = index.read_text(encoding="utf-8")
        novo = f"- [{tema} ({formato})]({filename})\n"
        if "## Índice" in existing:
            existing = existing.replace("## Índice\n\n", f"## Índice\n\n{novo}")
        else:
            existing += f"\n## Índice\n\n{novo}"
        index.write_text(existing, encoding="utf-8")
    except Exception:
        pass

    return filename


# =====================================================================
# CLI
# =====================================================================

def listar_salvos(perfil_id: str):
    ensure_output(perfil_id)
    files = sorted(_output_path(perfil_id).glob("*.md"), reverse=True)
    files = [f for f in files if f.name != "index.md"]
    print(f"\n[🎠 {len(files)} carrosséis salvos — perfil: {perfil_id}]\n")
    for f in files:
        print(f"  - {f.stem}")


def ler_salvo(nome: str, perfil_id: str):
    caminho = _output_path(perfil_id) / f"{nome}.md"
    if caminho.exists():
        print(caminho.read_text(encoding="utf-8"))
    else:
        print(f"Carrossel '{nome}' não encontrado em {perfil_id}.")


def main():
    args_full = sys.argv[1:]
    arg_pid, args = parse_perfil_arg(args_full)
    pid = resolve_profile_id(arg_pid)

    if "--listar" in args:
        listar_salvos(pid)
        return

    # args_no_flags = tudo que NÃO é flag nem valor de flag
    flags_com_valor = {"--perfil", "-p", "--ideia", "--tipo", "--formato"}
    args_no_flags = []
    skip_next = False
    for i, a in enumerate(args):
        if skip_next:
            skip_next = False
            continue
        if a in flags_com_valor:
            skip_next = True
            continue
        if any(a.startswith(f + "=") for f in flags_com_valor):
            continue
        if a.startswith("--"):
            continue
        args_no_flags.append(a)

    if "--ler" in args and args_no_flags:
        ler_salvo(args_no_flags[0], pid)
        return

    # Help
    if not args_no_flags and "--ideia" not in args:
        print(__doc__)
        print("\nTipos disponíveis por perfil:")
        for perfil in ("paz-na-conta", "toque-de-paz", "caminho-vida"):
            tipos = T.listar_tipos(perfil)
            print(f"  {perfil}: {', '.join(tipos)}")
        print("\nFormatos: carrossel (default) | twitter | legenda")
        return

    # Parse tema (ideia principal)
    tema = ""
    if args_no_flags:
        tema = args_no_flags[0]
    elif "--ideia" in args:
        idx = args.index("--ideia")
        if idx + 1 >= len(args):
            print("❌ --ideia precisa de um caminho de arquivo.")
            return
        caminho = args[idx + 1]
        try:
            ideia = carregar_ideia(caminho)
        except FileNotFoundError as e:
            print(f"❌ {e}")
            return
        tema = ideia["titulo"]
        print(f"📂 Ideia carregada de: {ideia['arquivo']}")
        print(f"   Título: {tema}")
        if ideia.get("hook"):
            print(f"   Hook: {ideia['hook']}")
        if ideia.get("pilar"):
            print(f"   Pilar: {ideia['pilar']}")
        if ideia.get("angulo"):
            print(f"   Ângulo: {ideia['angulo']}")
    else:
        print("❌ Forneça um tema ou --ideia <arquivo>.")
        return

    # Tipo
    tipo = "educacional"
    if "--tipo" in args:
        idx = args.index("--tipo")
        if idx + 1 < len(args):
            tipo = args[idx + 1]
    elif len(args_no_flags) > 1 and args_no_flags[1] in T.TIPOS_DISPONIVEIS:
        # compat: python main.py "ideia" educacional
        tipo = args_no_flags[1]

    if tipo not in T.TIPOS_DISPONIVEIS:
        print(f"⚠️  Tipo '{tipo}' desconhecido. Usando 'educacional'.")
        tipo = "educacional"

    # Formato
    formato = "carrossel"
    if "--formato" in args:
        idx = args.index("--formato")
        if idx + 1 < len(args):
            formato = args[idx + 1]
    if formato not in T.FORMATOS_DISPONIVEIS:
        print(f"⚠️  Formato '{formato}' desconhecido. Usando 'carrossel'.")

    use_llm = "--enriquecer" in args

    # Carrega contexto
    contexto = carregar_contexto(pid)

    # Pega template
    tmpl_cfg = T.pick_template(pid, tipo, formato)
    slides = tmpl_cfg.get("slides", [])

    if not slides:
        print(f"❌ Sem slides definidos para {pid}/{tipo}/{formato}.")
        return

    # LLM enrichment (opcional)
    enrichments = {}
    if use_llm:
        print(f"🤖 LLM: enriquecendo {len(slides)} slots...")
        enrichments = _tentar_enriquecer(pid, tema, slides, contexto)
        if enrichments:
            print(f"   ✅ {len(enrichments)} slots preenchidos")
        else:
            print(f"   ⚠️  LLM nao retornou nada usável — saida em branco")

    # Formata
    if formato == "carrossel":
        texto = formatar_carrossel_canva(tema, slides, pid, enrichments, contexto)
    elif formato == "twitter":
        texto = formatar_twitter(tema, slides, pid, enrichments, contexto)
    else:  # legenda
        texto = formatar_legenda(tema, slides, pid, enrichments, contexto)

    # Cabeçalho
    print()
    print("═" * 60)
    print(f"🎠 CARROSSEL — {tema}")
    print(f"   Perfil:  {contexto.get('nome', pid)} ({contexto.get('handle','')})")
    print(f"   Tipo:    {tipo}")
    print(f"   Formato: {formato}")
    print(f"   Slides:  {len(slides)}")
    print(f"   LLM:     {'enriquecido' if enrichments else 'template puro'}")
    print("═" * 60)
    print()
    print(texto)
    print()

    # Salva
    arquivo = salvar_saida(tema, texto, formato, pid)
    print(f"📁 Salvo em: perfis/{pid}/acervo/carrossel/{arquivo}")


if __name__ == "__main__":
    main()
