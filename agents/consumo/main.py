#!/usr/bin/env python3
"""
📖 Agente de Consumo de Conteúdo - OPB Sistema
Processa textos, PDFs e URLs, gerando resumos estruturados para o cérebro.
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_PATH = Path(__file__).parent.parent.parent
CONTEXT_PATH = PROJECT_PATH / "context-brain"
ACERVO_PATH = PROJECT_PATH / "acervo" / "conhecimento"

# Adiciona utils ao path
sys.path.append(str(PROJECT_PATH / "utils"))

from context_loader import load_context, get_business_value


def ensure_dirs():
    """Garante que os diretórios de saída existam."""
    CONTEXT_PATH.mkdir(parents=True, exist_ok=True)
    ACERVO_PATH.mkdir(parents=True, exist_ok=True)

    index = ACERVO_PATH / "index.md"
    if not index.exists():
        index.write_text("""# Conhecimento

> Resumos e conceitos extraídos de conteúdo consumido

---

_Last updated: AAAA-MM-DD_
""", encoding='utf-8')


def carregar_contexto():
    """Carrega identidade e regras do cérebro."""
    quem_sou = {}
    path = PROJECT_PATH / "negocio" / "governanca" / "quem-sou.md"
    if path.exists():
        content = path.read_text(encoding='utf-8')
        for line in content.split('\n'):
            if "**Nome**:" in line:
                quem_sou['nome'] = line.split('**Nome**:')[-1].strip()
            if "**Tom de Voz**:" in line:
                quem_sou['tom'] = line.split('**Tom de Voz**:')[-1].strip()
            if "**Cores primárias**:" in line:
                quem_sou['cores'] = line.split('**Cores primárias**:')[-1].strip()
            if "**Missão**:" in line:
                quem_sou['missao'] = line.split('**Missão**:')[-1].strip()
            if "**Público Alvo**:" in line:
                quem_sou['publico'] = line.split('**Público Alvo**:')[-1].strip()
    return quem_sou


def processar_texto_bruto(texto: str) -> str:
    """Limpa e normaliza texto bruto para processamento."""
    # Remove markdown frontmatter
    if texto.startswith('---'):
        parts = texto.split('---', 2)
        if len(parts) >= 3:
            texto = parts[2]

    linhas = texto.split('\n')
    linhas_limpas = [l.strip() for l in linhas if l.strip()]
    return '\n'.join(linhas_limpas)


def eh_resposta_util(texto: str, minimo_palavras: int = 30) -> bool:
    """Verifica se a resposta do LLM é útil ou genérica/descartável."""
    if not texto or len(texto.strip()) < minimo_palavras:
        return False

    # Padrões de respostas genéricas do mock
    genericos = [
        "PERGUNTA PARA VOCÊ",
        "Compartilhe sua experiência",
        "vamos aprender juntos",
        "DICA RÁPIDA",
        "LEMBRE-SE",
        "OFERTA ESPECIAL",
        "#produtividade #empreendedorismo",
        "#comunidade #troca #crescimento",
    ]

    texto_upper = texto.upper()
    for gen in genericos:
        if gen.upper() in texto_upper:
            # Se contém genérico E é curto, descarta
            if len(texto.split()) < 50:
                return False
    return True


def extrair_palavras_chave(texto: str, max_palavras: int = 20) -> list:
    """Extrai palavras-chave relevantes do texto."""
    # Palavras para ignorar (stopwords PT-BR + termos genéricos)
    stopwords = {
        'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'do', 'da', 'dos', 'das',
        'em', 'no', 'na', 'nos', 'nas', 'por', 'para', 'com', 'sem', 'sobre',
        'e', 'ou', 'mas', 'se', 'que', 'como', 'mais', 'menos', 'já', 'não',
        'ser', 'ter', 'estar', 'ir', 'poder', 'fazer', 'dizer', 'haver',
        'isso', 'isto', 'aquilo', 'aquele', 'aquela', 'este', 'esta',
        'pode', 'são', 'foi', 'era', 'será', 'seria', 'foram',
        'então', 'porém', 'porque', 'porquê', 'assim', 'também', 'muito',
        'muita', 'muitos', 'muitas', 'pouco', 'pouca', 'outro', 'outra',
        'mesmo', 'mesma', 'cada', 'entre', 'aqui', 'ali', 'lá', 'cá',
        'onde', 'quando', 'quanto', 'qual', 'quais', 'quem', 'cujo', 'cuja',
        'tudo', 'toda', 'todo', 'todas', 'todos', 'ainda', 'apenas',
        'até', 'coisa', 'coisas', 'contra', 'dar', 'desde', 'diante',
        'disso', 'depois', 'dessa', 'desse', 'desta', 'deste', 'deve',
        'devem', 'devendo', 'devir', 'dizem', 'dizer', 'diz', 'ela',
        'ele', 'elas', 'eles', 'essa', 'esse', 'estou', 'eu',
        'fazendo', 'feita', 'feitas', 'feito', 'feitos', 'grande', 'grandes',
        'ha', 'la', 'lhe', 'lhes', 'lo', 'me', 'minha', 'meu',
        'minhas', 'meus', 'ne', 'nem', 'nessa', 'nessas', 'nesse',
        'nesses', 'nesta', 'nestas', 'neste', 'nestes', 'ninguém',
        'nosso', 'nossos', 'num', 'numa', 'nunca', 'pela', 'pelas',
        'pelo', 'pelos', 'pequena', 'pequenas', 'pequeno', 'pequenos',
        'pois', 'pro', 'quereis', 'queria', 'queriam', 'quero', 'só',
        'sua', 'suas', 'te', 'tem', 'tendendo', 'tendo', 'tenha',
        'tiveram', 'tinham', 'tinha', 'tive', 'tivemos', 'tivéramos',
        'tuas', 'tua', 'vc', 'vem', 'vez', 'vezes', 'você', 'vocês',
        'vos', 'vós', 'zero', 'tipo', 'bem', 'tão', 'tudo',
    }

    # Extrai palavras alfanuméricas
    palavras = re.findall(r'\b[a-záàâãéèêíïóôõöúçñ]+\b', texto.lower())
    palavras = [p for p in palavras if p not in stopwords and len(p) > 3]

    # Conta frequência
    freq = {}
    for p in palavras:
        freq[p] = freq.get(p, 0) + 1

    # Retorna as mais frequentes
    palavras_ordenadas = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [p for p, _ in palavras_ordenadas[:max_palavras]]


def gerar_prompt_resumo(tipo: str, conteudo: str, contexto: dict) -> str:
    """Gera o prompt para o LLM resumir o conteúdo."""
    tom = contexto.get('tom', 'direto e inspirador')
    nome = contexto.get('nome', 'Cleiton')
    missao = contexto.get('missao', 'automação e produtividade')
    publico = contexto.get('publico', 'solopreneurs')

    prompts = {
        "resumo": f"""Resuma o seguinte conteúdo de forma clara e prática.
Tom de voz: {tom}.
Público-alvo: {publico}.
Foque em conceitos acionáveis e insights extraíveis.
Máximo 300 palavras.
Use formatação markdown com tópicos e negritos.

Conteúdo:
{conteudo[:5000]}""",

        "conceitos": f"""Extraia os conceitos-chave, frameworks e padrões do texto abaixo.
Formate como uma lista de conceitos com explicação de uma linha cada.
Tom: {tom}.
Contexto: {nome} é focado em {missao}.

Conteúdo:
{conteudo[:5000]}""",

        "citacoes": f"""Extraia as citações, insights e frases mais impactantes do texto.
Formate cada uma com autor/contexto quando possível.

Conteúdo:
{conteudo[:5000]}""",

        "aplicacao": f"""Com base no conteúdo abaixo, sugira 3-5 formas práticas de aplicar
esses conceitos no negócio de {publico}.
Tom: {tom}.
Foque em ações concretas e imediatas.

Conteúdo:
{conteudo[:5000]}""",

        "tema": f"""Analise o conteúdo abaixo e sugira 3-5 temas de carrossel
que poderiam ser criados a partir dessas informações.
Tom: {tom}.
Para: {publico}.

Formate como uma lista numerada com título e uma breve descrição de cada tema.

Conteúdo:
{conteudo[:3000]}""",
    }

    return prompts.get(tipo, prompts["resumo"])


def gerar_resumo_fallback(conteudo: str) -> str:
    """Gera resumo por extração de frases-chave (sem LLM)."""
    linhas = conteudo.split('\n')
    linhas = [l.strip() for l in linhas if l.strip() and len(l.strip()) > 15]

    if not linhas:
        return "Conteúdo insuficiente para gerar resumo."

    # Seleciona linhas representativas (início, meio, fim)
    total = len(linhas)
    if total <= 5:
        selecionadas = linhas
    else:
        selecionadas = (
            linhas[:2] +
            [linhas[total // 2]] +
            linhas[-2:]
        )

    return "\n\n".join(selecionadas)


def gerar_conceitos_fallback(conteudo: str) -> str:
    """Extrai conceitos por análise de texto (sem LLM)."""
    linhas = conteudo.split('\n')
    # Pega linhas que parecem ser frases completas
    candidatos = []
    for linha in linhas:
        linha = linha.strip()
        if 20 < len(linha) < 150 and not linha.startswith('#') and not linha.startswith('---'):
            candidatos.append(linha)

    if not candidatos:
        palavras = extrair_palavras_chave(conteudo, 10)
        return "\n".join(f"- **{p}** — conceito extraído do conteúdo" for p in palavras)

    return "\n".join(f"- **{i+1}.** {c}" for i, c in enumerate(candidatos[:8]))


def gerar_citacoes_fallback(conteudo: str) -> str:
    """Extrai citações por padrão (sem LLM)."""
    linhas = conteudo.split('\n')
    citacoes = [l.strip() for l in linhas if any(c in l for c in ['"', "“", "”", "''"])]

    if citacoes:
        return "\n".join(f"> {c}" for c in citacoes[:5])

    # Se não achou citações, pega as frases mais longas como insights
    frases = [l.strip() for l in linhas if 30 < len(l.strip()) < 200]
    palavras_chave = extrair_palavras_chave(conteudo, 5)

    if frases:
        return "\n".join(f"> 💡 {f}" for f in frases[:3]) + f"\n\n**Palavras-chave**: {', '.join(palavras_chave)}"

    return f"> **Insight**: {', '.join(palavras_chave)} são os temas centrais deste conteúdo."


def gerar_aplicacao_fallback(conteudo: str) -> str:
    """Gera sugestões de aplicação prática (sem LLM)."""
    palavras = extrair_palavras_chave(conteudo, 8)

    return f"""### 🎯 Aplicação Prática

Com base nos conceitos identificados ({', '.join(palavras[:4])}):

1. **Revisão semanal**: Releia os pontos-chave toda semana para fixar
2. **Lista de ações**: Transforme cada conceito em uma tarefa concreta
3. **Ensine para aprender**: Compartilhe o que aprendeu com alguém
4. **Conecte ideias**: Relacione esses conceitos com outros conteúdos que você já consumiu
5. **Aplique imediatamente**: Escolha 1 conceito e implemente ainda hoje

> Use os conceitos acima como guia para criar conteúdo e carrosséis."""


def gerar_temas_fallback(conteudo: str) -> str:
    """Gera temas de carrossel por análise de texto (sem LLM)."""
    palavras = extrair_palavras_chave(conteudo, 10)
    linhas = conteudo.split('\n')
    titulos = [l.strip().rstrip('.') for l in linhas if l.strip().endswith('.') and 20 < len(l.strip()) < 100]

    temas = []

    # Tema 1: Conceitos principais
    if palavras:
        temas.append(f"**1. {palavras[0].title()} na prática**\n   Como aplicar no dia a dia")

    # Tema 2: Erros comuns
    temas.append("**2. Erros que você pode estar cometendo**\n   Armadilhas comuns nesse assunto")

    # Tema 3: Passo a passo
    temas.append("**3. Passo a passo simplificado**\n   Guia rápido para começar")

    # Tema 4: Mitos vs verdades
    temas.append("**4. Mitos vs. verdades**\n   O que é real e o que é mito")

    # Tema 5: Minha jornada
    temas.append("**5. Minha jornada com {palavra}**\n   Como isso mudou minha forma de pensar")

    return "\n\n".join(temas)


def ler_arquivo_texto(caminho: str) -> str:
    """Lê conteúdo de arquivo de texto."""
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(caminho, 'r', encoding='latin-1') as f:
            return f.read()


def ler_pdf(caminho: str) -> str:
    """Lê conteúdo de PDF."""
    try:
        import fitz
        doc = fitz.open(caminho)
        texto = "\n".join(pagina.get_text() for pagina in doc)
        return texto
    except ImportError:
        try:
            import subprocess
            result = subprocess.run(
                ['pdftotext', caminho, '-'],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return result.stdout
        except Exception:
            pass
        return None


def ler_url(url: str) -> str:
    """Extrai texto de uma URL."""
    try:
        import requests
        from bs4 import BeautifulSoup

        headers = {'User-Agent': 'Mozilla/5.0 (compatible; OPBConsumo/1.0)'}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()

        article = soup.find('article') or soup.find('main') or soup.find('div', class_='post')
        texto = (article or soup).get_text(separator='\n', strip=True)
        return texto[:10000]

    except Exception as e:
        print(f"⚠️ Erro ao ler URL: {e}")
        return None


def processar_com_llm(conteudo: str, tipo_analise: str, contexto: dict) -> tuple:
    """
    Processa o conteúdo usando o LLM.
    Retorna (resultado, foi_util).
    """
    try:
        from llm_provider import generate_text

        prompt = gerar_prompt_resumo(tipo_analise, conteudo, contexto)
        resultado = generate_text(prompt).strip()

        util = eh_resposta_util(resultado)
        if not util:
            print(f"  ⚠️ Resposta do LLM parece genérica, usando fallback...")
            return (None, False)

        return (resultado, True)
    except Exception as e:
        print(f"  ⚠️ Erro no LLM: {e}")
        return (None, False)


ANALISE_FALLBACKS = {
    "resumo": gerar_resumo_fallback,
    "conceitos": gerar_conceitos_fallback,
    "citacoes": gerar_citacoes_fallback,
    "aplicacao": gerar_aplicacao_fallback,
    "tema": gerar_temas_fallback,
}


def analisar_conteudo(conteudo: str, tipo: str = "completo", titulo: str = None,
                      fonte: str = None, tags: list = None, contexto: dict = None,
                      usar_llm: bool = True) -> dict:
    """
    Analisa o conteúdo e gera insights estruturados.
    """
    if contexto is None:
        contexto = carregar_contexto()

    conteudo = processar_texto_bruto(conteudo)

    # Usa frontmatter se disponível
    dados_fm, conteudo_limpo = extrair_dados_frontmatter(conteudo)
    titulo = titulo or dados_fm.get('title', dados_fm.get('titulo', 'Conteúdo sem título'))
    fonte = fonte or dados_fm.get('source', dados_fm.get('fonte', 'Desconhecida'))
    tags = tags or ([dados_fm.get('tags', '').split(',')] if dados_fm.get('tags') else [])

    tipos_analise = ["resumo", "conceitos", "citacoes", "aplicacao", "tema"]
    resultados = {}
    usou_llm = {}

    for t in (tipos_analise if tipo == "completo" else [tipo]):
        print(f"  📊 Gerando análise: {t}...")

        resultado_llm = None
        if usar_llm:
            resultado_llm, foi_util = processar_com_llm(conteudo_limpo, t, contexto)

        if resultado_llm:
            resultados[t] = resultado_llm
            usou_llm[t] = True
        else:
            fallback_fn = ANALISE_FALLBACKS.get(t)
            if fallback_fn:
                print(f"  🔄 Usando fallback para '{t}'")
                resultados[t] = fallback_fn(conteudo_limpo)
                usou_llm[t] = False
            else:
                resultados[t] = "N/A"
                usou_llm[t] = False

    return {
        "titulo": titulo,
        "fonte": fonte,
        "tags": tags,
        "data": datetime.now().strftime("%Y-%m-%d"),
        "conteudo_original_tamanho": len(conteudo),
        "resultados": resultados,
        "usou_llm": usou_llm,
    }


def extrair_dados_frontmatter(texto: str) -> tuple:
    """Extrai metadados do frontmatter YAML se existir."""
    dados = {}
    if texto.startswith('---'):
        partes = texto.split('---', 2)
        if len(partes) >= 3:
            for linha in partes[1].split('\n'):
                if ':' in linha:
                    chave, valor = linha.split(':', 1)
                    dados[chave.strip()] = valor.strip()
            texto = partes[2]
    return dados, texto


def formatar_conhecimento(analise: dict) -> str:
    """Formata a análise como markdown para salvar."""
    tags_str = ", ".join(analise["tags"]) if analise["tags"] else "geral"
    fonte_llm = "LLM" if any(analise.get("usou_llm", {}).values()) else "fallback"

    output = f"""---
name: "{analise['titulo']}"
tipo: conhecimento
fonte: "{analise['fonte']}"
tags: [{tags_str}]
data: {analise['data']}
tamanho_original: {analise['conteudo_original_tamanho']}
gerado_por: {fonte_llm}
---

# 📖 {analise['titulo']}

> Fonte: {analise['fonte']} | Data: {analise['data']}

---

## 📝 Resumo

{analise['resultados'].get('resumo', 'N/A')}

---

## 💡 Conceitos-Chave

{analise['resultados'].get('conceitos', 'N/A')}

---

## 🗣️ Citações e Insights

{analise['resultados'].get('citacoes', 'N/A')}

---

## 🎯 Aplicação Prática

{analise['resultados'].get('aplicacao', 'N/A')}

---

## 🎠 Temas para Carrossel

{analise['resultados'].get('tema', 'N/A')}

---

_Gerado pelo Agente de Consumo de Conteúdo_
"""
    return output


def salvar_conhecimento(analise: dict, titulo_custom: str = None) -> str:
    """Salva a análise como arquivo markdown no acervo."""
    ensure_dirs()

    titulo = analise["titulo"]
    if titulo_custom:
        titulo = titulo_custom

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    titulo_seguro = re.sub(r'[<>:"/\\|?*]', '', titulo.replace(' ', '-').lower())[:40]
    filename = f"{titulo_seguro}_{timestamp}.md"
    filepath = ACERVO_PATH / filename

    output = formatar_conhecimento(analise)
    filepath.write_text(output, encoding='utf-8')

    atualizar_index(titulo, filename)
    salvar_contexto_conhecimento(analise)

    return str(filepath)


def atualizar_index(titulo: str, filename: str):
    """Atualiza o index.md do acervo de conhecimento."""
    index_path = ACERVO_PATH / "index.md"
    if index_path.exists():
        content = index_path.read_text(encoding='utf-8')
        novo_entry = f"- [{titulo}](conhecimento/{filename})\n"
        if "## Índice" not in content:
            content = content.replace(
                "_Last updated:_",
                f"## Índice\n\n{novo_entry}_Last updated:_"
            )
        else:
            content = content.replace(
                "## Índice\n\n",
                f"## Índice\n\n{novo_entry}"
            )
        index_path.write_text(content, encoding='utf-8')


def salvar_contexto_conhecimento(analise: dict):
    """Salva conhecimento extraído no context-brain."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conhecimento_{timestamp}.md"
    filepath = CONTEXT_PATH / filename

    output = f"""# Conhecimento: {analise['titulo']}

> Fonte: {analise['fonte']} | {analise['data']}

## Conceitos Principais

{analise['resultados'].get('conceitos', 'N/A')}

## Citações

{analise['resultados'].get('citacoes', 'N/A')}

## Aplicação

{analise['resultados'].get('aplicacao', 'N/A')}

---

_Last updated: {datetime.now().strftime("%Y-%m-%d")}_
"""
    filepath.write_text(output, encoding='utf-8')


def processar_input(input_path: str, tipo: str = "completo",
                    titulo: str = None, usar_llm: bool = True) -> dict:
    """Processa um input e retorna a análise."""
    conteudo = None
    fonte = input_path

    if input_path.startswith('http://') or input_path.startswith('https://'):
        print(f"🌐 Lendo URL: {input_path}")
        conteudo = ler_url(input_path)
        if not conteudo:
            print(f"❌ Falha ao ler URL: {input_path}")
            return None
        fonte = input_path
    elif Path(input_path).exists():
        print(f"📄 Lendo arquivo: {input_path}")
        ext = Path(input_path).suffix.lower()
        if ext == '.pdf':
            conteudo = ler_pdf(input_path)
        else:
            conteudo = ler_arquivo_texto(input_path)
        fonte = Path(input_path).name
    else:
        print(f"📝 Usando texto direto ({len(input_path)} caracteres)")
        conteudo = input_path
        fonte = "texto direto"

    if not conteudo or len(conteudo.strip()) < 10:
        print("❌ Conteúdo vazio ou muito curto")
        return None

    print(f"✅ Conteúdo carregado ({len(conteudo)} caracteres)")

    contexto = carregar_contexto()
    titulo_final = titulo or Path(fonte).stem if fonte != "texto direto" else "Conteúdo"

    analise = analisar_conteudo(
        conteudo, tipo,
        titulo=titulo_final,
        fonte=fonte,
        contexto=contexto,
        usar_llm=usar_llm
    )

    return analise


def listar_conhecimento():
    """Lista todo o conhecimento salvo."""
    ensure_dirs()
    arquivos = sorted(ACERVO_PATH.glob("*.md"))
    arquivos = [a for a in arquivos if a.name != "index.md"]

    print(f"\n[📖 {len(arquivos)} itens de conhecimento salvos]\n")
    for a in arquivos:
        print(f"  - {a.stem}")

    context_files = sorted(CONTEXT_PATH.glob("conhecimento_*.md"))
    if context_files:
        print(f"\n  [🧠 {len(context_files)} referências no cérebro]")


def stats():
    """Mostra estatísticas do conhecimento."""
    ensure_dirs()
    arquivos = list(ACERVO_PATH.glob("*.md"))
    arquivos = [a for a in arquivos if a.name != "index.md"]

    total = len(arquivos)
    com_llm = 0
    com_fallback = 0

    for a in arquivos:
        content = a.read_text(encoding='utf-8')
        if "gerado_por: LLM" in content:
            com_llm += 1
        elif "gerado_por: fallback" in content:
            com_fallback += 1

    print(f"\n📊 Estatísticas do Conhecimento")
    print(f"   Total: {total} itens")
    print(f"   LLM: {com_llm}")
    print(f"   Fallback: {com_fallback}")
    print(f"   Cérebro: {len(list(CONTEXT_PATH.glob('conhecimento_*.md')))} referências")


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("""
📖 Agente de Consumo de Conteúdo — OPB Sistema

USO:
  python main.py "texto ou conteúdo aqui" [tipo] [título]
  python main.py <arquivo.txt|.pdf> [tipo] [título]
  python main.py <https://url.com> [tipo] [título]
  python main.py --listar
  python main.py --stats
  python main.py --ler "nome"

TIPOS DE ANÁLISE:
  completo      (padrão) - Tudo: resumo + conceitos + citações + aplicação + temas
  resumo        - Apenas resumo
  conceitos     - Apenas conceitos-chave
  citacoes      - Apenas citações e insights
  aplicacao     - Apenas aplicações práticas
  tema          - Apenas temas sugeridos para carrossel

OPÇÕES:
  --no-llm     - Forçar fallback (sem LLM)

EXEMPLOS:
  python main.py "IA vai mudar tudo"
  python main.py artigo.txt completo "Artigo sobre IA"
  python main.py livro.pdf conceitos
  python main.py https://example.com/artigo tema
  python main.py --listar
  python main.py --stats
""")
        return

    arg1 = sys.argv[1]

    if arg1 == "--listar":
        listar_conhecimento()
        return

    if arg1 == "--stats":
        stats()
        return

    if arg1 == "--ler" and len(sys.argv) > 2:
        nome = sys.argv[2]
        arquivos = list(ACERVO_PATH.glob(f"{nome}*.md"))
        if arquivos:
            print(arquivos[0].read_text(encoding='utf-8'))
        else:
            print(f"Conhecimento '{nome}' não encontrado.")
        return

    # Configurar
    input_path = arg1
    tipo = "completo"
    titulo_custom = None
    usar_llm = True

    # Parsear argumentos
    args_restantes = sys.argv[2:]
    for arg in args_restantes:
        if arg in ["completo", "resumo", "conceitos", "citacoes", "aplicacao", "tema"]:
            tipo = arg
        elif arg == "--no-llm":
            usar_llm = False
        else:
            titulo_custom = arg

    # Processar
    print(f"📖 Processando conteúdo...")
    print(f"   Input: {input_path}")
    print(f"   Tipo: {tipo}")
    print(f"   LLM: {'Sim' if usar_llm else 'Não (fallback)'}")
    if titulo_custom:
        print(f"   Título: {titulo_custom}")
    print("-" * 50)

    analise = processar_input(input_path, tipo, titulo_custom, usar_llm)

    if analise is None:
        print("❌ Falha ao processar conteúdo")
        sys.exit(1)

    # Salvar
    arquivo = salvar_conhecimento(analise, titulo_custom)
    print(f"\n✅ Conhecimento salvo em: acervo/conhecimento/{Path(arquivo).name}")

    # Resumo no terminal
    print(f"\n{'='*50}")
    print(f"📖 {analise['titulo']}")
    print(f"   Fonte: {analise['fonte']}")
    print(f"   Tags: {', '.join(analise['tags']) if analise['tags'] else 'geral'}")
    print(f"   Gerado por: {'LLM' if any(analise.get('usou_llm', {}).values()) else 'Fallback'}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()