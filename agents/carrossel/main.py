#!/usr/bin/env python3
"""
🎠 Agente Carrossel - OPB Sistema
Transforma texto em estrutura de carrossel para Instagram
"""

import os
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_PATH = Path(__file__).parent.parent.parent
OUTPUT_PATH = PROJECT_PATH / "acervo" / "carrossel"

# Adiciona utils ao path
sys.path.append(str(PROJECT_PATH / "utils"))

def ensure_output():
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    index = OUTPUT_PATH / "index.md"
    if not index.exists():
        index.write_text("""# Carrosséis

> Estruturas de carrossel geradas para Instagram

---

_Last updated: AAAA-MM-DD_
""", encoding='utf-8')


def load_templates():
    """Load carousel templates if they exist, or return defaults."""
    templates_dir = Path(__file__).parent / "templates"
    templates = {}

    if templates_dir.exists():
        for template_file in templates_dir.glob("*.j2"):
            with open(template_file, 'r', encoding='utf-8') as f:
                templates[template_file.stem] = f.read()

    return templates


def carregar_contexto():
    """Carrega identidade e regras do cérebro"""
    from profile_loader import load_profile as load_perfil
    perfil = load_perfil()
    ctx = {
        "nome": perfil.get("nome", "Você"),
        "descricao": perfil.get("descricao", ""),
        "tom": ", ".join(perfil.get("tom_de_voz", [])),
        "valores": perfil.get("valores", []),
        "missao": perfil.get("missao", ""),
        "publico": perfil.get("publico_alvo", ""),
        "regras": perfil.get("regras_escrita", []),
    }
    mv = perfil.get("marca_visual", {})
    ctx["cores"] = mv.get("cores_primárias", "#FF6B6B, #4ECDC4")
    return ctx


SLIDE_TEMPLATES = {
    "educational": [
        {"tipo": "capa", "titulo": "🚀 {tema}", "descricao": "Gancho forte + ícone"},
        {"tipo": "problema", "titulo": "O problema", "descricao": "Dor do público em 1 frase"},
        {"tipo": "causa", "titulo": "A causa raiz", "descricao": "Por que isso acontece"},
        {"tipo": "solucao", "titulo": "A solução", "descricao": "Resposta direta"},
        {"tipo": "passo1", "titulo": "Passo 1", "descricao": "Primeira ação concreta"},
        {"tipo": "passo2", "titulo": "Passo 2", "descricao": "Segunda ação concreta"},
        {"tipo": "passo3", "titulo": "Passo 3", "descricao": "Terceira ação concreta"},
        {"tipo": "resultado", "titulo": "O resultado", "descricao": "Transformação esperada"},
        {"tipo": "cta", "titulo": "Agora é contigo", "descricao": "Call to action"},
    ],
    "inspirational": [
        {"tipo": "capa", "titulo": "💡 {tema}", "descricao": "Frase de impacto"},
        {"tipo": "historia", "titulo": "A história", "descricao": "Narrativa inspiradora"},
        {"tipo": "reviravolta", "titulo": "O momento que mudou tudo", "descricao": "Ponto de virada"},
        {"tipo": "aprendizado", "titulo": "O que aprendi", "descricao": "Lição principal"},
        {"tipo": "principio", "titulo": "O princípio", "descricao": "Conceito aplicável"},
        {"tipo": "reflexao", "titulo": "Pare e reflita", "descricao": "Pergunta provocativa"},
        {"tipo": "cta", "titulo": "Compartilhe", "descricao": "CTA de engajamento"},
    ],
    "promotional": [
        {"tipo": "capa", "titulo": "🆕 {tema}", "descricao": "Anúncio + hype"},
        {"tipo": "problema", "titulo": "Você se identifica?", "descricao": "Dor do público"},
        {"tipo": "apresentacao", "titulo": "A solução", "descricao": "Apresentar produto/serviço"},
        {"tipo": "beneficio1", "titulo": "Benefício #1", "descricao": "Vantagem principal"},
        {"tipo": "beneficio2", "titulo": "Benefício #2", "descricao": "Vantagem secundária"},
        {"tipo": "beneficio3", "titulo": "Benefício #3", "descricao": "Vantagem extra"},
        {"tipo": "prova", "titulo": "Prova social", "descricao": "Depoimento ou dado"},
        {"tipo": "cta", "titulo": "Quero isso!", "descricao": "Call to action"},
    ],
    "engagement": [
        {"tipo": "capa", "titulo": "🤔 {tema}", "descricao": "Pergunta provocativa"},
        {"tipo": "contexto", "titulo": "Sobre esse assunto...", "descricao": "Introdução rápida"},
        {"tipo": "opiniao", "titulo": "Minha opinião", "descricao": "Posicionamento claro"},
        {"tipo": "polemica", "titulo": "O que muita gente erra", "descricao": "Contraponto"},
        {"tipo": "dica", "titulo": "A dica de ouro", "descricao": "Insight valioso"},
        {"tipo": "cta", "titulo": "Concorda? Comenta!", "descricao": "CTA de engajamento"},
    ],
}

PROMPTS_PERFIL = {
    "capa": "Escreva um gancho de carrossel curto e impactante sobre {tema}. Máximo 30 caracteres.",
    "conteudo": "Escreva o conteúdo de um slide de carrossel sobre {tema}. Use frases curtas. Máximo 80 caracteres.",
    "cta": "Escreva um call to action para carrossel sobre {tema}. Máximo 50 caracteres.",
}


def gerar_carrossel(tema: str, tipo: str = "educational", num_slides: int = None) -> list:
    """
    Gera a estrutura de um carrossel baseado no tema e tipo.

    Args:
        tema: Assunto do carrossel
        tipo: Tipo de carrossel (educational, inspirational, promotional, engagement)
        num_slides: Número de slides (usa o padrão do tipo se não especificado)

    Returns:
        Lista de slides com título e descrição
    """
    contexto = carregar_contexto()

    # Pega template do tipo
    template = SLIDE_TEMPLATES.get(tipo, SLIDE_TEMPLATES["educational"])

    # Limita número de slides se especificado
    if num_slides and num_slides < len(template):
        template = template[:num_slides]

    slides = []
    for slide_def in template:
        titulo = slide_def["titulo"].format(tema=tema)
        slides.append({
            "tipo": slide_def["tipo"],
            "titulo": titulo,
            "descricao": slide_def["descricao"],
            "sugestao_visual": gerar_sugestao_visual(slide_def["tipo"], tema, contexto),
            "texto": gerar_texto_slide(tema, slide_def["tipo"], contexto),
        })

    return slides


def gerar_sugestao_visual(tipo_slide: str, tema: str, contexto: dict) -> str:
    """Gera sugestão de elementos visuais para o slide."""
    cores = contexto.get('cores', '#FF6B6B, #4ECDC4').split(', ')

    visuais = {
        "capa": f"Título grande em negrito, cor {cores[0]} como fundo, ícone relacionado ao tema",
        "problema": f"Icone de alerta, fundo {cores[1]}, texto em vermelho suave",
        "causa": f"Diagrama de setas, cores neutras, ícone de lâmpada",
        "solucao": f"Icone de checkmark, fundo {cores[0]}, visual limpo",
        "passo1": f"Número '1' grande, ícone de passo, cor {cores[0]}",
        "passo2": f"Número '2' grande, ícone de passo, cor {cores[1]}",
        "passo3": f"Número '3' grande, ícone de passo, cor {cores[0]}",
        "resultado": f"Icone de troféu ou estrela, fundo gradiente",
        "cta": f"Botão estilizado, cor {cores[0]}, seta ou emoji de ação",
        "historia": f"Imagem emocional, filtro suave, texto overlay",
        "reviravolta": f"Divisão visual, antes/depois, cor de contraste",
        "aprendizado": f"Icone de livro ou lâmpada, fundo claro",
        "reflexao": f"Fundo minimalista, texto centralizado, cor suave",
        "apresentacao": f"Mockup de produto, foto profissional, visual clean",
        "beneficio1": f"Icone de estrela, cor {cores[0]}, destaque",
        "beneficio2": f"Icone de relógio, cor {cores[1]}, destaque",
        "beneficio3": f"Icone de escudo, cor {cores[0]}, destaque",
        "prova": f"Coments/citações, foto de pessoas, badge",
        "opiniao": f"Texto grande em destaque, cor forte",
        "polemica": f"X vermelho, contraste forte, visual ousado",
        "dica": f"Icone de💎, fundo premium, texto elegante",
        "contexto": f"Ícones de contexto, mapa mental, visual informativo",
    }

    return visuais.get(tipo_slide, f"Visual padrão para {tipo_slide}")


def gerar_texto_slide(tema: str, tipo_slide: str, contexto: dict) -> str:
    """Gera o texto de conteúdo para o slide usando perfil do usuário."""
    nome = contexto.get("nome", "Eu")
    tom = contexto.get("tom", "direto e prático")
    publico = contexto.get("publico", "solopreneurs")

    fallbacks = {
        "capa": f"🔥 {tema.upper()}\n\nO que a fé católica tem a ver com isso? Tudo.",
        "problema": f"❌ Católico também se endivida\n\nE não é falta de fé — é falta de organização à luz do que a Igreja ensina",
        "causa": f"🔍 A raiz do problema\n\nEsquecemos que o dinheiro deve servir, não governar (Fratelli Tutti)",
        "solucao": f"✅ O caminho da paz nas contas\n\nOrganização + fé + DSI = tranquilidade real",
        "passo1": f"📌 1. Encare sem culpa\n\nDeus não te cobra juros. A culpa não ajuda — a ação sim.",
        "passo2": f"📌 2. Organize com propósito\n\nCada real tem um destino: servir a Deus, à família e ao próximo",
        "passo3": f"📌 3. Confie na Providência\n\nFaça a sua parte e abandone o resto nas mãos d'Ele",
        "resultado": f"🏆 O resultado não é riqueza\n\nÉ paz. É poder olhar pra conta e não desesperar. É servir melhor.",
        "cta": f"💾 Salva pra ver depois\n\nCompartilha com alguém que precisa ouvir que fé e finanças podem (e devem) andar juntas",
        "historia": f"📖 A gente já esteve onde você está\n\nContas no vermelho, sem saber como conciliar fé e dinheiro",
        "reviravolta": f"⚡ O que mudou?\n\nDescobrimos que a Igreja já tinha a resposta — Doutrina Social + Segredo da Divina Providência",
        "aprendizado": f"💡 O aprendizado\n\nPobreza não é virtude. Riqueza não é bênção. Organização é caminho de santidade.",
        "principio": f"📐 O princípio\n\nDinheiro bem administrado serve a Deus e ao próximo. Mal administrado vira ídolo.",
        "reflexao": f"🤔 E você, já parou pra pensar que suas contas também são lugar de encontro com Deus?",
        "apresentacao": f"🎯 Paz na Conta apresenta:\n\nFinanças à luz da fé católica — sem culpa, sem prosperidade falsa",
        "beneficio1": f"✅ Benefício #1:\n\nVocê aprende a cuidar do dinheiro sem perder a alma",
        "beneficio2": f"⏰ Benefício #2:\n\nOrganização que liberta — não pra ficar rico, pra viver em paz",
        "beneficio3": f"🛡️ Benefício #3:\n\nSuas escolhas financeiras alinhadas com o que você acredita",
        "prova": f"⭐ O que a Igreja diz\n\n\"O dinheiro deve servir, não governar\" — Papa Francisco, Fratelli Tutti",
        "opiniao": f"🔥 O que a gente acredita\n\nFé não é desculpa pra bagunça financeira. É motivo pra se organizar.",
        "polemica": f"⚠️ O que ninguém conta\n\nTeologia da prosperidade não é católica. Mas também não é pecado ser organizado.",
        "dica": f"💎 A dica de ouro\n\nAntes de qualquer investimento, invista na sua paz. O resto é consequência.",
        "contexto": f"📋 O cenário\n\nCatólicos endividados, sem referência, ouvindo que \"Deus quer te ver rico\" ou que \"dinheiro é sujo\". Nem um, nem outro.",
    }
    return fallbacks.get(tipo_slide, f"{nome} fala sobre {tema} para {publico}")


def formatar_carrossel(slides: list, tema: str) -> str:
    """Formata o carrossel como markdown para salvar."""
    contexto = carregar_contexto()
    nome = contexto.get('nome', 'Você')

    output = f"""---
name: "Carrossel: {tema}"
tipo: carrossel
tema: {tema}
slides: {len(slides)}
data: {datetime.now().strftime("%Y-%m-%d")}
---

# 🎠 {tema}

> Carrossel para Instagram | {len(slides)} slides

---

"""
    for i, slide in enumerate(slides, 1):
        output += f"""## Slide {i}/{len(slides)} — [{slide['tipo'].upper()}]

**🎯 Título do slide:** {slide['titulo']}

**📝 Texto:**
{slide['texto']}

**🎨 Sugestão visual:**
{slide['sugestao_visual']}

---

"""
    output += f"""---

💡 **Dicas para montar no Canva/Figma:**
- Use as cores da marca: {contexto.get('cores', '#FF6B6B, #4ECDC4')}
- Mantenha fonte legível (Montserrat Bold para título, Open Sans para corpo)
- Cada slide deve ter no máximo 1 frase de destaque
- Use o template "Clean & Modern" do Canva

_Gerado pelo Agente Carrossel_
"""

    return output


def salvar_carrossel(tema: str, slides: list) -> str:
    """Salva o carrossel em arquivo."""
    ensure_output()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tema_seguro = tema.replace(' ', '-').lower()[:30]
    filename = f"{tema_seguro}_{timestamp}.md"
    filepath = OUTPUT_PATH / filename

    conteudo = formatar_carrossel(slides, tema)
    filepath.write_text(conteudo, encoding='utf-8')

    # Atualizar index
    index_path = OUTPUT_PATH / "index.md"
    existing = index_path.read_text(encoding='utf-8')
    novo_entry = f"- [{tema}](carrossel/{filename})\n"
    if "## Índice" not in existing:
        existing = existing.replace(
            "_Last updated:_",
            f"## Índice\n\n{novo_entry}\n_Last updated:_"
        )
    else:
        existing = existing.replace(
            "## Índice\n\n",
            f"## Índice\n\n{novo_entry}"
        )
    index_path.write_text(existing, encoding='utf-8')

    return filename


def listar_carrossel():
    """Lista carrosséis salvos."""
    ensure_output()
    carrossel_files = sorted(OUTPUT_PATH.glob("*.md"), reverse=True)

    print(f"\n[🎠 {len(carrossel_files)} carrosséis salvos]\n")
    for f in carrossel_files:
        print(f"  - {f.stem}")


def ler_carrossel(nome: str):
    """Lê e exibe um carrossel salvo."""
    caminho = OUTPUT_PATH / f"{nome}.md"
    if caminho.exists():
        print(caminho.read_text(encoding='utf-8'))
    else:
        print(f"Carrossel '{nome}' não encontrado.")


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("""
🎠 Agente Carrossel — OPB Sistema

USO:
  python main.py "tema do carrossel" [tipo] [num_slides]
  python main.py --listar
  python main.py --ler "nome"

TIPOS:
  educational     (padrão) - Conteúdo educativo, passo a passo
  inspirational   - Histórias e inspiração
  promotional     - Divulgação de produto/serviço
  engagement      - Perguntas e interação

EXEMPLOS:
  python main.py "IA para solopreneurs"
  python main.py "5 ferramentas de IA" educational 9
  python main.py "Minha jornada" inspirational
  python main.py --listar
""")
        return

    arg1 = sys.argv[1]

    if arg1 == "--listar":
        listar_carrossel()
        return

    if arg1 == "--ler" and len(sys.argv) > 2:
        ler_carrossel(sys.argv[2])
        return

    # Gerar carrossel
    tema = arg1
    tipo = sys.argv[2] if len(sys.argv) > 2 else "educational"
    num_slides = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else None

    print(f"🎠 Gerando carrossel...")
    print(f"Tema: {tema}")
    print(f"Tipo: {tipo}")
    if num_slides:
        print(f"Slides: {num_slides}")
    print("-" * 50)

    slides = gerar_carrossel(tema, tipo, num_slides)

    print(f"\n[🎠 {len(slides)} slides gerados]\n")
    for i, slide in enumerate(slides, 1):
        print(f"Slide {i} [{slide['tipo'].upper()}]")
        print(f"  🎯 {slide['titulo']}")
        print(f"  📝 {slide['texto'][:80]}...")
        print()

    # Salvar
    arquivo = salvar_carrossel(tema, slides)
    print(f"📁 Salvo em: acervo/carrossel/{arquivo}")


if __name__ == "__main__":
    main()