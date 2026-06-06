#!/usr/bin/env python3
"""
Instagram Text Generator Agent
Generates engaging Instagram post text based on business context and objectives.
"""

import sys
import os
from pathlib import Path
import json

# Set UTF-8 encoding for output to handle emojis on Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent.parent / "utils"))
sys.path.append(str(Path(__file__).parent.parent.parent))

from context_loader import get_brain_context, get_business_value
from llm_provider import generate_text
from utils.multi_profile import resolve_profile_id, parse_perfil_arg

def load_templates():
    """Load text templates for different post types."""
    templates_dir = Path(__file__).parent / "templates"
    templates = {}
    
    if templates_dir.exists():
        for template_file in templates_dir.glob("*.j2"):
            with open(template_file, 'r', encoding='utf-8') as f:
                templates[template_file.stem] = f.read()
    else:
        # Default templates if none exist
        templates = {
            "educational": "Crie um post educativo para Instagram sobre {topic}. Tom de voz: {tone}. Público-alvo: {audience}. Valores a incorporar: {values}. Máximo 125 caracteres.",
            "inspirational": "Crie um post inspirador para Instagram sobre {topic}. Tom de voz: {tone}. Público-alvo: {audience}. Valores a incorporar: {values}. Máximo 125 caracteres.",
            "promotional": "Crie um post promocional para Instagram sobre {topic}. Tom de voz: {tone}. Público-alvo: {audience}. Valores a incorporar: {values}. Máximo 125 caracteres.",
            "engagement": "Crie um post que engaje a audiência para Instagram sobre {topic}. Tom de voz: {tone}. Público-alvo: {audience}. Valores a incorporar: {values}. Máximo 125 caracteres."
        }
    
    return templates

def generate_instagram_post(objective: str, post_type: str = "educational", profile_id: str = None) -> str:
    """
    Generate an Instagram post based on objective and context.

    Args:
        objective: The goal/topic of the post (e.g., "educar sobre produtividade")
        post_type: Type of post (educational, inspirational, promotional, engagement)
        profile_id: id do perfil (multi-perfil). Se None, usa o perfil ativo.

    Returns:
        Generated Instagram post text
    """
    pid = resolve_profile_id(profile_id)
    brain = get_brain_context(pid)
    tone = get_business_value("tom_de_voz", "direto e inspirador", pid)
    audience = get_business_value("publico_alvo", "empreendedores", pid)
    values = get_business_value("valores", [], pid)
    values_str = ", ".join(values) if values else "autenticidade e praticidade"

    templates = load_templates()
    template = templates.get(post_type, templates["educational"])
    prompt = template.format(
        topic=objective,
        tone=tone,
        audience=audience,
        values=values_str,
        context=brain or f"Negócio voltado para {audience}"
    )
    
    # Generate text using LLM
    try:
        generated_text = generate_text(prompt)
        return generated_text.strip()
    except Exception as e:
        # Fallback template-based generation if LLM fails
        return f"""💡 DICA RÁPIDA: {objective.capitalize()}

Lembre-se de aplicar esses princípios no seu dia a dia:
1. Comece pequeno, mas comece hoje
2. Foque no progresso, não na perfeição
3. Celebre cada conquista, por menor que seja

Como isso se aplica ao seu negócio? Compartilhe nos comentários! 👇

#produtividade #empreendedorismo #dicas"""

def save_post(text: str, filename: str = None) -> str:
    """
    Save generated post to output directory.
    
    Args:
        text: The generated post text
        filename: Optional filename (defaults to timestamp-based)
        
    Returns:
        Path to saved file
    """
    output_dir = Path(__file__).parent.parent.parent / "output" / "text_posts"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if filename is None:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"post_{timestamp}.txt"
    
    output_path = output_dir / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    return str(output_path)

def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<objective>\" [post_type] [--perfil <id>]")
        print("Example: python main.py \"educar sobre organização de tempo\" educational")
        sys.exit(1)

    profile_id, args = parse_perfil_arg(sys.argv[1:])
    pid = resolve_profile_id(profile_id)
    if not args:
        print("Erro: objetivo é obrigatório")
        sys.exit(1)
    objective = args[0]
    post_type = args[1] if len(args) > 1 else "educational"

    print(f"Gerando post do Instagram...")
    print(f"Objetivo: {objective}")
    print(f"Tipo: {post_type}")
    print(f"Perfil: {pid}")
    print("-" * 50)

    try:
        post_text = generate_instagram_post(objective, post_type, pid)
        print("Post gerado:")
        print(post_text)
        print("-" * 50)

        # Save post
        saved_path = save_post(post_text)
        print(f"Post salvo em: {saved_path}")
        
    except Exception as e:
        print(f"Erro ao gerar post: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()