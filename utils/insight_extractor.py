"""
Insight Extractor - Utilitário compartilhado
Extrai insights, tom e análise de textos de transcrições.

Uso:
    from utils.insight_extractor import extract_insights
    resultado = extract_insights(texto_da_transcricao)
"""

import re
from typing import Dict, List


def extract_insights(text: str) -> Dict:
    """Extrai insights, tom e análise de um texto de transcrição."""
    if not text or len(text.strip()) < 20:
        return {
            "insights": [],
            "tom": "neutro",
            "resumo": "",
            "keywords": [],
            "total_palavras": 0,
            "tempo_leitura_min": 0,
            "sentimento_geral": "neutro",
            "analise_tons": {}
        }

    text_lower = text.lower()
    words = re.findall(r'\b\w{4,}\b', text_lower)
    word_freq = {}
    for w in words:
        word_freq[w] = word_freq.get(w, 0) + 1
    sorted_words = sorted(word_freq.items(), key=lambda x: -x[1])
    keywords = [w for w, c in sorted_words[:15]]

    # Detecção de tom
    tom_palavras = {
        "otimista": ["esperanca", "confianca", "acreditar", "futuro", "bom", "otimo",
                     "feliz", "alegria", "conseguir", "vitoria", "vencer", "positivo",
                     "crescimento", "oportunidade", "transformacao", "milagre"],
        "preocupado": ["medo", "preocupado", "ansioso", "dificil", "problema", "crise",
                       "perigo", "risco", "cuidado", "atencao", "urgente", "batalha"],
        "informativo": ["saber", "entender", "explicar", "mostrar", "conceito",
                        "dado", "informacao", "estudo", "pesquisa", "analise"],
        "reflexivo": ["pensar", "refletir", "sentido", "vida", "proposito",
                      "coracao", "alma", "verdade", "deus", "fe", "espiritual"],
        "motivacional": ["poder", "capacidade", "potencial", "acreditar", "sonho",
                         "coragem", "forca", "determinacao", "persistir",
                         "superar", "transformar", "mudar", "agir"]
    }

    contagem_tons = {}
    for tom, palavras in tom_palavras.items():
        contagem = sum(text_lower.count(p) for p in palavras)
        if contagem > 0:
            contagem_tons[tom] = contagem

    tom_dominante = "neutro"
    if contagem_tons:
        tom_dominante = max(contagem_tons, key=contagem_tons.get)

    # Extrair frases relevantes para insights
    frases = re.split(r'[.!?]+', text)
    frases = [f.strip() for f in frases if len(f.strip()) > 30]

    palavras_chave_insight = [
        "importante", "principal", "essencial", "fundamental", "crucial",
        "dica", "segredo", "aprender", "descobrir", "perceber", "lembrar",
        "nunca", "sempre", "precisa", "deve", "atencao", "cuidado",
        "oportunidade", "diferenca", "atencao"
    ]

    insights = []
    for frase in frases:
        for palavra in palavras_chave_insight:
            if palavra in frase.lower():
                insights.append(frase.strip())
                break

    insights = insights[:5]
    if not insights:
        insights = frases[:3] if frases else []

    # Resumo automático
    resumo = ""
    for frase in frases[:3]:
        if len(resumo) + len(frase) < 300:
            resumo += frase + ". "

    total_palavras = len(text.split())
    tempo_leitura = total_palavras / 200 if total_palavras > 0 else 0

    return {
        "insights": insights,
        "tom": tom_dominante,
        "todos_tons": contagem_tons,
        "resumo": resumo.strip(),
        "keywords": keywords,
        "total_palavras": total_palavras,
        "tempo_leitura_min": round(tempo_leitura, 1),
        "sentimento_geral": tom_dominante,
        "analise_tons": contagem_tons
    }


def extract_timestamps(text: str) -> List[Dict]:
    """Extrai timestamps de um texto formatado como [MM:SS] ou [HH:MM:SS]."""
    pattern = r'\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*(.*)'
    matches = re.findall(pattern, text)
    result = []
    for timestamp, content in matches:
        result.append({
            "timestamp": timestamp,
            "text": content.strip()
        })
    return result
