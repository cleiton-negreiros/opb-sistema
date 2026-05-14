#!/usr/bin/env python3
"""
🧠 Alimentar Cérebro via API
Executado internamente pelo api_server.py
"""

import sys
import json
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent.resolve()
sys.path.append(str(PROJECT_PATH / "utils"))


def main(input_text: str, tipo: str = "completo", titulo: str = "Conteúdo"):
    """Processa conteúdo e alimenta o cérebro."""
    try:
        from agents.consumo.main import analisar_conteudo, salvar_conhecimento, carregar_contexto

        contexto = carregar_contexto()
        analise = analisar_conteudo(input_text, tipo, titulo=titulo, contexto=contexto)
        arquivo = salvar_conhecimento(analise, titulo)

        return {
            "sucesso": True,
            "arquivo": str(arquivo),
            "mensagem": f"✅ Conhecimento salvo: {arquivo}"
        }
    except Exception as e:
        return {
            "sucesso": False,
            "erro": str(e),
            "mensagem": f"❌ Erro: {e}"
        }


if __name__ == "__main__":
    # Recebe argumentos do api_server.py
    input_text = sys.argv[1] if len(sys.argv) > 1 else ""
    tipo = sys.argv[2] if len(sys.argv) > 2 else "completo"
    titulo = sys.argv[3] if len(sys.argv) > 3 else "Conteúdo"

    resultado = main(input_text, tipo, titulo)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))