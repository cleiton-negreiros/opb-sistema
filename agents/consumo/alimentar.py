#!/usr/bin/env python3
"""
🧠 Alimentar Cérebro — OPB Sistema
Lê o conteúdo da área de transferência e processa via Agente de Consumo.
Uso: copie o texto do formulário e execute este script.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

PROJECT_PATH = Path(__file__).parent.parent.parent
sys.path.append(str(PROJECT_PATH / "utils"))

# Tenta ler do clipboard
def ler_clipboard():
    """Tenta ler da área de transferência de várias formas."""
    # Método 1: tkinter (disponível na maioria das instalações Python)
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        try:
            texto = root.clipboard_get()
            root.destroy()
            if texto and len(texto.strip()) > 10:
                return texto
        except Exception:
            pass
        root.destroy()
    except Exception:
        pass

    # Método 2: pyperclip
    try:
        import pyperclip
        texto = pyperclip.paste()
        if texto and len(texto.strip()) > 10:
            return texto
    except Exception:
        pass

    # Método 3: Windows via ctypes
    if sys.platform == 'win32':
        try:
            import ctypes
            from ctypes import wintypes

            if not ctypes.windll.user32.OpenClipboard(0):
                return None

            try:
                handle = ctypes.windll.user32.GetClipboardData(1)
                if handle:
                    data = ctypes.c_char_p(handle).value
                    if data:
                        texto = data.decode('utf-8', errors='ignore')
                        if texto and len(texto.strip()) > 10:
                            return texto
            finally:
                ctypes.windll.user32.CloseClipboard()
        except Exception:
            pass

    return None


def ler_arquivo_fallback():
    """Lê de um arquivo de input se o clipboard estiver vazio."""
    input_path = PROJECT_PATH / "input.txt"
    if input_path.exists():
        return input_path.read_text(encoding='utf-8')
    return None


def main():
    print("=" * 60)
    print("🧠 ALIMENTAR CÉREBRO — OPB Sistema")
    print("=" * 60)

    # 1. Tentar ler do clipboard
    print("\n📋 Tentando ler da área de transferência...")
    conteudo = ler_clipboard()

    # 2. Tentar ler do arquivo
    if not conteudo:
        print("⚠️ Área de transferência vazia, verificando arquivo input.txt...")
        conteudo = ler_arquivo_fallback()

    # 3. Pedir para colar
    if not conteudo:
        print("\n📝 Cole o conteúdo do formulário abaixo.")
        print("   (Cole tudo e pressione ENTER duas vezes quando terminar)\n")
        linhas = []
        while True:
            try:
                linha = input()
            except EOFError:
                break
            if linha == "":
                break
            linhas.append(linha)
        conteudo = "\n".join(linhas)

    if not conteudo or len(conteudo.strip()) < 20:
        print("❌ Nenhum conteúdo encontrado. Cole o texto do formulário e tente novamente.")
        sys.exit(1)

    print(f"✅ Conteúdo recebido ({len(conteudo)} caracteres)")
    print("-" * 60)

    # Processar com o Agente de Consumo
    from agents.consumo.main import analisar_conteudo, salvar_conhecimento, carregar_contexto

    print("\n🔄 Processando conteúdo...")
    contexto = carregar_contexto()

    # Detecção automática do tipo de conteúdo
    titulo = "Perfil Empreendedor Solo"
    if "posicionamento" in conteudo.lower():
        titulo = "Posicionamento do Empreendedor"
    elif "história" in conteudo.lower() or "historias" in conteudo.lower():
        titulo = "Histórias do Empreendedor"
    elif "habilidade" in conteudo.lower():
        titulo = "Habilidades do Empreendedor"
    elif "cosmovisão" in conteudo.lower() or "cosmovisao" in conteudo.lower():
        titulo = "Cosmovisão de Valores"
    elif "público" in conteudo.lower() or "publico" in conteudo.lower():
        titulo = "Público-Alvo Ideal"
    elif "narrativa" in conteudo.lower():
        titulo = "Narrativa Principal"

    analise = analisar_conteudo(conteudo, "completo", titulo=titulo, contexto=contexto)
    arquivo = salvar_conhecimento(analise, titulo)

    print(f"\n{'='*60}")
    print(f"🧠 CÉREBRO ALIMENTADO COM SUCESSO!")
    print(f"{'='*60}")
    print(f"📁 Arquivo: acervo/conhecimento/{Path(arquivo).name}")
    print(f"🧠 Contexto: context-brain/")
    tipo_gerado = "LLM" if any(analise.get("usou_llm", {}).values()) else "Fallback"
    print(f"📊 Tipo: {tipo_gerado}")
    print(f"\nPróximo passo: rode o Agente Carrossel para gerar conteúdo!")
    print(f"   python agents/carrossel/main.py \"tema do carrossel\"")


if __name__ == "__main__":
    main()