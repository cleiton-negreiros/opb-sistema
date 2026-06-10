#!/usr/bin/env python3
"""
OPB Reels Script Generator - Generate scripts for short videos
Structure: Gancho (3s) + Conteudo (20s) + CTA (7s) = 30s total
Supports: Reels, YouTube Shorts, TikTok

Usage:
    python main.py "3 erros financeiros que catolicos cometem"  - Generate script
    python main.py "tema" --duracao 60                          - 60 second script
    python main.py "tema" --formato shorts                      - YouTube Shorts format
    python main.py "tema" --variacoes 3                         - Generate 3 variations
    python main.py "tema" --exportar                            - Save to file
"""

import argparse
import json
import os
import random
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"
IDEIAS_DIR = SCRIPT_DIR.parent.parent / "acervo" / "ideias"
CONTEUDO_DIR = SCRIPT_DIR.parent.parent / "_conteudo" / "reels"

DURATION_CONFIG = {
    30: {"gancho": 3, "conteudo": 20, "cta": 7},
    60: {"gancho": 5, "conteudo": 45, "cta": 10},
    90: {"gancho": 7, "conteudo": 70, "cta": 13},
}

FORMAT_TIPS = {
    "reels": {
        "aspect": "9:16",
        "max_duration": 90,
        "tips": "Use musica em alta, legendas dinamicas, transicoes rapidas",
    },
    "shorts": {
        "aspect": "9:16",
        "max_duration": 60,
        "tips": "Titulo forte, thumbnail chamativa, SEO no titulo e descricao",
    },
    "tiktok": {
        "aspect": "9:16",
        "max_duration": 180,
        "tips": "Trends atuais, hashtags relevantes, som viral, interacao nos comentarios",
    },
}

GANCHO_TEMPLATES = [
    "Voce sabia que {tema} pode mudar sua vida financeira?",
    "3 erros que todo catolico comete com {tema} - e como evitar!",
    "Pare de perder dinheiro com {tema}! Veja o que a Igreja ensina.",
    "Se voce e catolico e quer organizar suas financas, preste atencao nisso.",
    "A Igreja tem uma resposta surpreendente sobre {tema}.",
    "Isso vai mudar sua forma de pensar sobre {tema} para sempre.",
    "Catolico, voce precisa saber disso sobre {tema}!",
    "O segredo que os santos sabiam sobre {tema}.",
]

CTA_TEMPLATES = [
    "Salve este video para nao esquecer! Siga para mais conteudo catolico sobre financas.",
    "Compartilhe com alguem que precisa ouvir isso! Siga para mais dicas.",
    "Deixe nos comentarios: voce ja aplica isso na sua vida? Siga para mais!",
    "Salva ai e manda pra aquele amigo que precisa ver isso!",
    "Quer mais conteudo como esse? Siga o perfil e ative as notificacoes!",
    "Comenta 'AMEM' se voce concorda! Siga para mais ensinamentos.",
    "Salve este video e siga para transformar suas financas com fe!",
    "Compartilhe com sua familia! Siga para mais conteudo catolico.",
]

VISUAL_TEMPLATES = [
    "Mostrar grafico/subindo seta verde",
    "Texto na tela com destaque",
    "Apontar para texto que aparece",
    "Expressao de surpresa/choque",
    "Mostrar Biblia aberta",
    "Calculadora ou planilha na tela",
    "Comparacao antes/depois",
    "Lista numerada aparecendo",
    "Mostrar dinheiro/moedas",
    "Cruz ou imagem religiosa ao fundo",
]


def query_ollama(prompt, model="llama3.2"):
    """Query Ollama for content generation."""
    if not HAS_REQUESTS:
        return None

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=30,
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "").strip()
    except Exception:
        pass

    return None


def generate_gancho(tema):
    """Generate a hook (gancho) for the video."""
    template = random.choice(GANCHO_TEMPLATES)
    return template.format(tema=tema)


def generate_conteudo(tema, duracao, formato):
    """Generate main content section."""
    config = DURATION_CONFIG.get(duracao, DURATION_CONFIG[30])
    tempo = config["conteudo"]

    if tempo <= 20:
        pontos = 1
    elif tempo <= 45:
        pontos = 3
    else:
        pontos = 5

    conteudos = {
        1: [
            f"A Igreja nos ensina que {tema} nao e apenas uma questao material, mas espiritual. Quando organizamos nossas financas com proposito, honramos a Deus com nossos recursos.",
            f"O dizimo e a base da organizacao financeira catolica. Comece separando os primeiros 10% e veja a providencia divina agir na sua vida.",
            f"Muitos catolicos separam a fe das financas, mas a Biblia fala mais sobre dinheiro do que sobre oracao. E hora de unir os dois.",
        ],
        3: [
            f"Erro 1: Misturar dinheiro da familia com dinheiro da igreja. Tenha clareza nos seus compromissos financeiros.\n\nErro 2: Nao fazer orcamento mensal. A Biblia diz em Lucas 14:28: 'Quem de vos, querendo edificar uma torre, nao se assenta primeiro a calcular as despesas?'\n\nErro 3: Achar que dizimo e opcional. E um ato de fe e obediencia, nao uma negociacao com Deus.",
            f"Ponto 1: Comece com um orcamento simples - anote todas as entradas e saidas.\n\nPonto 2: Priorize o dizimo antes de qualquer gasto. E o primeiro, nao o que sobra.\n\nPonto 3: Crie uma reserva de emergencia antes de investir. A prudencia e uma virtude catolica.",
            f"Dica 1: Use o metodo dos envelopes - separe o dinheiro por categorias.\n\nDica 2: Reze antes de tomar decisoes financeiras importantes.\n\nDica 3: Pratique a caridade mesmo com pouco - Deus multiplica.",
        ],
        5: [
            f"1. Faca um diagnostico financeiro completo hoje.\n2. Defina metas financeiras com prazos.\n3. Crie um orcamento mensal realista.\n4. Priorize o dizimo e a caridade.\n5. Invista com sabedoria e paciencia.",
            f"Passo 1: Liste todas as suas dividas.\nPasso 2: Negocie as maiores taxas.\nPasso 3: Quite as menores primeiro (efeito bola de neve).\nPasso 4: Nao faca novas dividas.\nPasso 5: Comece a poupar mesmo que seja pouco.",
        ],
    }

    key = min(pontos, 5) if pontos <= 5 else 5
    if key not in conteudos:
        key = 3

    return random.choice(conteudos[key])


def generate_cta():
    """Generate a call-to-action."""
    return random.choice(CTA_TEMPLATES)


def generate_visual_sugestions(tema, duracao):
    """Generate visual suggestions for the video."""
    config = DURATION_CONFIG.get(duracao, DURATION_CONFIG[30])
    num_suggestions = max(2, config["conteudo"] // 15)
    suggestions = random.sample(VISUAL_TEMPLATES, min(num_suggestions, len(VISUAL_TEMPLATES)))
    return suggestions


def generate_text_overlay(tema):
    """Generate text overlay suggestions."""
    overlays = [
        f"{tema.upper()} - Guia Catolico",
        "FINANCAS COM FE",
        "DINHEIRO + DEUS",
        "ORGANIZACAO FINANCEIRA CATOLICA",
        "DIZIMO = BENCAO",
        "LIBERDADE FINANCEIRA COM PROPOSITO",
    ]
    return random.choice(overlays)


def generate_script(tema, duracao=30, formato="reels", use_ollama=True):
    """Generate a complete video script."""
    config = DURATION_CONFIG.get(duracao, DURATION_CONFIG[30])
    format_info = FORMAT_TIPS.get(formato, FORMAT_TIPS["reels"])

    gancho = generate_gancho(tema)
    conteudo = generate_conteudo(tema, duracao, formato)
    cta = generate_cta()
    visuals = generate_visual_sugestions(tema, duracao)
    text_overlay = generate_text_overlay(tema)

    if use_ollama:
        ollama_prompt = f"""Generate a short video script (in Portuguese) for Catholic finance content about: {tema}.
Duration: {duracao} seconds.
Format: {formato}.
Structure: Hook (first {config['gancho']}s), Content ({config['conteudo']}s), CTA ({config['cta']}s).
Make it engaging, faithful to Catholic teaching, and practical for personal finance.
Return only the script text, no explanations."""

        ollama_result = query_ollama(ollama_prompt)
        if ollama_result:
            conteudo = ollama_result

    script = {
        "tema": tema,
        "duracao": duracao,
        "formato": formato,
        "estrutura": {
            "gancho": {"tempo": f"{config['gancho']}s", "texto": gancho},
            "conteudo": {"tempo": f"{config['conteudo']}s", "texto": conteudo},
            "cta": {"tempo": f"{config['cta']}s", "texto": cta},
        },
        "visual": visuals,
        "text_overlay": text_overlay,
        "format_tips": format_info["tips"],
    }

    return script


def format_script_output(script, variation_num=None):
    """Format script for display."""
    lines = []
    header = f"Variacao {variation_num}" if variation_num else "Script"
    lines.append("=" * 60)
    lines.append(f"OPB Reels Script Generator - {header}")
    lines.append(f"Tema: {script['tema']}")
    lines.append(f"Duração: {script['duracao']}s | Formato: {script['formato']}")
    lines.append("=" * 60)

    lines.append(f"\n[GANCHO] ({script['estrutura']['gancho']['tempo']})")
    lines.append(script["estrutura"]["gancho"]["texto"])

    lines.append(f"\n[CONTEUDO] ({script['estrutura']['conteudo']['tempo']})")
    lines.append(script["estrutura"]["conteudo"]["texto"])

    lines.append(f"\n[CTA] ({script['estrutura']['cta']['tempo']})")
    lines.append(script["estrutura"]["cta"]["texto"])

    lines.append(f"\n[TEXTO NA TELA]")
    lines.append(script["text_overlay"])

    lines.append(f"\n[SUGESTOES VISUAIS]")
    for i, visual in enumerate(script["visual"], 1):
        lines.append(f"  {i}. {visual}")

    lines.append(f"\n[DICAS PARA {script['formato'].upper()}]")
    lines.append(script["format_tips"])

    return "\n".join(lines)


def save_output(content, filename=None, source_idea=""):
    """Save output to file (acervo + _conteudo/reels)."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IDEIAS_DIR.mkdir(parents=True, exist_ok=True)
    CONTEUDO_DIR.mkdir(parents=True, exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"script_{timestamp}.txt"

    # Add Obsidian frontmatter with source backlink
    header = "---\ntags: reels/script\ntipo: reels\n"
    if source_idea:
        source_rel = source_idea.replace("\\", "/")
        header += "fonte: [[" + source_rel + "]]\n"
    header += "---\n\n"
    content_with_header = header + content

    output_path = OUTPUT_DIR / filename
    ideias_path = IDEIAS_DIR / filename
    conteudo_path = CONTEUDO_DIR / filename

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content_with_header)

    with open(ideias_path, "w", encoding="utf-8") as f:
        f.write(content_with_header)

    with open(conteudo_path, "w", encoding="utf-8") as f:
        f.write(content_with_header)

    return output_path, ideias_path


def main():
    parser = argparse.ArgumentParser(description="OPB Reels Script Generator")
    parser.add_argument("tema", help="Tema do video ou caminho da ideia")
    parser.add_argument("--ideia", help="Caminho do arquivo de ideia (para backlink no grafo)")
    parser.add_argument("--duracao", type=int, default=30, choices=[30, 60, 90], help="Duracao em segundos")
    parser.add_argument("--formato", default="reels", choices=["reels", "shorts", "tiktok"], help="Formato do video")
    parser.add_argument("--variacoes", type=int, default=1, help="Numero de variacoes")
    parser.add_argument("--exportar", action="store_true", help="Salvar output em arquivo")
    parser.add_argument("--sem-ollama", action="store_true", help="Desativar integracao com Ollama")
    parser.add_argument("--modelo", default="llama3.2", help="Modelo Ollama a usar")

    args = parser.parse_args()
    source_idea = args.ideia or ""

    use_ollama = not args.sem_ollama

    all_scripts = []
    for i in range(args.variacoes):
        script = generate_script(args.tema, args.duracao, args.formato, use_ollama)
        all_scripts.append(script)

    output_parts = []
    for idx, script in enumerate(all_scripts, 1):
        var_num = idx if args.variacoes > 1 else None
        output_parts.append(format_script_output(script, var_num))

    full_output = "\n\n".join(output_parts)

    print(full_output)

    if args.exportar:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tema_clean = args.tema.replace(" ", "_")[:30]
        filename = f"script_{tema_clean}_{args.duracao}s_{timestamp}.txt"

        out_path, ideias_path = save_output(full_output, filename, source_idea)
        print(f"\nSalvo em: {out_path}")
        print(f"Salvo em: {ideias_path}")


if __name__ == "__main__":
    main()
