#!/usr/bin/env python3
"""
OPB Video 10min — Gera roteiro para video semanal de ~10 minutos.
Estrutura: Abertura (1min) + Contexto (2min) + Reflexao (4min) + Aplicacao (2min) + Encerramento (1min)

Uso:
    python main.py "Tema do video"                             — roteiro basico
    python main.py --ideia caminho/para/ideia.md               — a partir de ideia salva
    python main.py "Tema" --exportar                            — salva em arquivo
"""

import argparse
import random
import sys
import re
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR.parent.parent / "acervo" / "video"

SECOES = {
    "abertura": {
        "tempo": "0:00 - 1:00",
        "descricao": "Gancho + versiculo + o que vai aprender",
        "templates": [
            "Voce ja parou pra pensar que {tema}? No video de hoje, vamos refletir sobre isso a luz da Palavra de Deus.",
            "Hoje quero conversar com voce sobre {tema}. Vem comigo que o Senhor tem uma palavra pra nos hoje.",
            "Se tem uma coisa que {tema}, e esta: {versiculo}. Vamos entender o que isso significa na pratica.",
        ],
    },
    "contexto": {
        "tempo": "1:00 - 3:00",
        "descricao": "Contexto do problema, diagnostico, porque isso importa",
        "templates": [
            "No mundo de hoje, {tema} parece algo secundario. Mas, para nos catolicos, isso toca diretamente a nossa fe. A Doutrina Social da Igreja nos ensina que...\n\n{versiculo} nos mostra que Deus se importa com todas as areas da nossa vida, inclusive esta.",
            "Muitos de nos crescemos ouvindo que {tema} e assunto separado da fe. Mas a verdade e que a Igreja tem uma tradicao riquissima sobre isso. Desde os primeiros cristaos em Atos dos Apostolos, vemos que...\n\nO problema e que, sem essa visao, acabamos caindo em dois extremos: ou a busca desenfreada ou a negligencia.",
            "Voce sabia que a Biblia fala mais sobre {tema} do que sobre fe e oracao? Pois e. Deus nao separa o espiritual do material. O que acontece na nossa conta bancaria reflete o que esta no nosso coracao.\n\n{versiculo} nos chama a uma postura diferente.",
        ],
    },
    "reflexao": {
        "tempo": "3:00 - 7:00",
        "descricao": "Aprofundamento teologico, citacao de Padre/Santo, 3 pontos principais",
        "templates": [
            "Vamos nos aprofundar em tres pontos:\n\n1. **{ponto1}** — {versiculo} nos lembra que... (aqui o Padre Furtado diz que 'a confianca e uma homenagem a Divina Providencia'). Isso significa que...\n\n2. **{ponto2}** — Emmir Nogueira nos ensina que 'a Economia do Reino esta baseada na logica do dar-se ao outro.' Quando entendemos isso, percebemos que {tema} nao e sobre acumular, mas sobre administrar com proposito.\n\n3. **{ponto3}** — Carlo Acutis nos mostra que a santidade esta nas coisas simples do dia a dia. E {tema} faz parte disso. Como ele dizia: 'todos nascem como originais, mas muitos morrem como fotocopias.'",
            "Vou te contar uma historia que ilumina isso. Um padre certa vez disse que 'o maior bem do humilde e nao ter bens, e nao se possuir, e esquecer-se inteiramente pelo outro.' Parece contraintuitivo, mas e libertador.\n\n{versiculo} nos convida a olhar para {tema} com os olhos da fe. Nao se trata de...\n\nAqui vale a pena lembrar o que a Doutrina Social da Igreja nos ensina sobre {tema}. O Catecismo diz que...",
            "Vamos refletir sobre {tema} a partir de tres perspectivas:\n\nPrimeiro, a **pessoa consigo mesma** — como eu lido com isso internamente? {versiculo} me confronta com a verdade de que...\n\nSegundo, a **pessoa com o outro** — {tema} nao e uma questao individual. A partilha dos bens e um assunto espiritual, como diz Emmir Nogueira.\n\nTerceiro, a **pessoa com Deus** — no final, {tema} e sobre confianca. O Padre Caussade diz: 'A acao divina inunda o universo, nao temos senao que deixar-nos levar pelas suas ondas.'",
        ],
    },
    "aplicacao": {
        "tempo": "7:00 - 9:00",
        "descricao": "Passos praticos, desafio da semana, o que fazer",
        "templates": [
            "E agora, o que fazer com tudo isso? Aqui vai um desafio pratico para esta semana:\n\n**1. {pratica1}** — Comece hoje mesmo.\n**2. {pratica2}** — Durante a semana, repare como isso muda sua perspectiva.\n**3. {pratica3}** — Compartilhe com alguem e veja o que acontece.\n\nLembre-se: {tema} nao e sobre perfeicao, e sobre direcao. Deus nao espera que voce acerte de primeira, mas que confie Nele e de um passo de cada vez.",
            "Quero deixar tres acoes concretas para voce aplicar esta semana:\n\n📌 **{pratica1}** — Reserve 10 minutos para...\n📌 **{pratica2}** — Durante a semana, tente...\n📌 **{pratica3}** — Ao final da semana, reflita...\n\n{versiculo} nao e um conselho, e uma promessa. Deus esta cuidando de voce.",
            "Nao basta refletir, precisamos agir. Aqui esta seu plano de acao para os proximos 7 dias:\n\n✅ **Dias 1-2**: {pratica1}\n✅ **Dias 3-5**: {pratica2}\n✅ **Dias 6-7**: {pratica3}\n\nCompartilhe nos comentarios como esta sendo essa experiencia. Sua historia pode ajudar outro irmao.",
        ],
    },
    "encerramento": {
        "tempo": "9:00 - 10:00",
        "descricao": "Resumo, chamada para acao, oracao final, like/signo/inscreva-se",
        "templates": [
            "Resumindo o que vimos hoje: {tema} e uma oportunidade de crescer na confianca em Deus. {versiculo} nos lembra que Ele esta no controle.\n\nVamos orar juntos? [ORACAO]\n\nSe este video te ajudou, compartilhe com alguem que precisa ouvir isso. Inscreva-se no canal e ative o sininho para nao perder os proximos videos. Deixe nos comentarios: como voce tem vivido {tema}?\n\nDeus abencoe sua semana! Paz na conta!",
            "Hoje aprendemos que {tema} nao e apenas mais um assunto — e caminho de santidade. {versiculo} e a chave para vivermos isso com liberdade.\n\nQue Sao Mateus e Santa Edwiges intercedam por nos. [ORACAO]\n\nSe voce chegou ate aqui, escreva 'AMEM' nos comentarios. Compartilhe com um amigo catolico e inscreva-se para mais conteudo como este.\n\nFiquem na paz de Cristo!",
            "Para finalizar: {tema} e muito mais simples do que imaginamos. {versiculo} nos mostra o caminho.\n\n[ORACAO FINAL]\n\nGostou? Entao da like, inscreva-se e compartilhe. Me diga nos comentarios: qual versiculo te ajuda quando o assunto e {tema}?\n\nNos vemos no proximo video! Paz na conta!",
        ],
    },
}

PONTOS_REFLEXAO = [
    {"ponto1": "Confianca na providencia", "ponto2": "Administracao como vocacao", "ponto3": "Partilha como caminho de santidade"},
    {"ponto1": "O dinheiro como meio, nao fim", "ponto2": "A liberdade de quem confia em Deus", "ponto3": "O testemunho dos primeiros cristaos"},
    {"ponto1": "A oracao como base das decisoes", "ponto2": "O discernimento financeiro", "ponto3": "A comunidade que sustenta"},
]

PRATICAS = [
    {"pratica1": "faca um orcamento simples das suas entradas e saidas", "pratica2": "separe um valor para o dizimo antes de qualquer gasto", "pratica3": "reescreva sua oracao pedindo a Deus sabedoria financeira"},
    {"pratica1": "anote 3 coisas pelas quais voce e grato financeiramente", "pratica2": "identifique 1 gasto desnecessario e corte esta semana", "pratica3": "ajude alguem com uma necessidade pratica"},
    {"pratica1": "leia Mt 6,25-34 e medite 5 minutos", "pratica2": "converse com sua familia sobre as financas da casa", "pratica3": "fac�a uma doacao, mesmo que pequena, para quem precisa"},
]


def carregar_ideia(caminho_arquivo):
    """Carrega tema e conteudo de um arquivo de ideia markdown."""
    path = Path(caminho_arquivo)
    if not path.exists():
        print(f"Erro: Arquivo nao encontrado: {path}", file=sys.stderr)
        sys.exit(1)

    conteudo = path.read_text(encoding="utf-8")
    linhas = conteudo.split("\n")

    tema = path.stem
    versiculo = ""
    for linha in linhas:
        if linha.startswith("# "):
            tema = linha[2:].strip()
        if "versiculo:" in linha.lower() and ":" in linha:
            partes = linha.split(":", 1)
            if len(partes) > 1:
                versiculo = partes[1].strip().strip('"').strip("'")

    return tema, versiculo, conteudo


def gerar_roteiro(tema, versiculo="", variacao=0, ideia_path=""):
    """Gera roteiro completo de 10 minutos."""
    idx = variacao % len(PONTOS_REFLEXAO)
    pontos = PONTOS_REFLEXAO[idx]
    praticas = PRATICAS[idx]

    if not versiculo:
        versiculos = ["Mt 6, 26.33", "Mt 6, 34", "Rm 8, 28", "At 4, 32-34"]
        versiculo = random.choice(versiculos)

    linhas = []
    linhas.append("---")
    linhas.append("tags: video/roteiro")
    linhas.append("tipo: video")
    linhas.append("tema: \"" + tema + "\"")
    linhas.append("versiculo: \"" + versiculo + "\"")
    if ideia_path:
        source_rel = ideia_path.replace("\\", "/")
        linhas.append("---")
        linhas.append("")
        linhas.append("Fonte: [[" + source_rel + "]]")
        linhas.append("")
    linhas.append("---")
    linhas.append("")
    linhas.append("=" * 60)
    linhas.append(f"ROTEIRO — Video Semanal (~10 min)")
    linhas.append(f"Tema: {tema}")
    linhas.append(f"Versiculo: {versiculo}")
    linhas.append("=" * 60)

    for secao_nome, secao in SECOES.items():
        template = random.choice(secao["templates"])
        texto = template.format(
            tema=tema,
            versiculo=versiculo,
            **pontos,
            **praticas,
        )

        linhas.append(f"\n---")
        linhas.append(f"[{secao_nome.upper()}] ({secao['tempo']})")
        linhas.append(f"--> {secao['descricao']}")
        linhas.append("")
        linhas.append(texto)

    linhas.append(f"\n---")
    linhas.append("=" * 60)
    linhas.append(f"Duracao estimada: ~10 minutos")
    linhas.append(f"Formato: YouTube")
    linhas.append(f"Perfil: Paz na Conta")
    linhas.append(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    linhas.append("=" * 60)

    return "\n".join(linhas)


OUTPUT_DIR2 = SCRIPT_DIR.parent.parent / "_conteudo" / "video"

def salvar_roteiro(conteudo, tema, filename=None):
    """Salva roteiro em arquivo (acervo/video/ + _conteudo/video/)."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR2.mkdir(parents=True, exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tema_clean = re.sub(r'[^a-zA-Z0-9]', '_', tema)[:40]
        filename = f"video_10min_{tema_clean}_{timestamp}.txt"

    output_path = OUTPUT_DIR / filename
    output_path.write_text(conteudo, encoding="utf-8")

    output_path2 = OUTPUT_DIR2 / filename
    output_path2.write_text(conteudo, encoding="utf-8")

    return output_path


def main():
    parser = argparse.ArgumentParser(description="OPB Video 10min — Roteiro semanal")
    parser.add_argument("tema", nargs="?", default="", help="Tema do video")
    parser.add_argument("--ideia", help="Caminho do arquivo de ideia")
    parser.add_argument("--exportar", action="store_true", help="Salvar em arquivo")
    parser.add_argument("--variacao", type=int, default=0, help="Variacao do template (0-2)")

    args = parser.parse_args()

    tema = args.tema
    versiculo = ""
    ideia_path = args.ideia or ""

    if args.ideia:
        tema, versiculo, _ = carregar_ideia(args.ideia)

    if not tema:
        print("Erro: Informe um tema ou use --ideia", file=sys.stderr)
        sys.exit(1)

    roteiro = gerar_roteiro(tema, versiculo, args.variacao, ideia_path)
    print(roteiro)

    if args.exportar:
        path = salvar_roteiro(roteiro, tema)
        print(f"\nSalvo em: {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
