#!/usr/bin/env python3
"""
OPB Hashtag Generator - Generate optimized hashtags for Instagram
3 tiers: Popular (1M+), Medium (100K-1M), Niche (<100K)
Max 30 hashtags total (Instagram limit)

Usage:
    python main.py "dizimo e organizacao financeira"  - Generate hashtags for topic
    python main.py --pilar espiritual                  - Generate by content pillar
    python main.py --blocos 3                          - Generate 3 variations
    python main.py --exportar                          - Save to file for reuse
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
DB_PATH = SCRIPT_DIR / "hashtags_db.json"
OUTPUT_DIR = SCRIPT_DIR / "output"
IDEIAS_DIR = SCRIPT_DIR.parent.parent / "acervo" / "ideias"


def load_db():
    """Load the hashtag database."""
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_hashtags_by_tier(hashtags_list, tier):
    """Filter hashtags by tier."""
    return [h for h in hashtags_list if h.get("tier") == tier]


def collect_hashtags_for_pillar(db, pillar):
    """Collect all hashtags for a given pillar."""
    hashtags = []
    pilares = db.get("pilares", {})
    if pillar in pilares:
        for subcategory in pilares[pillar].values():
            hashtags.extend(subcategory)
    gerais = db.get("gerais", {})
    if pillar in gerais:
        hashtags.extend(gerais[pillar])
    return hashtags


def collect_hashtags_for_topic(db, topic):
    """Collect hashtags relevant to a topic using keyword matching."""
    topic_lower = topic.lower()
    hashtags = []
    seen = set()

    pilares = db.get("pilares", {})
    for pillar_name, subcategories in pilares.items():
        for sub_name, sub_hashtags in subcategories.items():
            if sub_name in topic_lower or any(kw in topic_lower for kw in get_keywords(sub_name)):
                for h in sub_hashtags:
                    tag = h["tag"]
                    if tag not in seen:
                        seen.add(tag)
                        hashtags.append(h)

    gerais = db.get("gerais", {})
    for gen_name, gen_hashtags in gerais.items():
        if gen_name in topic_lower or any(kw in topic_lower for kw in get_keywords(gen_name)):
            for h in gen_hashtags:
                tag = h["tag"]
                if tag not in seen:
                    seen.add(tag)
                    hashtags.append(h)

    if not hashtags:
        for pillar_name, subcategories in pilares.items():
            for sub_hashtags in subcategories.values():
                for h in sub_hashtags:
                    tag = h["tag"]
                    if tag not in seen:
                        seen.add(tag)
                        hashtags.append(h)

    return hashtags


def get_keywords(name):
    """Get related keywords for a category name."""
    keyword_map = {
        "dizimo": ["dizimo", "oferta", "maaquias", "fie"],
        "fe": ["fe", "cre", "acredit"],
        "igreja": ["igreja", "missa", "paroquia", "eucaristia"],
        "evangelho": ["evangelho", "palavra", "biblia", "evangeliz"],
        "maria": ["maria", "nossa senhora", "rosario", "ave"],
        "santos": ["santo", "santos", "padre pio", "sao jose"],
        "caridade": ["caridade", "doacao", "solidariedade", "amar"],
        "orcamento": ["orcamento", "budget", "planejar", "controle"],
        "dividas": ["divida", "dividas", "debt", "quit"],
        "investimento": ["invest", "aplic", "rend"],
        "economia": ["economia", "economiz", "poupar", "dinheiro"],
        "testemunho": ["testemunho", "historia", "conversao", "milagre"],
        "conversao": ["conversao", "converter", "mudanca"],
        "milagre": ["milagre", "graca", "bencao"],
        "providencia": ["providencia", "prover"],
        "dsi": ["dsi", "doutrina social", "bem comum"],
        "doutrina": ["doutrina", "ensino", "igreja"],
        "trabalho": ["trabalho", "emprego", "profissao"],
        "bem_comum": ["bem comum", "social", "comunidade"],
        "catolico": ["catolico", "catolica", "roma"],
        "financas": ["financas", "financeiro", "dinheiro"],
        "organizacao": ["organizacao", "organizar", "planejar"],
    }
    return keyword_map.get(name, [name])


def generate_hashtag_set(hashtags, max_total=30, max_t1=5, max_t2=10, max_t3=15):
    """Generate a balanced set of hashtags across 3 tiers."""
    t1 = [h for h in hashtags if h.get("tier") == 1]
    t2 = [h for h in hashtags if h.get("tier") == 2]
    t3 = [h for h in hashtags if h.get("tier") == 3]

    random.shuffle(t1)
    random.shuffle(t2)
    random.shuffle(t3)

    selected = []
    selected.extend(t1[:max_t1])
    selected.extend(t2[:max_t2])
    selected.extend(t3[:max_t3])

    selected = selected[:max_total]
    return selected


def format_hashtags(hashtag_list):
    """Format hashtags for copy-paste."""
    return " ".join(h["tag"] for h in hashtag_list)


def query_ollama(topic, model="llama3.2"):
    """Query Ollama for smart hashtag suggestions."""
    if not HAS_REQUESTS:
        return []

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": f"Generate 10 relevant Instagram hashtags (in Portuguese) for a Catholic finance post about: {topic}. Return only hashtags separated by spaces, no explanations.",
                "stream": False,
            },
            timeout=10,
        )
        if response.status_code == 200:
            data = response.json()
            text = data.get("response", "")
            tags = [t.strip() for t in text.split() if t.startswith("#")]
            return [{"tag": t, "posts": 50000, "tier": 3} for t in tags]
    except Exception:
        pass

    return []


def generate_for_topic(db, topic, use_ollama=True):
    """Generate hashtags for a given topic."""
    hashtags = collect_hashtags_for_topic(db, topic)

    if use_ollama:
        ollama_tags = query_ollama(topic)
        hashtags.extend(ollama_tags)

    if not hashtags:
        for pillar_hashtags in db.get("pilares", {}).values():
            for sub in pillar_hashtags.values():
                hashtags.extend(sub)

    return generate_hashtag_set(hashtags)


def generate_for_pillar(db, pillar, use_ollama=True):
    """Generate hashtags for a content pillar."""
    hashtags = collect_hashtags_for_pillar(db, pillar)

    if use_ollama:
        ollama_tags = query_ollama(f"pilar {pillar} catolico financas")
        hashtags.extend(ollama_tags)

    return generate_hashtag_set(hashtags)


def save_output(content, filename=None):
    """Save output to file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IDEIAS_DIR.mkdir(parents=True, exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hashtags_{timestamp}.txt"

    output_path = OUTPUT_DIR / filename
    ideias_path = IDEIAS_DIR / filename

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    with open(ideias_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path, ideias_path


def main():
    parser = argparse.ArgumentParser(description="OPB Hashtag Generator")
    parser.add_argument("topic", nargs="?", help="Topic for hashtag generation")
    parser.add_argument("--pilar", help="Content pillar: espiritual, pratico, testemunho, dsi")
    parser.add_argument("--blocos", type=int, default=1, help="Number of variations to generate")
    parser.add_argument("--exportar", action="store_true", help="Save output to file")
    parser.add_argument("--sem-ollama", action="store_true", help="Disable Ollama integration")
    parser.add_argument("--modelo", default="llama3.2", help="Ollama model to use")

    args = parser.parse_args()

    if not args.topic and not args.pilar:
        print("Erro: Informe um tema ou use --pilar")
        print("Exemplos:")
        print('  python main.py "dizimo e organizacao financeira"')
        print("  python main.py --pilar espiritual")
        print("  python main.py --pilar pratico --blocos 3")
        print("  python main.py \"dizimo\" --exportar")
        sys.exit(1)

    db = load_db()
    use_ollama = not args.sem_ollama

    all_sets = []
    for i in range(args.blocos):
        if args.pilar:
            hashtag_set = generate_for_pillar(db, args.pilar, use_ollama)
            context = f"Pilar: {args.pilar}"
        else:
            hashtag_set = generate_for_topic(db, args.topic, use_ollama)
            context = f"Tema: {args.topic}"

        formatted = format_hashtags(hashtag_set)
        all_sets.append((context, formatted, hashtag_set))

    output_lines = []
    output_lines.append("=" * 60)
    output_lines.append("OPB Hashtag Generator")
    output_lines.append(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    output_lines.append("=" * 60)

    for idx, (context, formatted, hashtag_set) in enumerate(all_sets, 1):
        output_lines.append(f"\n--- Variacao {idx} ---")
        output_lines.append(context)
        output_lines.append(f"\nHashtags ({len(hashtag_set)}):")
        output_lines.append(formatted)

        t1_count = len([h for h in hashtag_set if h.get("tier") == 1])
        t2_count = len([h for h in hashtag_set if h.get("tier") == 2])
        t3_count = len([h for h in hashtag_set if h.get("tier") == 3])
        output_lines.append(f"\nDistribuicao: Tier 1 (Popular): {t1_count} | Tier 2 (Media): {t2_count} | Tier 3 (Nicho): {t3_count}")

    output_text = "\n".join(output_lines)

    print(output_text)

    if args.exportar:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if args.pilar:
            filename = f"hashtags_{args.pilar}_{timestamp}.txt"
        else:
            topic_clean = args.topic.replace(" ", "_")[:30]
            filename = f"hashtags_{topic_clean}_{timestamp}.txt"

        out_path, ideias_path = save_output(output_text, filename)
        print(f"\nSalvo em: {out_path}")
        print(f"Salvo em: {ideias_path}")


if __name__ == "__main__":
    main()
