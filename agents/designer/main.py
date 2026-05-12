#!/usr/bin/env python3
"""
🎨 Agente Designer - OPB Sistema
Designer gráfico especialista: diagramas, thumbnails, social media, mockups
"""

import os
import sys
import json
import math
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_PATH = Path(__file__).parent.parent.parent
OUTPUT_PATH = PROJECT_PATH / "acervo" / "designs"

sys.path.append(str(PROJECT_PATH / "utils"))
from llm_provider import generate_text

NOTAS = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
    'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
    'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
}
NOTAS_NOMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

ACORDES_BASE = {
    'C':  [0, 4, 7],    'Cm': [0, 3, 7],    'C7':  [0, 4, 7, 10],
    'D':  [2, 6, 9],    'Dm': [2, 5, 9],    'D7':  [2, 6, 9, 0],
    'E':  [4, 8, 11],   'Em': [4, 7, 11],   'E7':  [4, 8, 11, 2],
    'F':  [5, 9, 0],    'Fm': [5, 8, 0],    'F7':  [5, 9, 0, 3],
    'G':  [7, 11, 2],   'Gm': [7, 10, 2],   'G7':  [7, 11, 2, 5],
    'A':  [9, 1, 4],    'Am': [9, 0, 4],    'A7':  [9, 1, 4, 7],
    'B':  [11, 3, 6],   'Bm': [11, 2, 6],   'B7':  [11, 3, 6, 9],
}

DIAGRAMAS_POPULARES = {
    'C':  {'cordas': ['x', 3, 2, 0, 1, 0], 'pestana': None},
    'Cm': {'cordas': ['x', 3, 5, 5, 4, 3], 'pestana': (3, 1)},
    'C7': {'cordas': ['x', 3, 2, 3, 1, 0], 'pestana': None},
    'D':  {'cordas': ['x', 'x', 0, 2, 3, 2], 'pestana': None},
    'Dm': {'cordas': ['x', 'x', 0, 2, 3, 1], 'pestana': None},
    'D7': {'cordas': ['x', 'x', 0, 2, 1, 2], 'pestana': None},
    'E':  {'cordas': [0, 2, 2, 1, 0, 0], 'pestana': None},
    'Em': {'cordas': [0, 2, 2, 0, 0, 0], 'pestana': None},
    'E7': {'cordas': [0, 2, 0, 1, 0, 0], 'pestana': None},
    'F':  {'cordas': [1, 3, 3, 2, 1, 1], 'pestana': (1, 1)},
    'Fm': {'cordas': [1, 3, 3, 1, 1, 1], 'pestana': (1, 1)},
    'G':  {'cordas': [3, 2, 0, 0, 0, 3], 'pestana': None},
    'G7': {'cordas': [3, 2, 0, 0, 0, 1], 'pestana': None},
    'A':  {'cordas': ['x', 0, 2, 2, 2, 0], 'pestana': None},
    'Am': {'cordas': ['x', 0, 2, 2, 1, 0], 'pestana': None},
    'A7': {'cordas': ['x', 0, 2, 0, 2, 0], 'pestana': None},
    'B':  {'cordas': ['x', 2, 4, 4, 4, 2], 'pestana': (2, 1)},
    'Bm': {'cordas': ['x', 2, 4, 4, 3, 2], 'pestana': (2, 1)},
    'B7': {'cordas': ['x', 2, 1, 2, 0, 2], 'pestana': None},
}

CORES_PADRAO = {
    'fundo': '#FFFFFF',
    'trastes': '#333333',
    'cordas': '#888888',
    'bolinhas': '#E74C3C',
    'texto': '#2C3E50',
    'pestana': '#2C3E50',
}


def ensure_output():
    for sub in ['briefings', 'diagramas', 'mockups', 'pecas']:
        (OUTPUT_PATH / sub).mkdir(parents=True, exist_ok=True)


def load_brand_context():
    ctx = {}
    path = PROJECT_PATH / "negocio" / "governanca" / "regras" / "quem-sou.md"
    if path.exists():
        lines = path.read_text(encoding='utf-8').split('\n')
        for line in lines:
            if '**Nome**' in line:
                ctx['nome'] = line.split('**Nome**:')[-1].strip()
            if '**Cores primárias**' in line:
                ctx['cores'] = line.split('**Cores primárias**:')[-1].strip()
            if '**Estilo visual**' in line:
                ctx['estilo'] = line.split('**Estilo visual**:')[-1].strip()
            if '**Tipografia**' in line:
                ctx['tipografia'] = line.split('**Tipografia**:')[-1].strip()
            if '**Tom de voz**' in line:
                ctx['tom_voz'] = line.split('**Tom de voz**:')[-1].strip()
    return ctx


def gerar_svg_acorde(nome_acorde: str, tom: str = 'C') -> str:
    if nome_acorde not in DIAGRAMAS_POPULARES:
        return f"Acorde '{nome_acorde}' não disponível. Disponíveis: {', '.join(sorted(DIAGRAMAS_POPULARES.keys()))}"

    dados = DIAGRAMAS_POPULARES[nome_acorde]
    cordas = dados['cordas']
    pestana = dados['pestana']

    cell_w = 40
    cell_h = 35
    margin_x = 60
    margin_y = 60
    head_h = 40
    num_trastes = 5
    width = margin_x * 2 + cell_w * 6
    height = margin_y + head_h + cell_h * num_trastes + 40

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">']
    svg.append(f'<rect width="{width}" height="{height}" fill="{CORES_PADRAO["fundo"]}" rx="8"/>')
    svg.append(f'<text x="{width/2}" y="30" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" font-weight="bold" fill="{CORES_PADRAO["texto"]}">{nome_acorde}</text>')

    top_y = margin_y + head_h

    for t in range(num_trastes + 1):
        y = top_y + t * cell_h
        stroke = CORES_PADRAO['pestana'] if t == 0 and pestana else CORES_PADRAO['trastes']
        sw = 4 if t == 0 else 2
        svg.append(f'<line x1="{margin_x}" y1="{y}" x2="{margin_x + cell_w * 5}" y2="{y}" stroke="{stroke}" stroke-width="{sw}"/>')

    for c in range(6):
        x = margin_x + c * cell_w
        svg.append(f'<line x1="{x}" y1="{top_y}" x2="{x}" y2="{top_y + cell_h * num_trastes}" stroke="{CORES_PADRAO["cordas"]}" stroke-width="1.5"/>')

    for c, (corda_i, casa) in enumerate(cordas):
        x = margin_x + corda_i * cell_w

        if casa == 'x':
            svg.append(f'<text x="{x}" y="{top_y - 10}" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" fill="{CORES_PADRAO["texto"]}">x</text>')
            continue

        if isinstance(casa, int):
            if pestana is None:
                y = top_y + (casa - 1) * cell_h + cell_h / 2
                svg.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{CORES_PADRAO["bolinhas"]}" opacity="0.85"/>')
            else:
                pass

    if pestana:
        pest_casa, pest_traste = pestana
        y = top_y + cell_h / 2
        x_start = margin_x + (pest_casa - 1) * cell_w
        x_end = margin_x + 5 * cell_w
        svg.append(f'<rect x="{x_start}" y="{y - 6}" width="{x_end - x_start}" height="12" rx="4" fill="{CORES_PADRAO["pestana"]}" opacity="0.3"/>')

    svg.append('</svg>')
    return '\n'.join(svg)


def salvar_diagrama(nome_acorde: str, tom: str) -> str:
    ensure_output()
    svg = gerar_svg_acorde(nome_acorde, tom)
    if svg.startswith('Acorde') and 'não disponível' in svg:
        print(svg)
        return None
    filename = f"{nome_acorde}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.svg"
    filepath = OUTPUT_PATH / "diagramas" / filename
    filepath.write_text(svg, encoding='utf-8')
    return str(filepath)


def gerar_briefing(tema: str, tipo: str = "post") -> str:
    ctx = load_brand_context()
    prompt = f"""Atue como designer gráfico especialista. Crie um BRIEFING CRIATIVO completo para:

Tema: {tema}
Tipo: {tipo}
Marca: {ctx.get('nome', 'OPB Sistema')}
Cores da marca: {ctx.get('cores', 'Não definido')}
Estilo: {ctx.get('estilo', 'Moderno e limpo')}

O briefing deve incluir:
1. CONCEITO: Ideia central em 1 frase
2. COMPOSIÇÃO: Layout, hierarquia visual, pontos focais
3. PALETA: Cores principais (hex) secundárias e destaque com justificativa
4. TIPOGRAFIA: Fontes sugeridas para título e corpo
5. ELEMENTOS: Ícones, fotos, texturas, formas
6. CÓPIA: Texto sugerido com hierarquia (headline, sub, CTA)
7. PSICOLOGIA: Por que essa composição funciona
8. FORMATO: Dimensões, resolução, orientação

Seja específico e pragmático. Explique o PORQUÊ de cada escolha."""
    return generate_text(prompt)


def salvar_briefing(tema: str, tipo: str, conteudo: str) -> str:
    ensure_output()
    filename = f"{tema.replace(' ', '-')[:30]}_{tipo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = OUTPUT_PATH / "briefings" / filename
    conteudo_final = f"""---
tema: {tema}
tipo: {tipo}
gerado: {datetime.now().strftime('%Y-%m-%d %H:%M')}
---

# Briefing: {tema}

> Tipo: {tipo}

{conteudo}

---
*Gerado pelo Agente Designer*
"""
    filepath.write_text(conteudo_final, encoding='utf-8')
    return str(filepath)


def gerar_paleta(humor: str) -> dict:
    prompt = f"""Atue como designer especialista em cores. Crie uma paleta para o humor/descritivo: "{humor}"

A paleta deve ter:
1. COR PRIMÁRIA: hex + nome + justificativa emocional
2. COR SECUNDÁRIA: hex + nome
3. COR DE DESTAQUE (CTA): hex + nome
4. FUNDO: hex
5. TEXTO: hex
6. 2 CORES DE APOIO: hex

Formato: JSON puro sem markdown - {{"primaria":{{"hex":"#...","nome":"...","porque":"..."}},"secundaria":{{"hex":"#...","nome":"..."}},"destaque":{{"hex":"#...","nome":"..."}},"fundo":"#...","texto":"#...","apoio":["#...","#..."]}}"""
    try:
        resp = generate_text(prompt)
        json_start = resp.index('{')
        json_end = resp.rindex('}') + 1
        return json.loads(resp[json_start:json_end])
    except (ValueError, json.JSONDecodeError):
        return {
            "primaria": {"hex": "#3498DB", "nome": "Azul Confiança", "porque": "Transmite profissionalismo"},
            "secundaria": {"hex": "#2ECC71", "nome": "Verde Crescimento"},
            "destaque": {"hex": "#E74C3C", "nome": "Vermelho Ação"},
            "fundo": "#F8F9FA",
            "texto": "#2C3E50",
            "apoio": ["#F39C12", "#9B59B6"]
        }


def exibir_paleta(paleta: dict):
    print("\n🎨 PALETA DE CORES\n")
    for chave, valor in paleta.items():
        if chave == 'apoio':
            print(f"  Cores de apoio: {', '.join(valor)}")
        elif isinstance(valor, dict):
            print(f"  {chave.upper()}: {valor.get('hex', '')} - {valor.get('nome', '')}")
            if 'porque' in valor:
                print(f"    → {valor['porque']}")
        else:
            print(f"  {chave}: {valor}")
    print()


def main():
    ensure_output()

    if len(sys.argv) < 2:
        print("""
🎨 Agente Designer - OPB Sistema

USO:
  python main.py briefing "tema" [--tipo post|thumb|carrossel|banner]
  python main.py acorde "C" [--tom G]
  python main.py paleta "humor/descritivo"

EXEMPLOS:
  python main.py briefing "IA para solopreneurs" --tipo carrossel
  python main.py acorde "Am"
  python main.py acorde "F" --tom G
  python main.py paleta "natureza elegante minimalista"
""")
        return

    cmd = sys.argv[1]

    if cmd == "briefing":
        tema = sys.argv[2] if len(sys.argv) > 2 else input("Tema: ")
        tipo = "post"
        if '--tipo' in sys.argv:
            idx = sys.argv.index('--tipo')
            tipo = sys.argv[idx + 1] if len(sys.argv) > idx + 1 else tipo
        print(f"\n🎨 Gerando briefing para: {tema} ({tipo})...\n")
        conteudo = gerar_briefing(tema, tipo)
        caminho = salvar_briefing(tema, tipo, conteudo)
        print(conteudo)
        print(f"\n💾 Salvo: {caminho}")

    elif cmd == "acorde":
        nome_acorde = sys.argv[2].upper() if len(sys.argv) > 2 else input("Acorde (ex: C, Am, G7): ").upper()
        tom = 'C'
        if '--tom' in sys.argv:
            idx = sys.argv.index('--tom')
            tom = sys.argv[idx + 1].upper() if len(sys.argv) > idx + 1 else tom
        caminho = salvar_diagrama(nome_acorde, tom)
        if caminho:
            print(f"\n🎸 Diagrama do acorde {nome_acorde} gerado!")
            print(f"💾 Salvo: {caminho}")
        print("\n" + gerar_svg_acorde(nome_acorde, tom))

    elif cmd == "paleta":
        humor = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else input("Descreva o humor/estilo: ")
        print(f"\n🎨 Gerando paleta para: {humor}\n")
        paleta = gerar_paleta(humor)
        exibir_paleta(paleta)

    else:
        print(f"Comando desconhecido: {cmd}")
        print("Use: briefing, acorde, ou paleta")


if __name__ == "__main__":
    main()