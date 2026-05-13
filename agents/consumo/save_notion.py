#!/usr/bin/env python3
"""Quick script to save Notion content to acervo and create template."""
import sys
sys.path.insert(0, '/'.join(__file__.replace('\\','/').split('/')[:-1]))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "utils"))

from pathlib import Path
from datetime import datetime

PROJECT_PATH = Path(__file__).parent.parent.parent
ACERVO_PATH = PROJECT_PATH / "acervo" / "conhecimento"

ACERVO_PATH.mkdir(parents=True, exist_ok=True)

conteudo = """# Cosmovisão de Valores

## 🎯 O que é
Definir como você vê o mundo, o trabalho, a disciplina e o que guia suas escolhas.

## ⭐ Por que importa
Sua visão molda seu conteúdo e atrai o público certo.

## 🧭 Como fazer
1. Escreva 10 crenças pessoais.
2. Liste 5 valores inegociáveis.
3. Relacione como isso influencia seu conteúdo.

## 📌 Checklist
- [ ] Listei 10 crenças
- [ ] Defini 5 valores
- [ ] Conectei isso ao meu conteúdo

## 🎁 Resultado
Uma identidade sólida e coerente.

## 📝 Exemplo prático

**Crenças:**
- "Disciplina transforma mais que talento."
- "Todo mundo tem algo ensinável."
- "Produtividade é clareza, não correria."

**Valores:**
- Honestidade
- Constância
- Simplicidade
- Responsabilidade

---

*Extraído da página do Notion — processado pelo Agente de Consumo*"""

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"cosmovisao-valores_{timestamp}.md"
filepath = ACERVO_PATH / filename
filepath.write_text(conteudo, encoding='utf-8')

# Atualizar index
index_path = ACERVO_PATH / "index.md"
if index_path.exists():
    content = index_path.read_text(encoding='utf-8')
    if "## Índice" in content:
        content = content.replace("## Índice\n\n", f"## Índice\n\n- [Cosmovisão de Valores](conhecimento/{filename})\n")
    else:
        content = content.replace("_Last updated:_", f"## Índice\n\n- [Cosmovisão de Valores](conhecimento/{filename})\n\n_Last updated:_")
    index_path.write_text(content, encoding='utf-8')

print(f"✅ Salvo: {filename}")