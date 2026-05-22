#!/usr/bin/env python3
"""
Agente Litúrgico - Paz na Conta
Gera sugestões de conteúdo alinhadas ao calendário litúrgico católico
combinadas com temas de finanças pessoais.
"""

import json
import math
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Paths
AGENT_DIR = Path(__file__).parent
CALENDARIO_FILE = AGENT_DIR / "calendario.json"
IDEIAS_DIR = AGENT_DIR / "acervo" / "ideias"
SOUL_FILE = AGENT_DIR / "SOUL.md"

IDEIAS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# CÁLCULO DA PÁSCOA - Algoritmo Gregoriano Anônimo
# ============================================================

def calcular_pascoa(ano):
    """Calcula a data da Páscoa usando o algoritmo de Anonymous Gregorian."""
    a = ano % 19
    b = ano // 100
    c = ano % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return datetime(ano, mes, dia)


def datas_moveis(ano):
    """Calcula datas móveis baseadas na Páscoa."""
    pascoa = calcular_pascoa(ano)

    return {
        "pascoa": pascoa,
        "quarta_cinzas": pascoa - timedelta(days=46),
        "domingo_ramos": pascoa - timedelta(days=7),
        "quinta_santa": pascoa - timedelta(days=3),
        "sexta_santa": pascoa - timedelta(days=2),
        "sabado_aleluia": pascoa - timedelta(days=1),
        "ascensao": pascoa + timedelta(days=39),
        "pentecostes": pascoa + timedelta(days=49),
        "santissima_trindade": pascoa + timedelta(days=56),
        "corpus_christi": pascoa + timedelta(days=60),
        "cristo_rei": pascoa + timedelta(days=210),  # 34 semanas após Pentecostes
    }


def calcular_inicio_advento(ano):
    """Calcula o 1º Domingo do Advento (domingo mais próximo de 30/11)."""
    natal = datetime(ano, 12, 25)
    # Advento começa ~4 semanas antes do Natal
    # 4º Domingo antes do Natal
    dia = datetime(ano, 11, 27)
    while dia.weekday() != 6:  # 6 = Domingo
        dia += timedelta(days=1)
    return dia


def obter_tempo_liturgico_hoje():
    """Determina o tempo litúrgico atual."""
    hoje = datetime.now()
    ano = hoje.year

    pascoa = calcular_pascoa(ano)
    cinzas = datas_moveis(ano)["quarta_cinzas"]
    pentecostes = datas_moveis(ano)["pentecostes"]
    advento_inicio = calcular_inicio_advento(ano)

    natal = datetime(ano, 12, 25)
    batismo_senhor = pascoa + timedelta(days=13)  # Aproximado

    # Advento do ano anterior pode estar em vigor no início do ano
    advento_ano_ant = calcular_inicio_advento(ano - 1)
    natal_ano_ant = datetime(ano - 1, 12, 25)

    if advento_ano_ant <= hoje <= natal_ano_ant + timedelta(days=6):
        return {
            "tempo": "Natal",
            "cor": "Branco",
            "descricao": "Tempo do Natal - Celebramos a Encarnação do Senhor",
            "tema_financeiro": "Generosidade e partilha - Reflexão sobre dar com alegria",
        }

    if natal_ano_ant + timedelta(days=7) <= hoje < cinzas:
        return {
            "tempo": "Tempo Comum",
            "cor": "Verde",
            "descricao": "Tempo Comum - Crescimento na fé e na vida cristã",
            "tema_financeiro": "Planejamento e sabedoria - Construindo hábitos financeiros saudáveis",
        }

    if cinzas <= hoje < pascoa:
        if hoje <= datas_moveis(ano)["domingo_ramos"]:
            return {
                "tempo": "Quaresma",
                "cor": "Roxo",
                "descricao": "Quaresma - Tempo de conversão, jejum e esmola",
                "tema_financeiro": "Desapego e caridade - Jejum financeiro e doação aos pobres",
            }
        else:
            return {
                "tempo": "Semana Santa",
                "cor": "Roxo/Vermelho",
                "descricao": "Semana Santa - Paixão e morte do Senhor",
                "tema_financeiro": "Sacrifício e esperança - Superando crises com fé",
            }

    if pascoa <= hoje < pentecostes:
        return {
            "tempo": "Páscoa",
            "cor": "Branco",
            "descricao": "Tempo Pascal - Alegria da Ressurreição",
            "tema_financeiro": "Renovação e providência - Recomeços financeiros com Deus",
        }

    if pentecostes <= hoje < advento_inicio:
        return {
            "tempo": "Tempo Comum",
            "cor": "Verde",
            "descricao": "Tempo Comum após Pentecostes - Crescimento na vida do Espírito",
            "tema_financeiro": "Frutificação e multiplicação - Fazendo render os talentos",
        }

    if advento_inicio <= hoje <= natal + timedelta(days=6):
        if hoje < natal:
            return {
                "tempo": "Advento",
                "cor": "Roxo",
                "descricao": "Advento - Tempo de espera e preparação para o Natal",
                "tema_financeiro": "Esperança e preparação - Planejando o futuro com fé",
            }
        else:
            return {
                "tempo": "Natal",
                "cor": "Branco",
                "descricao": "Tempo do Natal - Celebramos a Encarnação do Senhor",
                "tema_financeiro": "Generosidade e partilha - Dar com alegria",
            }

    # Fallback
    return {
        "tempo": "Tempo Comum",
        "cor": "Verde",
        "descricao": "Tempo Comum",
        "tema_financeiro": "Sabedoria e prudência na administração dos bens",
    }


# ============================================================
# CARREGAR CALENDÁRIO
# ============================================================

def carregar_calendario():
    """Carrega o calendário litúrgico do JSON."""
    if CALENDARIO_FILE.exists():
        with open(CALENDARIO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


# ============================================================
# COMANDOS
# ============================================================

def cmd_hoje():
    """Tema para hoje."""
    hoje = datetime.now()
    tempo = obter_tempo_liturgico_hoje()
    calendario = carregar_calendario()

    print(f"# 📅 Tema Litúrgico de Hoje - {hoje.strftime('%d/%m/%Y')}")
    print()
    print(f"## Tempo Litúrgico: {tempo['tempo']}")
    print(f"**Cor litúrgica:** {tempo['cor']}")
    print(f"**Descrição:** {tempo['descricao']}")
    print()

    # Verificar se há festa/solenidade hoje
    festas = calendario.get("festas_fixas", {})
    mes_dia = hoje.strftime("%m-%d")

    for festa_key, festa_data in festas.items():
        if festa_data.get("data") == mes_dia:
            print(f"## 🎉 Solenidade/Festa: {festa_data['nome']}")
            print(f"**Descrição:** {festa_data.get('descricao', '')}")
            if "tema_financeiro" in festa_data:
                print(f"**Tema financeiro:** {festa_data['tema_financeiro']}")
            print()

    # Verificar santos do dia
    santos = calendario.get("santos", {})
    for santo_key, santo_data in santos.items():
        if santo_data.get("data") == mes_dia:
            print(f"## ⛪ Santo do Dia: {santo_data['nome']}")
            print(f"**Patrono de:** {santo_data.get('patrono', '')}")
            if "tema_financeiro" in santo_data:
                print(f"**Tema financeiro:** {santo_data['tema_financeiro']}")
            print()

    print(f"## 💰 Tema Financeiro Sugerido")
    print(f"{tempo['tema_financeiro']}")
    print()
    print("---")
    print(f"*Gerado pelo Agente Litúrgico - Paz na Conta*")


def cmd_semana():
    """Temas para a semana."""
    hoje = datetime.now()
    calendario = carregar_calendario()

    print(f"# 📅 Temas da Semana - {hoje.strftime('%d/%m/%Y')}")
    print()

    for i in range(7):
        dia = hoje + timedelta(days=i)
        tempo = obter_tempo_liturgico_hoje()
        mes_dia = dia.strftime("%m-%d")

        print(f"## {dia.strftime('%A - %d/%m/%Y')}")
        print(f"**Tempo:** {tempo['tempo']} | **Cor:** {tempo['cor']}")

        # Verificar festas
        festas = calendario.get("festas_fixas", {})
        for festa_key, festa_data in festas.items():
            if festa_data.get("data") == mes_dia:
                print(f"🎉 **{festa_data['nome']}**")

        # Verificar santos
        santos = calendario.get("santos", {})
        for santo_key, santo_data in santos.items():
            if santo_data.get("data") == mes_dia:
                print(f"⛪ **{santo_data['nome']}** - {santo_data.get('patrono', '')}")

        print(f"💰 {tempo['tema_financeiro']}")
        print()


def cmd_mes():
    """Temas para o mês."""
    hoje = datetime.now()
    calendario = carregar_calendario()

    mes_nome = hoje.strftime("%B")
    print(f"# 📅 Temas do Mês - {mes_nome.capitalize()} {hoje.year}")
    print()

    tempo = obter_tempo_liturgico_hoje()
    print(f"## Tempo Litúrgico Predominante: {tempo['tempo']}")
    print(f"**Cor:** {tempo['cor']}")
    print(f"**Tema financeiro:** {tempo['tema_financeiro']}")
    print()

    # Santas e festas do mês
    santos = calendario.get("santos", {})
    festas = calendario.get("festas_fixas", {})

    mes_atual = hoje.strftime("%m")

    print("## 📌 Datas Importantes do Mês")
    print()

    encontrados = False

    for festa_key, festa_data in festas.items():
        if festa_data.get("data", "").startswith(mes_atual):
            print(f"- **{festa_data['data']}** - {festa_data['nome']}")
            encontrados = True

    for santo_key, santo_data in santos.items():
        if santo_data.get("data", "").startswith(mes_atual):
            print(f"- **{santo_data['data']}** - {santo_data['nome']} ({santo_data.get('patrono', '')})")
            encontrados = True

    if not encontrados:
        print("- Nenhuma data especial registrada para este mês.")

    print()
    print("## 💰 Sugestões de Conteúdo para o Mês")
    print(f"1. {tempo['tema_financeiro']}")
    print(f"2. Testemunho de fé e finanças alinhado ao tempo litúrgico")
    print(f"3. Desafio prático semanal para a comunidade")
    print()
    print("---")
    print(f"*Gerado pelo Agente Litúrgico - Paz na Conta*")


def cmd_tempo():
    """Informações do tempo litúrgico atual."""
    hoje = datetime.now()
    ano = hoje.year

    pascoa = calcular_pascoa(ano)
    moveis = datas_moveis(ano)
    tempo = obter_tempo_liturgico_hoje()

    print(f"# ⛪ Tempo Litúrgico Atual")
    print()
    print(f"## Hoje: {hoje.strftime('%d/%m/%Y')} ({hoje.strftime('%A')})")
    print()
    print(f"### {tempo['tempo']}")
    print(f"- **Cor litúrgica:** {tempo['cor']}")
    print(f"- **Descrição:** {tempo['descricao']}")
    print(f"- **Tema financeiro:** {tempo['tema_financeiro']}")
    print()

    print("## 📅 Datas Móveis de {ano}".format(ano=ano))
    print()
    datas_formatadas = {
        "Quarta-feira de Cinzas": moveis["quarta_cinzas"],
        "Domingo de Ramos": moveis["domingo_ramos"],
        "Quinta-feira Santa": moveis["quinta_santa"],
        "Sexta-feira Santa": moveis["sexta_santa"],
        "Sábado de Aleluia": moveis["sabado_aleluia"],
        "Páscoa": moveis["pascoa"],
        "Ascensão do Senhor": moveis["ascensao"],
        "Pentecostes": moveis["pentecostes"],
        "Santíssima Trindade": moveis["santissima_trindade"],
        "Corpus Christi": moveis["corpus_christi"],
    }

    for nome, data in datas_formatadas.items():
        marker = " ← HOJE" if data.date() == hoje.date() else ""
        print(f"- **{nome}:** {data.strftime('%d/%m/%Y')}{marker}")

    advento = calcular_inicio_advento(ano)
    print(f"- **1º Domingo do Advento:** {advento.strftime('%d/%m/%Y')}")

    print()
    print("---")
    print(f"*Gerado pelo Agente Litúrgico - Paz na Conta*")


def cmd_datas():
    """Datas litúrgicas importantes futuras."""
    hoje = datetime.now()
    ano = hoje.year
    calendario = carregar_calendario()
    moveis = datas_moveis(ano)

    print(f"# 📅 Próximas Datas Litúrgicas Importantes")
    print()

    # Datas móveis
    datas_formatadas = {
        "Quarta-feira de Cinzas": moveis["quarta_cinzas"],
        "Domingo de Ramos": moveis["domingo_ramos"],
        "Páscoa": moveis["pascoa"],
        "Ascensão do Senhor": moveis["ascensao"],
        "Pentecostes": moveis["pentecostes"],
        "Corpus Christi": moveis["corpus_christi"],
    }

    print("## 📌 Datas Móveis")
    print()
    for nome, data in datas_formatadas.items():
        if data >= hoje:
            dias = (data - hoje).days
            print(f"- **{nome}:** {data.strftime('%d/%m/%Y')} (em {dias} dias)")

    # Festas fixas futuras
    print()
    print("## 🎉 Próximas Solenidades e Festas")
    print()

    festas = calendario.get("festas_fixas", {})
    for festa_key, festa_data in festas.items():
        data_str = festa_data.get("data", "")
        if data_str:
            partes = data_str.split("-")
            if len(partes) == 2:
                mes, dia = int(partes[0]), int(partes[1])
                data_festa = datetime(ano, mes, dia)
                if data_festa < hoje:
                    data_festa = datetime(ano + 1, mes, dia)
                dias = (data_festa - hoje).days
                if dias <= 90:
                    print(f"- **{festa_data['nome']}:** {data_festa.strftime('%d/%m/%Y')} (em {dias} dias)")

    # Santos relevantes
    print()
    print("## ⛪ Santos Relevantes para Finanças/Trabalho")
    print()

    santos = calendario.get("santos", {})
    for santo_key, santo_data in santos.items():
        if santo_data.get("tema_financeiro"):
            data_str = santo_data.get("data", "")
            if data_str:
                partes = data_str.split("-")
                if len(partes) == 2:
                    mes, dia = int(partes[0]), int(partes[1])
                    data_santo = datetime(ano, mes, dia)
                    if data_santo < hoje:
                        data_santo = datetime(ano + 1, mes, dia)
                    dias = (data_santo - hoje).days
                    if dias <= 90:
                        print(f"- **{santo_data['nome']}:** {data_santo.strftime('%d/%m/%Y')} (em {dias} dias)")
                        print(f"  - Patrono de: {santo_data.get('patrono', '')}")

    print()
    print("---")
    print(f"*Gerado pelo Agente Litúrgico - Paz na Conta*")


def cmd_sugerir(tema=None):
    """Gerar ideias de conteúdo combinando liturgia e finanças."""
    hoje = datetime.now()
    tempo = obter_tempo_liturgico_hoje()
    calendario = carregar_calendario()

    # Banco de temas financeiros católicos
    temas_financeiros = [
        "Dízimo e generosidade cristã",
        "Orçamento familiar à luz do Evangelho",
        "Caridade e justiça social",
        "Desapego material e liberdade financeira",
        "Trabalho como vocação",
        "Investimento ético e responsável",
        "Superando dívidas com fé e disciplina",
        "Poupança com propósito",
        "Doação e solidariedade",
        "Administração dos bens como mordomia",
        "Planejamento financeiro familiar",
        "Consumo consciente e sustentabilidade",
        "Empreendedorismo católico",
        "Educação financeira dos filhos",
        "Aposentadoria com dignidade",
    ]

    if tema:
        print(f"# 💡 Ideias de Conteúdo: \"{tema}\"")
        print()
        print(f"**Tempo litúrgico atual:** {tempo['tempo']}")
        print(f"**Tema do tempo:** {tempo['tema_financeiro']}")
        print()
    else:
        print(f"# 💡 Sugestões de Conteúdo Litúrgico-Financeiro")
        print()
        print(f"**Tempo litúrgico atual:** {tempo['tempo']} ({tempo['cor']})")
        print(f"**Data:** {hoje.strftime('%d/%m/%Y')}")
        print()

    print("## 📝 Ideias Geradas")
    print()

    ideias = []

    for i, tf in enumerate(temas_financeiros[:10], 1):
        ideia = {
            "titulo": f"{tf} no tempo de {tempo['tempo']}",
            "formato": ["Carrossel", "Texto", "Vídeo curto", "Story"][i % 4],
            "publico": ["Iniciantes", "Famílias", "Jovens adultos", "Empreendedores"][i % 4],
            "gancho": _gerar_gancho(tf, tempo["tempo"]),
            "descricao": _gerar_descricao(tf, tempo),
        }
        ideias.append(ideia)

        print(f"### {i}. {ideia['titulo']}")
        print(f"- **Formato:** {ideia['formato']}")
        print(f"- **Público:** {ideia['publico']}")
        print(f"- **Gancho:** {ideia['gancho']}")
        print(f"- **Descrição:** {ideia['descricao']}")
        print()

    # Salvar no acervo
    arquivo_ideias = IDEIAS_DIR / f"ideias_{hoje.strftime('%Y%m%d')}.md"
    with open(arquivo_ideias, "w", encoding="utf-8") as f:
        f.write(f"# Ideias de Conteúdo - {hoje.strftime('%d/%m/%Y')}\n\n")
        f.write(f"Tempo litúrgico: {tempo['tempo']}\n\n")
        for i, ideia in enumerate(ideias, 1):
            f.write(f"## {i}. {ideia['titulo']}\n")
            f.write(f"- Formato: {ideia['formato']}\n")
            f.write(f"- Público: {ideia['publico']}\n")
            f.write(f"- Gancho: {ideia['gancho']}\n")
            f.write(f"- Descrição: {ideia['descricao']}\n\n")

    print(f"✅ Ideias salvas em: `{arquivo_ideias}`")
    print()
    print("---")
    print(f"*Gerado pelo Agente Litúrgico - Paz na Conta*")


def _gerar_gancho(tema, tempo):
    """Gera um gancho de conteúdo."""
    ganchos = {
        "Advento": [
            f"Como se preparar financeiramente para o Natal sem endividamento?",
            f"{tema}: Um guia para o tempo de espera e esperança",
            f"Enquanto o mundo gasta, o cristão se prepara: {tema}",
        ],
        "Natal": [
            f"O verdadeiro presente: {tema} à luz do Natal",
            f"Dar com alegria: {tema} na festa da Encarnação",
            f"Presentes que transformam: {tema}",
        ],
        "Quaresma": [
            f"Jejum financeiro: {tema} como prática quaresmal",
            f"40 dias para transformar suas finanças: {tema}",
            f"Desapego e conversão: {tema} na Quaresma",
        ],
        "Páscoa": [
            f"Ressurreição financeira: {tema} com esperança",
            f"Recomeçar com Cristo: {tema} no tempo pascal",
            f"Alegria da libertação: {tema} após a Páscoa",
        ],
        "Tempo Comum": [
            f"Crescendo na fé e nas finanças: {tema}",
            f"Discipulado financeiro: {tema} no dia a dia",
            f"Vida cristã e dinheiro: {tema}",
        ],
        "Semana Santa": [
            f"Do sacrifício à vitória: {tema}",
            f"Na cruz e na ressurreição: {tema}",
            f"Paixão e esperança: {tema}",
        ],
    }

    opcoes = ganchos.get(tempo, ganchos["Tempo Comum"])
    return opcoes[hash(tema) % len(opcoes)]


def _gerar_descricao(tema, tempo):
    """Gera descrição do conteúdo."""
    return (
        f"Conteúdo sobre '{tema}' alinhado ao tempo de {tempo['tempo']}. "
        f"Cor litúrgica: {tempo['cor']}. "
        f"{tempo['descricao']}. "
        f"Conectar com {tempo['tema_financeiro']}."
    )


def cmd_santo(nome):
    """Conteúdo sobre um santo específico."""
    calendario = carregar_calendario()
    santos = calendario.get("santos", {})

    # Buscar santo por nome
    santo_encontrado = None
    for santo_key, santo_data in santos.items():
        if nome.lower() in santo_data.get("nome", "").lower():
            santo_encontrado = santo_data
            break

    if not santo_encontrado:
        print(f"❌ Santo \"{nome}\" não encontrado no calendário.")
        print()
        print("Santos disponíveis:")
        for santo_key, santo_data in santos.items():
            print(f"  - {santo_data['nome']}")
        return

    print(f"# ⛪ {santo_encontrado['nome']}")
    print()
    print(f"## 📅 Data: {santo_encontrado.get('data', 'N/A')}")
    print(f"## 🏷️ Patrono de: {santo_encontrado.get('patrono', 'N/A')}")
    print()

    if "biografia" in santo_encontrado:
        print(f"## 📖 Biografia")
        print(f"{santo_encontrado['biografia']}")
        print()

    if "tema_financeiro" in santo_encontrado:
        print(f"## 💰 Tema Financeiro")
        print(f"{santo_encontrado['tema_financeiro']}")
        print()

    if "ideias_conteudo" in santo_encontrado:
        print(f"## 💡 Ideias de Conteúdo")
        for i, ideia in enumerate(santo_encontrado["ideias_conteudo"], 1):
            print(f"{i}. {ideia}")
        print()

    # Salvar no acervo
    hoje = datetime.now()
    arquivo = IDEIAS_DIR / f"santo_{nome.lower().replace(' ', '_')}_{hoje.strftime('%Y%m%d')}.md"
    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(f"# {santo_encontrado['nome']}\n\n")
        f.write(f"Data: {santo_encontrado.get('data', 'N/A')}\n\n")
        f.write(f"Patrono de: {santo_encontrado.get('patrono', 'N/A')}\n\n")
        if "biografia" in santo_encontrado:
            f.write(f"## Biografia\n{santo_encontrado['biografia']}\n\n")
        if "tema_financeiro" in santo_encontrado:
            f.write(f"## Tema Financeiro\n{santo_encontrado['tema_financeiro']}\n\n")

    print(f"✅ Conteúdo salvo em: `{arquivo}`")
    print()
    print("---")
    print(f"*Gerado pelo Agente Litúrgico - Paz na Conta*")


def cmd_ollama(prompt=None):
    """Usa Ollama para gerar conteúdo (opcional)."""
    hoje = datetime.now()
    tempo = obter_tempo_liturgico_hoje()

    if not prompt:
        prompt = (
            f"Você é um criador de conteúdo católico para o projeto 'Paz na Conta' "
            f"(mentoria financeira católica). Hoje é {hoje.strftime('%d/%m/%Y')}, "
            f"tempo litúrgico: {tempo['tempo']}. "
            f"Gere 5 ideias de conteúdo para redes sociais que combinem "
            f"a liturgia deste tempo com educação financeira. "
            f"Formato: título, gancho e breve descrição para cada ideia."
        )

    print(f"# 🤖 Gerando conteúdo com Ollama...")
    print()

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2", prompt],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode == 0:
            print(result.stdout)

            # Salvar
            arquivo = IDEIAS_DIR / f"ollama_{hoje.strftime('%Y%m%d_%H%M')}.md"
            with open(arquivo, "w", encoding="utf-8") as f:
                f.write(f"# Conteúdo Ollama - {hoje.strftime('%d/%m/%Y')}\n\n")
                f.write(f"Tempo: {tempo['tempo']}\n\n")
                f.write(result.stdout)

            print(f"\n✅ Conteúdo salvo em: `{arquivo}`")
        else:
            print(f"❌ Erro ao executar Ollama: {result.stderr}")
            print("Dica: Verifique se o Ollama está instalado e rodando.")

    except FileNotFoundError:
        print("❌ Ollama não encontrado. Instale em: https://ollama.com")
        print("Ou use o modo offline sem Ollama.")
    except subprocess.TimeoutExpired:
        print("⏱️ Timeout: Ollama demorou muito para responder.")
    except Exception as e:
        print(f"❌ Erro: {e}")


# ============================================================
# CLI
# ============================================================

def mostrar_ajuda():
    """Mostra ajuda do agente."""
    ajuda = """
# ⛪ Agente Litúrgico - Paz na Conta

## Uso

```bash
python main.py hoje          # Tema litúrgico de hoje
python main.py semana        # Temas para a semana
python main.py mes           # Temas para o mês
python main.py tempo         # Tempo litúrgico atual
python main.py datas         # Próximas datas importantes
python main.py sugerir       # Sugestões de conteúdo
python main.py sugerir "dízimo"  # Sugestões sobre tema específico
python main.py santo "José"  # Conteúdo sobre um santo
python main.py ollama        # Gerar conteúdo com Ollama
python main.py ajuda         # Esta ajuda
```

## Sobre

Agente que combina o calendário litúrgico católico com temas de
finanças pessoais para gerar conteúdo alinhado à fé.

**Projeto:** Paz na Conta - Mentoria Financeira Católica
"""
    print(ajuda)


def main():
    if len(sys.argv) < 2:
        mostrar_ajuda()
        return

    comando = sys.argv[1].lower()

    if comando == "hoje":
        cmd_hoje()
    elif comando == "semana":
        cmd_semana()
    elif comando == "mes":
        cmd_mes()
    elif comando == "tempo":
        cmd_tempo()
    elif comando == "datas":
        cmd_datas()
    elif comando == "sugerir":
        tema = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
        cmd_sugerir(tema)
    elif comando == "santo":
        nome = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not nome:
            print("Uso: python main.py santo \"nome do santo\"")
            return
        cmd_santo(nome)
    elif comando == "ollama":
        prompt = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
        cmd_ollama(prompt)
    elif comando == "ajuda" or comando == "help" or comando == "-h" or comando == "--help":
        mostrar_ajuda()
    else:
        print(f"❌ Comando desconhecido: {comando}")
        print()
        mostrar_ajuda()


if __name__ == "__main__":
    main()
