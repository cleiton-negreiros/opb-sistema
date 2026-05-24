#!/usr/bin/env python3
"""
Consultor de Negocios OPB — Agente de Estrategia e Insights Diarios

Uso:
    python main.py insight_diario           → Insights diarios baseados em todo o contexto
    python main.py revisao_contexto          → Revisao profunda de tudo que coletamos
    python main.py coordenacao_agentes       → Sugere quais agentes rodar e em que ordem
    python main.py planejamento_estrategico  → Consulta estrategica (original)
    python main.py <tipo> '[{"key":"val"}]'  → Com contexto extra
"""

import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime, date

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

sys.path.append(str(Path(__file__).parent.parent.parent / "utils"))
from context_loader import get_brain_context
from llm_provider import generate_text

PROJECT = Path(__file__).parent.parent.parent

# ============================================================
# LEITURA DE CONTEXTO
# ============================================================

def read_file(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding='utf-8')
    return ""

def read_markdown_section(text: str, section: str) -> str:
    """Extrai o conteudo de uma secao de markdown."""
    pattern = rf"##\s*{re.escape(section)}.*?\n(.*?)(?=\n##|\Z)"
    m = re.search(pattern, text, re.DOTALL)
    return m.group(1).strip() if m else ""

def load_full_context() -> dict:
    """Carrega TODO o contexto disponivel no cerebro."""
    ctx = {}

    # 1. Quem-sou (identidade, valores, tom, publico, missao, linha editorial)
    quem_sou = PROJECT / "negocio" / "governanca" / "quem-sou.md"
    ctx["identidade"] = read_file(quem_sou)
    ctx["nome"] = read_markdown_section(ctx["identidade"], "Identidade") or "Paz na Conta"
    ctx["missao"] = read_markdown_section(ctx["identidade"], "Missão") or ""
    ctx["posicionamento"] = read_markdown_section(ctx["identidade"], "Posicionamento") or ""
    ctx["visao"] = read_markdown_section(ctx["identidade"], "Visão") or ""

    # 2. Projetos ativos
    ativos = PROJECT / "negocio" / "projetos" / "ativos.md"
    ctx["projetos_ativos"] = read_file(ativos)

    # 3. Pesquisas realizadas
    pesquisas_dir = PROJECT / "acervo" / "pesquisas"
    ctx["pesquisas"] = []
    if pesquisas_dir.exists():
        for f in sorted(pesquisas_dir.glob("*.md"), reverse=True)[:3]:
            ctx["pesquisas"].append({"arquivo": f.name, "conteudo": read_file(f)[:2000]})

    # 4. Conhecimento processado
    conhecimento_dir = PROJECT / "acervo" / "conhecimento"
    ctx["conhecimento"] = []
    if conhecimento_dir.exists():
        ctx["conhecimento"] = [f.name for f in conhecimento_dir.glob("*.md")]

    # 5. Regras de governanca
    regras_dir = PROJECT / "negocio" / "governanca" / "regras"
    ctx["regras"] = []
    if regras_dir.exists():
        ctx["regras"] = [f.stem for f in regras_dir.glob("*.md")]

    # 6. Linha editorial
    linha = PROJECT / "negocio" / "governanca" / "linha-editorial.md"
    ctx["linha_editorial"] = read_file(linha)[:1500] if linha.exists() else ""

    # 7. Brain context via loader
    ctx["brain_context"] = get_brain_context()

    # 8. Outputs de consultorias anteriores
    consultorias_dir = PROJECT / "output" / "consultoria"
    ctx["consultorias_anteriores"] = []
    if consultorias_dir.exists():
        ctx["consultorias_anteriores"] = sorted(
            [f.name for f in consultorias_dir.glob("*.md")], reverse=True
        )[:5]

    return ctx

def format_context_for_prompt(ctx: dict) -> str:
    """Formata o contexto para injecao no prompt do LLM."""
    parts = []
    parts.append(f"## IDENTIDADE\n{ctx.get('nome', '')}")
    parts.append(f"Missao: {ctx.get('missao', '')}")
    parts.append(f"Visao: {ctx.get('visao', '')}")
    parts.append(f"Posicionamento: {ctx.get('posicionamento', '')[:300]}")

    parts.append(f"\n## PROJETOS ATIVOS\n{ctx.get('projetos_ativos', 'Nenhum')}")
    parts.append(f"\n## LINHA EDITORIAL\n{ctx.get('linha_editorial', '')[:1000]}")

    if ctx.get("pesquisas"):
        parts.append("\n## PESQUISAS RECENTES")
        for p in ctx["pesquisas"]:
            parts.append(f"\n--- {p['arquivo']} ---\n{p['conteudo'][:1000]}")

    if ctx.get("consultorias_anteriores"):
        parts.append(f"\n## CONSULTORIAS ANTERIORES\n{', '.join(ctx['consultorias_anteriores'])}")

    brain = ctx.get("brain_context", "")
    if brain:
        parts.append(f"\n## BRAIN CONTEXT\n{brain}")

    return "\n".join(parts)

# ============================================================
# PROMPTS
# ============================================================

INSIGHT_DIARIO_PROMPT = """Voce e um consultor de negocios catolico. Analise TODO o contexto abaixo e gere um relatorio de insights diarios.

CONTEXTO:
{context}

INSTRUCOES:
1. Identifique OS 3 INSIGHTS mais relevantes do contexto para o dia de hoje
2. Para cada insight, explique POR QUE ele e importante e QUAL acao pratica tomar
3. Sugira 1 pergunta reflexiva para o empreendedor pensar durante o dia
4. Aponte 1 oportunidade imediata que esta sendo negligenciada
5. De uma "dica do dia" pratica e acionavel

FORMATO:
- Seja direto, pratico e acionavel
- Use linguagem clara sem jargao
- Numere os insights claramente
- Termine com uma frase de fecho inspiradora alinhada com a fe catolica (sem prosperidade)
- Inclua a data: {data}"""

REVISAO_CONTEXTO_PROMPT = """Voce e um consultor de negocios catolico. Faca uma REVISAO PROFUNDA de todo o contexto coletado ate agora.

CONTEXTO:
{context}

INSTRUCOES:
1. GAP ANALYSIS: O que esta faltando no contexto atual? (pesquisas nao feitas, dados nao coletados, decisoes pendentes)
2. OPORTUNIDADES: Quais sao as 3 maiores oportunidades que o contexto revela?
3. RISCOS: Quais sao os 2 principais riscos ou ameacas identificaveis?
4. PROXIMA ACAO: Qual e A UNICA coisa mais importante que deveria ser feita hoje para avancar?
5. AGENDA SUGERIDA: Sugira uma sequencia de acoes para os proximos 7 dias
6. AGENTES: Quais agentes do sistema seriam mais uteis para avancar em cada item?

Seja especifico. Nao de conselhos genericos. Use dados reais do contexto. Data: {data}"""

COORDENACAO_AGENTES_PROMPT = """Voce e um coordenador de agentes de IA. Analise o contexto do projeto e sugira quais agentes executar e em que ordem.

CONTEXTO:
{context}

AGENTES DISPONIVEIS:
- carrossel: Gera carrosseis para Instagram (4 tipos)
- capa_video: Gera ideias de thumbnail YouTube
- consumo: Processa textos, PDFs, URLs (5 tipos de analise)
- text_generator: Gera posts Instagram (educational, inspirational, promotional, engagement)
- posicionamento: Analisa concorrentes e posicionamento de mercado
- transcricao: Transcreve videos do YouTube
- radagast: Curadoria diaria via yt-dlp + RSS (gratuito)
- narvi: Edicao de video com FFmpeg
- consultor-negocios: Consultoria estrategica e insights
- audio-transcriber: Transcreve audios do Telegram
- telegram_bot: Interface Telegram

INSTRUCOES:
1. Sugira uma SEQUENCIA otimizada de agentes para executar HOJE
2. Para cada agente, explique POR QUE executa-lo agora
3. Identifique DEPENDENCIAS entre agentes (ex: precisa de transcricao antes de consumo)
4. Estime o IMPACTO de cada execucao (alto/medio/baixo)
5. Indique se algum agente pode ser IGNORADO hoje e por que

FORMATO:
- Tabela simples: Ordem | Agente | Motivo | Impacto | Dependencia
- Priorize o que gera conteudo publicavel primeiro
- Data: {data}"""

# ============================================================
# GERACAO
# ============================================================

def build_prompt(consultation_type: str, ctx: dict) -> str:
    context = format_context_for_prompt(ctx)
    data = date.today().strftime('%d/%m/%Y')

    prompts = {
        "insight_diario": INSIGHT_DIARIO_PROMPT,
        "revisao_contexto": REVISAO_CONTEXTO_PROMPT,
        "coordenacao_agentes": COORDENACAO_AGENTES_PROMPT,
    }

    template = prompts.get(consultation_type)
    if not template:
        # fallback para tipos originais
        context_str = get_brain_context()
        if not context_str:
            context_str = f"Data: {data}"
        return f"""Voce e um consultor de negocios catolico. Responda a consulta: {consultation_type}
Contexto: {context_str}
Seja pratico e alinhado com valores catolicos."""

    return template.format(context=context, data=data)


def generate_advice(consultation_type: str, context_data: dict = None) -> str:
    ctx = load_full_context()
    if context_data:
        ctx.update(context_data)

    prompt = build_prompt(consultation_type, ctx)

    print(f"[consultor] Gerando {consultation_type}...", file=sys.stderr)

    try:
        result = generate_text(prompt)
        if result and result.strip():
            return result.strip()
    except Exception as e:
        print(f"[consultor] Erro no LLM: {e}", file=sys.stderr)

    return fallback_advice(consultation_type)


def fallback_advice(consultation_type: str) -> str:
    """Fallback textual quando LLM falha."""
    hoje = date.today().strftime('%d/%m/%Y')
    base = f"""---\nData: {hoje}\nTipo: {consultation_type}\n---"""

    if consultation_type == "insight_diario":
        return base + """

## Insight 1 — Contexto carregado com sucesso
O sistema esta operacional e todo o contexto do cerebro foi carregado. Continue alimentando o cerebro com novas pesquisas e conhecimentos para que os insights fiquem cada vez mais precisos.

## Insight 2 — Revisar projetos ativos
Verifique o arquivo negocio/projetos/ativos.md e atualize o status de cada projeto. Manter os projetos atualizados e a chave para o coordenador priorizar corretamente.

## Insight 3 — Producao de conteudo
O Paz na Conta precisa de conteudo novo. Considere usar o text_generator ou carrossel para produzir um post educativo hoje.

## Acao pratica do dia
Identifique 1 tarefa que leva menos de 15 minutos e execute agora.

## Oportunidade imediata
Os dados de concorrentes e pesquisas coletados podem virar um carrossel comparativo de alto engajamento.

## Dica do dia
Pequenas acoes consistentes vencem grandes acoes esporadicas.

*Confie no processo. Deus da o crescimento.*"""

    elif consultation_type == "revisao_contexto":
        return base + """

## Gaps Identificados
1. Nao ha metricas claras de desempenho dos agentes (quantos posts gerados, quantas transcricoes, etc.)
2. As pesquisas de mercado precisam ser atualizadas regularmente
3. Faltam definicoes claras de KPIs para cada projeto ativo

## Oportunidades
1. O nicho de financas catolicas tem pouca concorrencia organizada no Brasil
2. O material de pesquisa coletado pode ser reaproveitado em multiplos formatos
3. A integracao com Telegram permite capturar ideias 24h

## Riscos
1. Dependencia de unico modelo de IA (tinyllama) — considerar fallback
2. Conteudo parado = audiencia perdida

## Proxima Acao
Definir e documentar as metricas de cada agente em um arquivo de acompanhamento.

*Nada substitui a acao consistente.*"""

    elif consultation_type == "coordenacao_agentes":
        return base + """

| Ordem | Agente | Motivo | Impacto | Dependencia |
|-------|--------|--------|---------|-------------|
| 1 | consultor-negocios (insight_diario) | Aquecer o cerebro com contexto do dia | Alto | Nenhuma |
| 2 | radagast | Coletar novas ideias do mercado | Alto | Nenhuma |
| 3 | text_generator | Produzir post do dia com base nos insights | Alto | Insight diario |
| 4 | consumo | Processar conteudo coletado pelo radagast | Medio | Radagast |
| 5 | carrossel | Gerar carrossel educativo semanal | Medio | Nenhuma |

## Ignorar hoje
- narvi: So quando houver video bruto para editar
- audio-transcriber: So quando houver audio novo no Telegram
- posicionamento: So quando houver novos concorrentes para analisar

*Coordene com sabedoria. Nem tudo precisa ser feito hoje.*"""

    return base + f"\n\nConsulta '{consultation_type}' realizada. Contexto carregado com {len(base)} caracteres."


def save_advice(advice: str, consultation_type: str) -> str:
    output_dir = PROJECT / "output" / "consultoria"
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"consultoria_{consultation_type}_{ts}.md"
    path.write_text(
        f"""# Consultoria OPB
**Tipo**: {consultation_type}
**Data**: {datetime.now().strftime('%d/%m/%Y %H:%M')}

---
{advice}
---
*Gerado pelo Consultor de Negocios OPB*
""", encoding='utf-8')
    return str(path)


# ============================================================
# CLI
# ============================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    consultation_type = sys.argv[1]
    context_data = None
    if len(sys.argv) > 2:
        try:
            context_data = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            context_data = {"user_input": sys.argv[2]}

    print(f"[consultor] Consulta: {consultation_type}")
    print(f"[consultor] Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("-" * 50)

    advice = generate_advice(consultation_type, context_data)
    print(advice)
    print("-" * 50)

    path = save_advice(advice, consultation_type)
    print(f"[consultor] Salvo em: {path}")


if __name__ == "__main__":
    main()
