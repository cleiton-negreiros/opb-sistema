#!/usr/bin/env python3
"""
Business Consultant Agent for OPB Sistema
Provides strategic business advice for managing multiple businesses with Catholic values.
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Set UTF-8 encoding for output to handle emojis on Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent.parent / "utils"))

from context_loader import get_brain_context, get_business_value
from llm_provider import generate_text

def load_templates():
    """Load consulting templates for different business advice types."""
    # Default templates - always available
    templates = {
        "planejamento_estrategico": "Você é um consultor de negócios especializado em finanças católicas, música com propósito e formação espiritual. Ajude o empreendedor a criar um plano estratégico integrado para seus 3 negócios: Paz na Conta (finanças pessoais católicas), Toque de Paz (música e louvor com propósito) e Caminho Vida (formação e espiritualidade católica). Considere o contexto atual: {context}. Forneça recomendações específicas para cada negócio e como eles podem se apoiar mutuamente.",
        "analise_swot": "Realize uma análise SWOT (Forças, Fraquezas, Oportunidades, Ameaças) para o negócio específico: {business_name}. Considere o contexto católico e os valores da Doutrina Social da Igreja. Contexto atual: {context}",
        "planejamento_conteudo": "Crie um calendário editorial integrado para os 3 negócios considerando o calendário litúrgico católico. Negócios: Paz na Conta (finanças), Toque de Paz (música), Caminho Vida (formação). Período: {timeframe}. Objetivos: {objectives}",
        "otimizacao_tempo": "Sugira um sistema de gestão de tempo e produtividade para um empreendedor solo gerenciando 3 negócios diferentes. Considere principios de stewardship católico e equilíbrio vida-trabalho. Desafios específicos: {challenges}",
        "metricas_kpis": "Defina métricas e KPIs específicos para cada um dos 3 negócios considerando sua natureza católica e missionária. Negócios: Paz na Conta (finanças pessoais), Toque de Paz (música/louvor), Caminho Vida (formação/espiritualidade). Inclua métricas qualitativas e quantitativas.",
        "consulta_geral": "Você é um consultor de negócios especializado em empreendedorismo católico. Responda à seguinte pergunta considerando os 3 negócios do empreendedor (Paz na Conta, Toque de Paz, Caminho Vida) e os princípios da Doutrina Social da Igreja: {question}"
    }
    
    # Try to load external templates if they exist (for customization)
    templates_dir = Path(__file__).parent / "templates"
    if templates_dir.exists():
        for template_file in templates_dir.glob("*.j2"):
            with open(template_file, 'r', encoding='utf-8') as f:
                templates[template_file.stem] = f.read()
    
    return templates

def generate_business_advice(consultation_type: str, context_data: dict = None) -> str:
    """
    Generate business advice based on consultation type and context.
    
    Args:
        consultation_type: Type of advice needed (planejamento_estrategico, analise_swot, etc.)
        context_data: Optional dictionary with specific context information
        
    Returns:
        Generated business advice text
    """
    context_str = get_brain_context()
    if context_str:
        context_str += f" | Data: {datetime.now().strftime('%d/%m/%Y')}"
    else:
        context_str = f"Data da Consulta: {datetime.now().strftime('%d/%m/%Y')}"
    
    # Add specific context data if provided
    if context_data:
        context_str += f"\nDados Específicos: {json.dumps(context_data, indent=2, ensure_ascii=False)}"
    
    # Load templates
    templates = load_templates()
    print(f"DEBUG: Available templates: {list(templates.keys())}")
    print(f"DEBUG: Looking for consultation_type: '{consultation_type}'")
    template = templates.get(consultation_type, templates["consulta_geral"])
    print(f"DEBUG: Selected template - using key: '{consultation_type if consultation_type in templates else 'consulta_geral'}'")
    
    # Format prompt based on consultation type
    if consultation_type == "planejamento_estrategico":
        prompt = template.format(context=context_str)
    elif consultation_type == "analise_swot":
        business_name = context_data.get("business_name", "negócio não especificado") if context_data else "negócio não especificado"
        prompt = template.format(business_name=business_name, context=context_str)
    elif consultation_type == "planejamento_conteudo":
        timeframe = context_data.get("timeframe", "trimestre") if context_data else "trimestre"
        objectives = context_data.get("objectives", "educar, engajar e converter") if context_data else "educar, engajar e converter"
        prompt = template.format(timeframe=timeframe, objectives=objectives, context=context_str)
    elif consultation_type == "otimizacao_tempo":
        challenges = context_data.get("challenges", "equilibrar três áreas de atuação diferentes") if context_data else "equilibrar três áreas de atuação diferentes"
        prompt = template.format(challenges=challenges, context=context_str)
    elif consultation_type == "metricas_kpis":
        prompt = template.format(context=context_str)
    elif consultation_type == "consulta_geral":
        question = context_data.get("question", "Como posso melhorar meus negócios?") if context_data else "Como posso melhorar meus negócios?"
        prompt = template.format(question=question, context=context_str)
    else:
        # Default fallback
        prompt = f"""Você é um consultor de negócios católico. Forneça orientação sobre: {consultation_type}
        
        Contexto:
        {context_str}
        
        Seja específico, prático e alinhado com os valores catholiques."""
    
    # Generate text using LLM
    print(f"DEBUG: About to generate text with prompt length: {len(prompt)}")
    try:
        generated_text = generate_text(prompt)
        print(f"DEBUG: Text generation successful, length: {len(generated_text)}")
        return generated_text.strip()
    except Exception as e:
        print(f"DEBUG: Error in text generation: {e}")
        # Fallback response if LLM fails
        return f"""⚠️  Consultoria Temporariamente Indisponível
        
        Enquanto nosso sistema de IA está passando por manutenção, aqui estão alguns princípios básicos:

        Para seus 3 negócios:
        1. **Paz na Conta**: Mantenha o foco na educação financeira católica - ensine antes de lucrar
        2. **Toque de Paz**: Que a música sempre sirva ao louvor, nunca ao entretenimento vazio
        3. **Caminho Vida**: A formação deve levar ao encontro com Cristo, não apenas à informação

        Princípio unificador: Buscai primeiro o Reino de Deus e a sua justiça, e todas estas coisas vos serão acrescentadas. (Mt 6,33)

        Erro técnico: {str(e)}"""

def save_advice(advice: str, consultation_type: str = None) -> str:
    """
    Save generated advice to output directory.
    
    Args:
        advice: The generated advice text
        consultation_type: Type of consultation (for filename)
        
    Returns:
        Path to saved file
    """
    output_dir = Path(__file__).parent.parent.parent / "output" / "consultoria"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if consultation_type is None:
        consultation_type = "consulta_geral"
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"consultoria_{consultation_type}_{timestamp}.md"
    
    output_path = output_dir / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"""# Consulta de Negócios - OPB Sistema
**Tipo**: {consultation_type}
**Data**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
**Base**: Consultor de Negócios Católico

---

{advice}

---
*Gerado pelo Sistema OPB - Consultor de Negócios*
""")
    
    return str(output_path)

def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<consultation_type>\" [context_json]")
        print("Consultation types: planejamento_estrategico, analise_swot, planejamento_conteudo, otimizacao_tempo, metricas_kpis, consulta_geral")
        print('Example: python main.py "planejamento_estrategico" \'{"focus": "expansão"}\'')
        sys.exit(1)
    
    consultation_type = sys.argv[1]
    context_data = None
    
    if len(sys.argv) > 2:
        try:
            context_data = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            context_data = {"user_input": sys.argv[2]}
    
    print("Consultor de Negocios OPB")
    print("Tipo de consulta: {}".format(consultation_type))
    if context_data:
        print("Contexto fornecido: {}".format(json.dumps(context_data, ensure_ascii=False)))
    print("-" * 50)
    
    try:
        advice = generate_business_advice(consultation_type, context_data)
        # Handle emojis that might cause encoding issues on Windows console
        safe_advice = advice.encode('utf-8', errors='replace').decode('utf-8')
        print("Consulta realizada:")
        print(safe_advice)
        print("-" * 50)
        
        # Save advice
        saved_path = save_advice(advice, consultation_type)
        print(f"Consulta salva em: {saved_path}")
        
    except Exception as e:
        # Handle emojis in error messages too
        safe_error = str(e).encode('utf-8', errors='replace').decode('utf-8')
        print(f"Erro ao realizar consulta: {safe_error}")
        sys.exit(1)

if __name__ == "__main__":
    main()