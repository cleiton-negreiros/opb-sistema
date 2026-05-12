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

PROJECT_PATH = Path(__file__).parent.parent.parent
OUTPUT_PATH = PROJECT_PATH / "acervo" / "capas"

def ensure_output():
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    index = OUTPUT_PATH / "index.md"
    if not index.exists():
        index.write_text("""# Capas de Vídeo

> Ideas de thumbnails para YouTube

---

_Last updated: AAAA-MM-DD_
""", encoding='utf-8')

def carregar_contexto():
    """Carrega identidade e regras do cérebro"""
    quem_sou = {}
    
    path = PROJECT_PATH / "negocio" / "governanca" / "regras" / "quem-sou.md"
    if path.exists():
        lines = path.read_text(encoding='utf-8').split('\n')
        for line in lines:
            if "**Nome**:" in line:
                quem_sou['nome'] = line.split('**Nome**:')[-1].strip()
            if "**Cores primárias**:" in line:
                quem_sou['cores'] = line.split('**Cores primárias**:')[-1].strip()
            if "**Estilo**:" in line:
                quem_sou['estilo'] = line.split('**Estilo**:')[-1].strip()
    
    return quem_sou

def gerar_ideias_capa(tema: str, quantidade: int = 5) -> list:
    """Gera ideias de thumbnail baseadas no tema"""
    
    contexto = carregar_contexto()
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

def salvar_capa(tema: str, ideias: list) -> str:
    """Salva as ideias de capa em arquivo"""
    ensure_output()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tema_seguro = tema.replace(' ', '-')[:30]
    filename = f"{tema_seguro}_{timestamp}.md"
    filepath = OUTPUT_PATH / filename
    
    conteudo = f"""---
name: "Capas: {tema}"
tipo: capa_video
tema: {tema}
quantidade: {len(ideias)}
data: {datetime.now().strftime("%Y-%m-%d")}
---

# {tema}

> Ideas de thumbnail geradas em {datetime.now().strftime("%Y-%m-%d")}

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

def listar_capas():
    """Lista capas salvas"""
    ensure_output()
    capas = sorted(OUTPUT_PATH.glob("*.md"), reverse=True)
    
    print(f"\n[{len(capas)} capas salvas]\n")
    for c in capas:
        print(f"  - {c.stem}")

def main():
    ensure_output()
    
    if len(sys.argv) < 2:
        print("""
🎬 Agente Capa de Vídeo

USO:
  python main.py "tema do video"
  python main.py --listar
  python main.py --ler "nome"

EXEMPLOS:
  python main.py "IA para negocios"
  python main.py "Automacao de tarefas"
  python main.py "Produtividade pessoal"
""")
        return
    
    arg1 = sys.argv[1]
    
    if arg1 == "--listar":
        listar_capas()
        return
    
    if arg1 == "--ler" and len(sys.argv) > 2:
        nome = sys.argv[2]
        caminho = OUTPUT_PATH / f"{nome}.md"
        if caminho.exists():
            print(caminho.read_text(encoding='utf-8'))
        return
    
    # Gerar capas
    tema = arg1
    quantidade = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 5
    
    print(f"🎬 Gerando ideias de capa para: {tema}")
    
    ideias = gerar_ideias_capa(tema, quantidade)
    
    print(f"\n[Gerado {len(ideias)} ideias]\n")
    for i, ideia in enumerate(ideias, 1):
        print(f"{i}. {ideia['titulo']}")
        print(f"   Estilo: {ideia['descricao']}")
        print(f"   Cores: {', '.join(ideia['cores'])}")
        print()
    
    arquivo = salvar_capa(tema, ideias)
    print(f"Salvo em: {arquivo}")

if __name__ == "__main__":
    main()