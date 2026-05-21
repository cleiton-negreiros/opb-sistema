import json
import os

def load_content_plan():
    script_dir = os.path.dirname(__file__)
    line_editorial_path = os.path.join(script_dir, "..", "..", "negocio", "governanca", "linha-editorial.md")
    
    with open(line_editorial_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Simple parsing for now, can be improved later
    plan = {"pilares": [], "cronograma": []}
    
    # Extracting pillars (basic example)
    pilares_section = content.split("## Pilares de Conteúdo")[1].split("## Cronograma Sugerido")[0]
    lines = pilares_section.split("\n")
    
    current_pilar = None
    for line in lines:
        if line.startswith("| ") and "|" in line[2:]:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) == 4 and parts[0] != "Pilar": # Skip header
                pilar_name = parts[0].replace("**", "").strip()
                plan["pilares"].append({
                    "nome": pilar_name,
                    "foco": parts[1],
                    "temas_originais": parts[2],
                    "novas_ideias": parts[3]
                })

    # Extracting cronograma (basic example)
    cronograma_section = content.split("## Cronograma Sugerido (Primeiro Mês)")[1]
    lines = cronograma_section.split("\n")

    for line in lines:
        if line.startswith("| ") and "|" in line[2:]:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) == 3 and parts[0] != "Semana": # Skip header
                plan["cronograma"].append({
                    "semana": parts[0].replace("**", "").strip(),
                    "youtube": parts[1],
                    "instagram": parts[2]
                })

    return plan

def generate_briefing(theme, format_type):
    plan = load_content_plan()
    briefing = {"theme": theme, "format": format_type, "details": ""}
    
    # Find theme in pillars or cronograma
    found = False
    for pilar in plan["pilares"]:
        if theme in pilar["temas_originais"] or theme in pilar["novas_ideias"]:
            briefing["details"] += f"Pilar: {pilar['nome']}\n"
            briefing["details"] += f"Foco: {pilar['foco']}\n"
            briefing["details"] += f"Temas Originais: {pilar['temas_originais']}\n"
            briefing["details"] += f"Novas Ideias: {pilar['novas_ideias']}\n"
            found = True
            break
    
    for item in plan["cronograma"]:
        if theme in item["youtube"] or theme in item["instagram"]:
            briefing["details"] += f"Semana do Cronograma: {item['semana']}\n"
            briefing["details"] += f"Conteúdo YouTube: {item['youtube']}\n"
            briefing["details"] += f"Conteúdo Instagram: {item['instagram']}\n"
            found = True
            break

    if not found:
        briefing["details"] += "Tema não encontrado no plano de conteúdo. Por favor, forneça mais detalhes.\n"

    # Add general editorial line
    script_dir = os.path.dirname(__file__)
    line_editorial_path = os.path.join(script_dir, "..", "..", "negocio", "governanca", "linha-editorial.md")
    with open(line_editorial_path, "r", encoding="utf-8") as f:
        full_editorial = f.read()
    
    briefing["details"] += "\n---\nLinha Editorial Geral:\n"
    briefing["details"] += full_editorial.split("## Tom e tomada de posição")[1].split("--- References")[0]

    return briefing

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        theme = sys.argv[1]
        format_type = sys.argv[2]
        brief = generate_briefing(theme, format_type)
        print(json.dumps(brief, indent=2, ensure_ascii=False))
    elif len(sys.argv) == 2 and sys.argv[1] == "load_plan":
        plan = load_content_plan()
        print(json.dumps(plan, indent=2, ensure_ascii=False))
    else:
        print("Uso: python main.py <tema> <formato> ou python main.py load_plan")
