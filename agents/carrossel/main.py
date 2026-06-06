#!/usr/bin/env python3
"""
🎠 Agente Carrossel — OPB Sistema (v2.0)
Especialista em storytelling para Instagram.

Cada carrossel é uma MINI-NARRATIVA contada em slides, com arco definido
(Jornada do Herói, Antes–Virada–Depois, Conflito–Resolução–Manifesto,
Pergunta–Viagem–Comunidade). O tema/ideia inicial do usuário é a semente
da história — o agente expande em uma jornada coerente, com tom e regras
de quem-sou.md, valores do cérebro, e progressão narrativa (cada slide
avança a história, sem repetir o anterior).

Uso:
    python main.py "ideia inicial" [tipo] [num_slides] [--perfil <id>]
    python main.py "Como sair das dívidas com fé" educational
    python main.py "Nossa história com o dízimo" inspirational
    python main.py "O que é DSI para investidores" educational 6
    python main.py --listar
    python main.py --ler "nome-do-carrossel"

Tipos (arcos narrativos):
    educational    → Jornada do Herói Aplicada (problema → causa → virada → caminho)
    inspirational  → Antes–Virada–Depois (mini-autobiografia com lição)
    promotional    → Conflito–Resolução–Manifesto (dor → solução → nova realidade)
    engagement     → Pergunta–Viagem–Comunidade (provocação → exploração → chamado)
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_PATH = Path(__file__).parent.parent.parent
OUTPUT_PATH = PROJECT_PATH / "acervo" / "carrossel"

sys.path.append(str(PROJECT_PATH / "utils"))

try:
    from context_loader import get_brain_context
    from profile_loader import load_profile
    from llm_provider import generate_text
    HAS_CEREBRO = True
except Exception as _e:
    HAS_CEREBRO = False
    _import_error = _e


# ============================================================
# ARCOS NARRATIVOS
# Cada arco é uma sequência de PAPÉIS (não tipos de slide).
# Cada papel tem: nome curto, função narrativa, prompt para o LLM.
# O número de slides é decidido pelo usuário; o agente escolhe
# quais papéis usar nessa quantidade (com fallback inteligente).
# ============================================================

ARCO_NARRATIVO = {
    "educational": {
        "nome": "Jornada do Herói Aplicada",
        "descricao": "Conduz o leitor do problema até a solução prática, mostrando causa raiz e caminho.",
        "ordem": ["gancho", "dor", "raiz", "perspectiva", "caminho", "passo", "resultado", "chamado"],
        "max_slides": 8,
        "persona_leitor": "Alguém travado no problema, querendo clareza e um próximo passo.",
    },
    "inspirational": {
        "nome": "Antes–Virada–Depois",
        "descricao": "Mini-autobiografia com momento de virada e lição universal.",
        "ordem": ["gancho", "antes", "momento", "virada", "depois", "licao", "chamado"],
        "max_slides": 7,
        "persona_leitor": "Alguém precisando de coragem, querendo ver que mudança é possível.",
    },
    "promotional": {
        "nome": "Conflito–Resolução–Manifesto",
        "descricao": "Nomeia o conflito, apresenta a resolução, declara a nova realidade.",
        "ordem": ["gancho", "conflito", "manifesto", "resolucao", "beneficio", "prova", "chamado"],
        "max_slides": 7,
        "persona_leitor": "Alguém com a dor, considerando uma solução, esperando prova e clareza.",
    },
    "engagement": {
        "nome": "Pergunta–Viagem–Comunidade",
        "descricao": "Provoca com pergunta, leva o leitor numa mini-exploração e abre para o coletivo.",
        "ordem": ["gancho", "pergunta", "contexto", "opiniao", "viagem", "chamado"],
        "max_slides": 6,
        "persona_leitor": "Alguém querendo pensar junto, ser ouvido, pertencer.",
    },
}

PAPEIS_NARRATIVOS = {
    "gancho": {
        "titulo": "O gancho",
        "funcao": "Quebrar a scroll. Criar curiosidade ou identificação imediata. Definir o que está em jogo.",
        "instrucao": "Escreva uma frase de impacto que faça o leitor pausar. Pode ser pergunta, contradição ou afirmação ousada. Máx 60 caracteres na linha principal. Não use 'você sabia que', 'a maioria das pessoas', ou clichê de coach. Termine com tensão que puxa pro próximo slide.",
    },
    "dor": {
        "titulo": "A dor",
        "funcao": "Nomear a ferida do público. Mostrar que o agente entende o que a pessoa sente.",
        "instrucao": "Descreva em 1-2 frases o que o público sente nesse tema. Use a primeira pessoa do plural OU a segunda pessoa. Tom próximo, como conversa de café. Mostre que não é julgamento, é reconhecimento.",
    },
    "raiz": {
        "titulo": "A causa raiz",
        "funcao": "Mostrar a causa oculta, a mentira cultural, ou o erro de mentalidade que mantém a pessoa presa.",
        "instrucao": "Revele em 1-2 frases o que ninguém fala. A causa profunda do problema. Pode citar uma crença errada, um padrão cultural, ou um erro de lógica. Traga uma frase de efeito que pareça 'lâmpada acesa'.",
    },
    "perspectiva": {
        "titulo": "A virada",
        "funcao": "Mudar a lente. Oferecer um novo ângulo que liberta da paralisia.",
        "instrucao": "Apresente a nova perspectiva em 1-2 frases. Conecte com a causa raiz mostrando que a saída é uma mudança de visão, não de esforço. Pode usar analogia simples.",
    },
    "caminho": {
        "titulo": "O caminho",
        "funcao": "Apresentar a solução de forma geral e memorável.",
        "instrucao": "Apresente a direção da solução em 1-2 frases. Não dê os passos ainda, só o 'para onde ir'. Use metáfora ou fórmula curta se possível.",
    },
    "passo": {
        "titulo": "O primeiro passo",
        "funcao": "A primeira ação concreta que o leitor pode dar hoje.",
        "instrucao": "Dê UMA ação específica e executável em 1-2 frases. Use imperativo leve ('comece por', 'tente', 'faça'). Evite listas longas — uma ação > cinco ações.",
    },
    "resultado": {
        "titulo": "A vida transformada",
        "funcao": "Descrever o amanhã. Como fica a vida de quem segue o caminho.",
        "instrucao": "Pinte o cenário de 1-2 frases da vida transformada. Foco no que muda na prática + no sentimento (paz, leveza, liberdade). Não prometa riqueza — prometa paz/propósito se o tom pedir.",
    },
    "chamado": {
        "titulo": "O chamado",
        "funcao": "CTA (call to action) que convida para o próximo passo fora do carrossel.",
        "instrucao": "Convide para uma ação simples: salvar, compartilhar, comentar, seguir, mandar no DM, ler outro post, baixar material. Seja específico. Termine com leveza.",
    },
    "antes": {
        "titulo": "A vida antes",
        "funcao": "Descrever o cenário de estagnação, dor ou incompreensão.",
        "instrucao": "Pinte o cenário de 1-2 frases de como era a vida antes da virada. Detalhe sensorial ou emocional. Use a primeira pessoa do plural se for autobiografia.",
    },
    "momento": {
        "titulo": "O momento decisivo",
        "funcao": "Descrever o ponto de virada — o que aconteceu, o que foi dito, o que ficou claro.",
        "instrucao": "Conte o momento-chave em 1-2 frases. Seja específico (cena, frase, descoberta). Pode ser uma frase de alguém, um evento, uma leitura. Crie tensão antes de revelar.",
    },
    "virada": {
        "titulo": "A virada interior",
        "funcao": "Nomear a mudança interna que ocorreu a partir do momento decisivo.",
        "instrucao": "Explique em 1-2 frases a mudança de mentalidade ou coração que aconteceu. Use 'passei a', 'descobri que', 'comecei a'. Conecte com o que o leitor pode aplicar.",
    },
    "depois": {
        "titulo": "A vida depois",
        "funcao": "Descrever a nova realidade, o que mudou na prática e no sentimento.",
        "instrucao": "Pinte o cenário de 1-2 frases do 'depois'. Detalhe prático + emocional. Mostre que a mudança é possível e replicável.",
    },
    "licao": {
        "titulo": "A lição",
        "funcao": "Extrair o princípio universal que o leitor pode aplicar.",
        "instrucao": "Formule em 1-2 frases a lição que vale pra qualquer pessoa. Tom de conselho sábio, não sermão. Conecte com a história contada.",
    },
    "conflito": {
        "titulo": "O conflito",
        "funcao": "Nomear o problema com força. Mostrar o que está em jogo.",
        "instrucao": "Descreva em 1-2 frases o conflito/dor com força e clareza. Use a tensão pra criar urgência. Mostre que ignorar tem custo.",
    },
    "manifesto": {
        "titulo": "O manifesto",
        "funcao": "Declarar a tese — a posição que o agente assume sobre o tema.",
        "instrucao": "Declare em 1-2 frases a posição firme. Use 'acreditamos que', 'a gente defende que', 'o caminho é'. Tom afirmativo, claro. Pode ser polêmico se o tom permitir.",
    },
    "resolucao": {
        "titulo": "A resolução",
        "funcao": "Apresentar a solução (produto, método, serviço) como caminho natural.",
        "instrucao": "Apresente a solução em 1-2 frases. Mostre o que é, pra quem é, e por que resolve o conflito. Tom direto, sem hype.",
    },
    "beneficio": {
        "titulo": "O benefício",
        "funcao": "Detalhar o que muda na vida de quem adota a solução.",
        "instrucao": "Liste 1-2 benefícios específicos em frases curtas. Use o 'pra quê' — não 'o que é' mas 'o que muda na sua vida'. Conecte com valor humano (paz, tempo, família).",
    },
    "prova": {
        "titulo": "A prova",
        "funcao": "Trazer evidência, depoimento ou dado que sustenta a solução.",
        "instrucao": "Apresente 1 prova em 1-2 frases: pode ser dado, citação de fonte respeitada, depoimento, ou princípio. Tom sóbrio, sem exagero.",
    },
    "pergunta": {
        "titulo": "A pergunta",
        "funcao": "Provocar reflexão com pergunta que não tem resposta óbvia.",
        "instrucao": "Formule uma pergunta provocativa em 1 frase. Tem que ser do tipo que faz a pessoa pensar 'hmm, nunca tinha pensado assim'. Não é sim/não — é aberta.",
    },
    "contexto": {
        "titulo": "O contexto",
        "funcao": "Contextualizar o tema — de onde vem, por que importa agora.",
        "instrucao": "Contextualize em 1-2 frases. Pode ser cenário cultural, dado, citação, ou observação do cotidiano. Faça o leitor sentir que 'faz sentido pensar nisso agora'.",
    },
    "opiniao": {
        "titulo": "A opinião",
        "funcao": "Posicionar-se com clareza. Dizer o que o agente pensa.",
        "instrucao": "Posicione-se em 1-2 frases. Tom claro e afirmativo. Pode ser polêmico se o tom do perfil permitir. Ofereça seu olhar com propriedade.",
    },
    "viagem": {
        "titulo": "A viagem",
        "funcao": "Levar o leitor numa mini-exploração — exemplos, perguntas, ou contrapontos.",
        "instrucao": "Leve o leitor numa exploração de 1-2 frases. Pode ser exemplo concreto, analogia, ou cenário. Ajuda a pessoa a pensar com você, não a receber lição.",
    },
}


# ============================================================
# CONTEXTO E REGRAS
# ============================================================

REGRAS_NARRATIVAS_GLOBAIS = [
    "Cada slide AVANÇA a história — nunca repete a ideia do anterior.",
    "Máx 1 ideia central por slide. Frases curtas e diretas.",
    "Linhas curtas: máx 80 caracteres por linha.",
    "Use o tom do perfil (a gente fala como conversa de café).",
    "Fé/valores aparecem como base, não como pregação.",
    "Termine cada slide (exceto o último) deixando gancho pro próximo.",
    "Não use clichês: 'você sabia que', 'a maioria das pessoas', 'no mundo atual', 'nunca foi tão importante'.",
    "Não prometa riqueza fácil. Prometa paz/propósito se o tom pedir.",
    "Último slide é SEMPRE um chamado (CTA) claro.",
    "Primeiro slide é SEMPRE um gancho que justifica o scroll-stop.",
]


def carregar_contexto(profile_id: Optional[str] = None) -> dict:
    """Carrega contexto completo do cérebro + perfil."""
    if not HAS_CEREBRO:
        return _contexto_minimo()

    try:
        perfil = load_profile(profile_id)
    except Exception:
        perfil = {}

    try:
        brain_text = get_brain_context(profile_id)
    except Exception:
        brain_text = ""

    mv = perfil.get("marca_visual", {}) or {}
    cores_raw = mv.get("cores_primarias") or mv.get("cores_primárias") or "#FF6B6B, #4ECDC4"
    if isinstance(cores_raw, list):
        cores = ", ".join(str(c).strip() for c in cores_raw)
    else:
        cores = str(cores_raw)

    return {
        "nome": perfil.get("nome") or "Paz na Conta",
        "autores": perfil.get("autores") or "Ingrid e Cleiton",
        "descricao": perfil.get("descricao") or "Finanças à luz da fé católica",
        "missao": perfil.get("missao") or "",
        "visao": perfil.get("visao") or "",
        "tom": ", ".join(perfil.get("tom_de_voz") or []) or "leve, direto, próximo",
        "valores": list(perfil.get("valores") or []),
        "regras": list(perfil.get("regras_escrita") or []),
        "publico": perfil.get("publico_alvo") or "católicos que querem organizar as finanças",
        "cores": cores,
        "brain_text": brain_text,
        "profile_id": profile_id,
    }


def _contexto_minimo() -> dict:
    return {
        "nome": "Paz na Conta",
        "autores": "Ingrid e Cleiton",
        "descricao": "Finanças à luz da fé católica",
        "missao": "",
        "visao": "",
        "tom": "leve, direto, próximo",
        "valores": ["fé", "organização", "paz", "serviço", "propósito"],
        "regras": ["Falam a gente", "Frases curtas", "Fé como base não pregação"],
        "publico": "católicos endividados que querem paz nas contas",
        "cores": "#FF6B6B, #4ECDC4",
        "brain_text": "",
        "profile_id": None,
    }


# ============================================================
# SELEÇÃO DE ARCOS
# ============================================================

def selecionar_papeis(arco_key: str, num_slides: int) -> list[str]:
    """Seleciona os papéis narrativos para o número de slides pedido.

    Estratégia: sempre começa com 'gancho' e termina com 'chamado'.
    Os slides do meio são distribuídos na ordem do arco.
    """
    arco = ARCO_NARRATIVO.get(arco_key, ARCO_NARRATIVO["educational"])
    ordem = list(arco["ordem"])
    maximo = arco["max_slides"]

    if num_slides < 3:
        num_slides = 3
    if num_slides > maximo:
        num_slides = maximo

    papeis_fixos = ["gancho", "chamado"]
    papeis_meio = [p for p in ordem if p not in papeis_fixos]

    if num_slides == 2:
        return ["gancho", "chamado"]

    if num_slides == 3:
        return ["gancho", papeis_meio[0] if papeis_meio else "dor", "chamado"]

    meio_count = num_slides - 2
    if meio_count > len(papeis_meio):
        meio_count = len(papeis_meio)

    passo = max(1, len(papeis_meio) // meio_count) if meio_count else 1
    indices = [min(i * passo, len(papeis_meio) - 1) for i in range(meio_count)]
    meio = [papeis_meio[i] for i in indices]

    return ["gancho"] + meio + ["chamado"]


# ============================================================
# GERAÇÃO DE TEXTO (LLM + FALLBACK CONTEXTUAL)
# ============================================================

def construir_prompt_slide(
    tema: str,
    arco_key: str,
    papel: str,
    slide_index: int,
    total_slides: int,
    contexto: dict,
    slides_anteriores: list[dict],
) -> str:
    """Constrói o prompt rico para o LLM gerar o texto de UM slide."""
    papel_info = PAPEIS_NARRATIVOS.get(papel, {})
    arco = ARCO_NARRATIVO.get(arco_key, ARCO_NARRATIVO["educational"])

    regras_texto = "\n".join(f"  - {r}" for r in contexto.get("regras", [])[:6])
    valores_texto = ", ".join(contexto.get("valores", [])[:5])

    anteriores = ""
    if slides_anteriores:
        anteriores = "\n".join(
            f"  Slide {i+1} ({s['papel']}): {s.get('titulo', '')} — {s.get('texto', '')[:140]}"
            for i, s in enumerate(slides_anteriores)
        )

    regras_globais = "\n".join(f"  - {r}" for r in REGRAS_NARRATIVAS_GLOBAIS)

    prompt = f"""Você é um especialista em storytelling para Instagram. Está criando o slide {slide_index + 1} de {total_slides} de um carrossel.

CONTEXTO DO AUTOR:
- Negócio: {contexto.get("nome")}
- Autores: {contexto.get("autores")}
- Descrição: {contexto.get("descricao")}
- Público: {contexto.get("publico")}
- Tom de voz: {contexto.get("tom")}
- Valores a incorporar: {valores_texto}
- Regras de escrita:
{regras_texto or "  - (sem regras específicas)"}

HISTÓRIA DO CARROSSEL:
- Tema/ideia inicial: "{tema}"
- Arco narrativo: {arco["nome"]} — {arco["descricao"]}
- Persona do leitor: {arco["persona_leitor"]}

PAPEL DESTE SLIDE ({slide_index + 1}/{total_slides}):
- Papel narrativo: {papel} — {papel_info.get("titulo", papel)}
- Função na história: {papel_info.get("funcao", "")}
- Instrução: {papel_info.get("instrucao", "")}

SLIDES ANTERIORES (para não repetir e dar continuidade):
{anteriores if anteriores else "  (este é o primeiro slide — o gancho)"}

REGRAS GLOBAIS DE STORYTELLING:
{regras_globais}

FORMATO DE SAÍDA:
- Texto pronto pra colar no Instagram.
- Use 1 emoji temático na primeira linha (não mais que 1).
- Linha principal: máx 60 caracteres.
- Linhas seguintes: máx 80 caracteres.
- Use quebras de linha para legibilidade.
- Não numere o slide.
- Retorne APENAS o texto do slide, sem comentários.

Texto do slide:"""
    return prompt


def gerar_texto_slide(
    tema: str,
    arco_key: str,
    papel: str,
    slide_index: int,
    total_slides: int,
    contexto: dict,
    slides_anteriores: list[dict],
    use_llm: bool = True,
) -> str:
    """Gera o texto de um slide via LLM (Ollama) com fallback contextual."""
    if use_llm and HAS_CEREBRO:
        prompt = construir_prompt_slide(
            tema=tema,
            arco_key=arco_key,
            papel=papel,
            slide_index=slide_index,
            total_slides=total_slides,
            contexto=contexto,
            slides_anteriores=slides_anteriores,
        )
        try:
            texto = generate_text(prompt)
            texto = (texto or "").strip()
            if texto and len(texto) > 10 and not texto.lower().startswith("[erro"):
                return _limpar_texto(texto)
        except Exception as e:
            print(f"   ⚠ LLM falhou no slide {slide_index + 1}: {e}", file=sys.stderr)

    return _fallback_texto(tema, papel, contexto, slide_index, total_slides)


def _limpar_texto(texto: str) -> str:
    """Remove prefixos de LLM (aspas, 'Texto:', 'Slide 1:') que tinyllama às vezes adiciona."""
    texto = texto.strip()
    texto = re.sub(r'^["\'\s]*', '', texto)
    texto = re.sub(r'^(slide\s*\d+\s*[:\-—]?\s*)', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'^(texto\s*[:\-—]?\s*)', '', texto, flags=re.IGNORECASE)
    if texto.startswith('"') and texto.endswith('"'):
        texto = texto[1:-1]
    return texto.strip()


def _fallback_texto(
    tema: str,
    papel: str,
    contexto: dict,
    slide_index: int,
    total_slides: int,
) -> str:
    """Fallback contextual sem LLM: usa o tema uma única vez (no gancho)
    e mantém o restante da narrativa em abstrato, ancorado em tom/valores
    do perfil. Não repete o tema literal entre slides.

    Estratégia de variação: cada papel tem 2-3 templates alternativos
    selecionados por `slide_index % len(opcoes)`, evitando repetição
    quando o mesmo papel aparece em múltiplos slides.
    """
    tom = contexto.get("tom", "leve e direto")
    publico = contexto.get("publico", "o público")
    valores = contexto.get("valores") or []
    missao = contexto.get("missao") or ""
    primeiro_valor = valores[0] if valores else "propósito"
    segundo_valor = valores[1] if len(valores) > 1 else "serviço"

    EMOJIS = {
        "gancho": "🎯", "dor": "💔", "raiz": "🔍", "perspectiva": "💡",
        "caminho": "🛤️", "passo": "👉", "resultado": "✨", "chamado": "💬",
        "antes": "🌧️", "momento": "⚡", "virada": "🌅", "depois": "🌤️",
        "licao": "📝", "conflito": "⚠️", "manifesto": "📢", "resolucao": "✅",
        "beneficio": "🌱", "prova": "🏛️", "pergunta": "❓", "contexto": "📋",
        "opiniao": "🔥", "viagem": "🧭",
    }
    emoji = EMOJIS.get(papel, "📌")
    tema_curto = tema if len(tema) <= 28 else tema[:25] + "..."
    tema_lower = tema.lower()

    # ---- GANCHO: 1ª menção do tema (a única explícita da narrativa) ----
    ganchos = [
        f"{emoji} {tema.upper()}\n\nE se essa fosse a peça que faltava pra você destravar isso de uma vez?",
        f"{emoji} {tema.upper()}\n\nPode parecer simples. Mas quase ninguém aplica direito.",
        f"{emoji} {tema.upper()}\n\nPresta atenção nesse post — ele muda como você vê o próximo passo.",
    ]
    gancho = ganchos[slide_index % len(ganchos)]

    # ---- DOR: em abstrato, sem citar o tema literal ----
    dores = [
        f"{emoji} A gente entende.\n\nVocê olha pra esse assunto e trava. Tem sensação de que todo mundo já resolveu menos você. Mas não é assim — é só que ninguém te ensinou pelo ângulo certo.",
        f"{emoji} A verdade nua.\n\nPor dentro, é um misto de cansaço e vergonha. Você tenta, não sai do lugar, e se convence de que talvez não seja pra você.",
        f"{emoji} Sabe o que dói?\n\nNão é o problema em si. É acreditar que você é o único que não consegue resolver.",
    ]
    dor = dores[slide_index % len(dores)]

    # ---- RAIZ: causa comum (sem citar o tema) ----
    raizes = [
        f"{emoji} A causa que ninguém fala.\n\nTem uma crença antiga sustentando isso. Algo que você absorveu sem questionar. E é ela — não a sua capacidade — que trava o jogo.",
        f"{emoji} Onde tudo começa.\n\nO erro não está em você. Está num modelo mental que te ensinaram como se fosse verdade universal. Mas é só um modelo.",
        f"{emoji} O ponto-cego.\n\nExiste um passo anterior que ninguém cita. Sem ele, qualquer tentativa vira empurrar pedra morro acima.",
    ]
    raiz = raizes[slide_index % len(raizes)]

    # ---- PERSPECTIVA: virada, novo ângulo ----
    perspectivas = [
        f"{emoji} E se a lente mudar?\n\nO problema continua o mesmo. Mas a forma de olhar muda tudo. Quando você vê por outro ângulo, o caminho aparece onde antes só tinha parede.",
        f"{emoji} A virada começa aqui.\n\nNão é fazer mais. É pensar diferente. Uma pergunta nova que desarruma o que parecia certo.",
        f"{emoji} O outro lado.\n\nExiste uma forma de olhar isso que simplifica. Não é mágica — é clareza. E clareza aparece quando alguém te mostra o que você não tava vendo.",
    ]
    perspectiva = perspectivas[slide_index % len(perspectivas)]

    # ---- CAMINHO: direção, sem citar o tema ----
    caminhos = [
        f"{emoji} O caminho existe.\n\nNão é milagre nem fórmula de coach. É processo — simples, real, testável. Funciona pra gente comum com vida corrida.",
        f"{emoji} A direção.\n\nTem um caminho que cabe na sua rotina. Curto, repetível, e baseado em princípios que você consegue explicar pra alguém num café.",
        f"{emoji} A rota.\n\nEla começa pequena. Mas é segura. E leva a um lugar que vale a pena.",
    ]
    caminho = caminhos[slide_index % len(caminhos)]

    # ---- PASSO: ação concreta (sem citar o tema) ----
    passos = [
        f"{emoji} Comece HOJE.\n\nEscolha UM papel. Anote UMA coisa. Só isso. Amanhã você continua — mas o motor já ligou.",
        f"{emoji} O primeiro passo.\n\nNão é planejar tudo. É decidir a primeira ação. Pequena, concreta, que você consegue fazer antes de dormir.",
        f"{emoji} Ação de 15 minutos.\n\nDefine um timer. Faz a coisa mais simples que avança o assunto. Quando apitar, você para. Amanhã repete.",
    ]
    passo = passos[slide_index % len(passos)]

    # ---- RESULTADO: a vida depois (em abstrato) ----
    resultados = [
        f"{emoji} A vida do outro lado.\n\nNão é sobre perfeição. É sobre paz. Sobre olhar pro tema e sentir que dá conta — com {primeiro_valor} e {segundo_valor} como guia.",
        f"{emoji} O amanhã.\n\nMais leveza. Mais clareza. Decisões que conversam com o que você acredita. É isso que está do outro lado.",
        f"{emoji} O que muda.\n\nVocê continua com a mesma rotina, as mesmas contas, o mesmo tempo. Mas a postura muda — e a postura muda o resultado.",
    ]
    resultado = resultados[slide_index % len(resultados)]

    # ---- CHAMADO: CTA, sem repetir o tema, foco na ação externa ----
    chamados = [
        f"{emoji} E agora?\n\nSalva esse post. Manda pra alguém que precisa ouvir isso. E me conta nos comentários: o que mais te trava quando o assunto é esse?",
        f"{emoji} Próximo passo.\n\nComenta 'eu quero' aqui embaixo. Quem comenta volta. E a próxima ideia vem na sequência.",
        f"{emoji} Bora?\n\nSegue pra não perder o próximo. Compartilha com alguém que tá travado nesse mesmo ponto. Às vezes uma frase muda a semana de alguém.",
    ]
    chamado = chamados[slide_index % len(chamados)]

    # ---- INSPIRATIONAL ----
    antes_text = (
        f"{emoji} Antes\n\nA gente vivia apagando incêndio. "
        f"Tudo era no susto. Toda decisão pesava. E a sensação era de correr sem sair do lugar."
    )
    momento = (
        f"{emoji} O dia que mudou tudo\n\n"
        f"Alguém disse uma frase simples. Ou um livro caiu na mão certa. "
        f"Não foi um evento grandioso — foi uma frase que destravou o automático."
    )
    virada = (
        f"{emoji} A virada\n\nNão foi força de vontade. Foi uma nova lente. "
        f"A gente parou de remar contra a maré e começou a escolher a direção antes de gastar energia."
    )
    depois_text = (
        f"{emoji} Depois\n\nA vida não virou filme. Ficou possível. "
        f"Possível muda tudo — porque possível é repetível, e repetível vira estilo de vida."
    )
    licao = (
        f"{emoji} O que a gente aprendeu\n\nNão é talento nem sorte. "
        f"É escolher uma vez e ajustar mil vezes — com constância e sem drama."
    )

    # ---- PROMOTIONAL ----
    conflito = (
        f"{emoji} O conflito é real\n\nQuando você ignora, o problema não some — cresce. "
        f"E cobra juros. Literalmente ou emocionalmente."
    )
    manifesto = (
        f"{emoji} A gente acredita\n\nQue isso aqui não precisa ser privilégio de quem já sabe. "
        f"Deve ser caminho aberto pra quem quer viver com mais paz e {primeiro_valor}."
    )
    resolucao = (
        f"{emoji} A solução\n\nNão é produto da moda nem promessa de coach. "
        f"É método simples, testado por gente real, com tom {tom}."
    )
    beneficio = (
        f"{emoji} O que muda pra você\n\nMais clareza. Menos ansiedade. "
        f"Decisões que conversam com seus valores. O peso vira ferramenta."
    )
    prova = (
        f"{emoji} Não é achismo\n\nTem base, tem princípio, tem gente que viveu. "
        f"A mudança começa simples — uma decisão por vez."
    )

    # ---- ENGAGEMENT ----
    pergunta_text = (
        f"{emoji} Pergunta séria\n\nE se tudo que te ensinaram sobre esse assunto "
        f"tivesse um ângulo cego? O que mudaria se você conhecesse esse ângulo?"
    )
    contexto_text = (
        f"{emoji} O cenário\n\nHoje se fala muito sobre, mas pouco com profundidade. "
        f"É hora de ir além do senso comum e do barulho das redes."
    )
    opiniao = (
        f"{emoji} Nossa posição\n\nA gente defende que isso se resolve com verdade, "
        f"não com atalho. Quem vende solução rápida tá te vendendo ilusão."
    )
    viagem = (
        f"{emoji} Vem comigo\n\nImagina a cena: você aplicando isso daqui a 30 dias. "
        f"O que seria diferente? O que sumiria da sua cabeça à noite?"
    )

    templates = {
        "gancho": gancho,
        "dor": dor,
        "raiz": raiz,
        "perspectiva": perspectiva,
        "caminho": caminho,
        "passo": passo,
        "resultado": resultado,
        "chamado": chamado,
        "antes": antes_text,
        "momento": momento,
        "virada": virada,
        "depois": depois_text,
        "licao": licao,
        "conflito": conflito,
        "manifesto": manifesto,
        "resolucao": resolucao,
        "beneficio": beneficio,
        "prova": prova,
        "pergunta": pergunta_text,
        "contexto": contexto_text,
        "opiniao": opiniao,
        "viagem": viagem,
    }
    return templates.get(papel, f"{emoji} {tema_curto} — slide {slide_index + 1} de {total_slides}.")


# ============================================================
# SUGESTÃO VISUAL
# ============================================================

def gerar_sugestao_visual(papel: str, tema: str, contexto: dict) -> str:
    """Sugere elementos visuais coerentes com o papel narrativo."""
    cores = contexto.get("cores", "#FF6B6B, #4ECDC4")
    cor_principal = cores.split(",")[0].strip()

    visuais = {
        "gancho": f"Tipografia grande e bold. Fundo {cor_principal} ou preto de contraste. Título com peso visual — primeira coisa que o olho lê.",
        "dor": f"Iconografia emocional sutil (linha contínua, mão no rosto, sombra). Fundo claro, paleta dessaturada. Texto próximo, sem dramatizar.",
        "raiz": f"Diagrama de causa-efeito ou setas. Visual informativo, mas limpo. Use ícone de lâmpada apagada/acesa pra reforçar a 'causa'.",
        "perspectiva": f"Divisão antes/depois ou duas colunas. Cor de contraste (verde/cyan) pra simbolizar a virada.",
        "caminho": f"Trilha, seta ou mapa minimalista. Visual de direção. Use {cor_principal} como guia.",
        "passo": f"Caixa única destacada, número '1' em destaque, fundo {cor_principal}. Visual de checklist executável.",
        "resultado": f"Imagem luminosa, paisagem aberta ou sol nascendo. Sensação de espaço e paz. Pouco texto.",
        "chamado": f"Botão estilizado com seta. Fundo {cor_principal}. CTA visível e simples — salve, compartilhe, comente.",
        "antes": f"Paleta fria, tons fechados, composição apertada. Sensação de peso.",
        "momento": f"Linha do tempo ou ponto de exclamação visual. Contraste forte — esse é o clique da história.",
        "virada": f"Transição de paleta (fechado → aberto). Sol/luz entrando no quadro. Tom de amanhecer.",
        "depois": f"Paleta quente, composição aberta, elementos leves. Sensação de respirar.",
        "licao": f"Iconografia de livro aberto ou citação entre aspas. Fundo clean, destaque no texto.",
        "conflito": f"Visual de alerta, mas sem ser apelativo. X sutil ou risco diagonal. Cor quente ({cor_principal}).",
        "manifesto": f"Tipografia manifesto — bold, espaçada, caixa alta. Fundo sólido. Tom de declaração.",
        "resolucao": f"Mockup do produto/serviço, ou símbolo de ferramenta. Visual limpo e profissional.",
        "beneficio": f"Icones de check, estrela ou semente. Use metáfora visual (planta crescendo, luz acesa).",
        "prova": f"Citação em destaque, ou badge/selo de fonte respeitada. Visual sóbrio, sem hype.",
        "pergunta": f"Fundo limpo, pergunta centralizada em tipografia grande. Sensação de pausa e reflexão.",
        "contexto": f"Mapas, dados, ou citação de fonte. Visual informativo e respeitoso.",
        "opiniao": f"Tipografia forte e direta. Cor de afirmação. Visual que impõe.",
        "viagem": f"Elementos visuais que 'andam' — setas, ícones de movimento, jornada. Convite visual.",
    }
    return visuais.get(papel, f"Visual coerente com o papel '{papel}' e a paleta {cor_principal}.")


# ============================================================
# GERAÇÃO DO CARROSSEL COMPLETO
# ============================================================

def gerar_carrossel(
    tema: str,
    arco_key: str = "educational",
    num_slides: int = None,
    profile_id: Optional[str] = None,
    use_llm: bool = True,
) -> list[dict]:
    """Gera a estrutura completa do carrossel como narrativa.

    Args:
        tema: ideia/semente inicial da história.
        arco_key: educational, inspirational, promotional, engagement.
        num_slides: quantidade desejada (3-8 conforme o arco).
        profile_id: id do perfil (para multi-perfil).
        use_llm: tentar usar Ollama (cai no fallback se falhar).

    Returns:
        Lista de slides com papel, titulo, texto, sugestao_visual.
    """
    contexto = carregar_contexto(profile_id)
    arco = ARCO_NARRATIVO.get(arco_key, ARCO_NARRATIVO["educational"])
    papeis = selecionar_papeis(arco_key, num_slides or arco["max_slides"])

    slides = []
    for i, papel in enumerate(papeis):
        texto = gerar_texto_slide(
            tema=tema,
            arco_key=arco_key,
            papel=papel,
            slide_index=i,
            total_slides=len(papeis),
            contexto=contexto,
            slides_anteriores=slides,
            use_llm=use_llm,
        )
        papel_info = PAPEIS_NARRATIVOS.get(papel, {})
        slide = {
            "papel": papel,
            "papel_titulo": papel_info.get("titulo", papel),
            "funcao": papel_info.get("funcao", ""),
            "titulo": _titulo_curto(tema, papel, i + 1, len(papeis)),
            "texto": texto,
            "sugestao_visual": gerar_sugestao_visual(papel, tema, contexto),
        }
        slides.append(slide)

    return slides


def _titulo_curto(tema: str, papel: str, slide_num: int, total: int) -> str:
    """Gera um título curto e visual pra cada slide (pra UI/plataforma)."""
    papel_info = PAPEIS_NARRATIVOS.get(papel, {})
    titulo_base = papel_info.get("titulo", papel.capitalize())
    if papel == "gancho":
        return f"Slide 1 — {tema[:30]}"
    if papel == "chamado":
        return f"Slide {slide_num} — {titulo_base}"
    return f"Slide {slide_num} — {titulo_base}"


# ============================================================
# FORMATAÇÃO E SALVAMENTO
# ============================================================

def formatar_carrossel(slides: list, tema: str, arco_key: str) -> str:
    """Formata o carrossel como markdown pronto pra copiar/revisar."""
    contexto = carregar_contexto()
    arco = ARCO_NARRATIVO.get(arco_key, ARCO_NARRATIVO["educational"])

    output = f"""---
name: "Carrossel: {tema}"
tipo: carrossel
tema: {tema}
arco: {arco["nome"]}
slides: {len(slides)}
data: {datetime.now().strftime("%Y-%m-%d")}
autor: {contexto.get("nome")}
---

# 🎠 {tema}

> **Arco narrativo:** {arco["nome"]}
> {arco["descricao"]}
> Tom: {contexto.get("tom")} | Público: {contexto.get("publico")}

---

## 📖 A História (resumo)

{_resumo_historia(slides)}

---

## 🖼️ Slides (prontos pra Instagram)

"""
    for i, slide in enumerate(slides, 1):
        output += f"""### Slide {i}/{len(slides)} — {slide['papel_titulo']}

**Papel na história:** {slide['funcao']}

**📝 Texto (copie e cole):**
```
{slide['texto']}
```

**🎨 Sugestão visual:** {slide['sugestao_visual']}

---

"""

    output += f"""## 💡 Dicas de montagem (Canva/Figma)

- Cores: {contexto.get("cores")}
- Fontes: Montserrat Bold (título) + Open Sans (corpo)
- Regra: 1 slide = 1 ideia. Não encha.
- Primeiro e último slide merecem mais atenção (são os que vendem o carrossel).
- Salve o PNG/JPG na ordem — a leitura tem que fluir como história.

---

_Gerado pelo Agente Carrossel v2.0 — especialista em storytelling_
"""
    return output


def _resumo_historia(slides: list) -> str:
    """Cria um parágrafo-síntese da narrativa do carrossel."""
    arco_papeis = " → ".join(s["papel_titulo"] for s in slides)
    return (
        f"O carrossel percorre {len(slides)} capítulos: **{arco_papeis}**. "
        f"Cada slide avança a história — do gancho inicial até o chamado final. "
        f"Não pule slides: a força está na progressão."
    )


def ensure_output():
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    index = OUTPUT_PATH / "index.md"
    if not index.exists():
        index.write_text(
            """# 🎠 Carrosséis — Storytelling

> Cada carrossel é uma mini-narrativa com arco definido.
> Gerados pelo Agente Carrossel v2.0 (storytelling).

---

## Índice

_Last updated: AAAA-MM-DD_
""",
            encoding='utf-8',
        )


def salvar_carrossel(tema: str, slides: list, arco_key: str) -> str:
    """Salva o carrossel em arquivo markdown e atualiza índice."""
    ensure_output()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tema_seguro = re.sub(r'[^\w\s-]', '', tema).strip().replace(' ', '-').lower()[:30]
    if not tema_seguro:
        tema_seguro = "carrossel"
    filename = f"{tema_seguro}_{timestamp}.md"

    conteudo = formatar_carrossel(slides, tema, arco_key)

    try:
        filepath = OUTPUT_PATH / filename
        filepath.write_text(conteudo, encoding='utf-8')
    except PermissionError:
        fallback_dir = Path.home() / ".opb" / "acervo" / "carrossel"
        fallback_dir.mkdir(parents=True, exist_ok=True)
        filepath = fallback_dir / filename
        filepath.write_text(conteudo, encoding='utf-8')
        print(f"   ⚠ PermissionError — salvou em {filepath}", file=sys.stderr)

    try:
        index_path = filepath.parent / "index.md"
        existing = index_path.read_text(encoding='utf-8')
        novo_entry = f"- [{tema}]({filename})\n"
        if "## Índice" not in existing:
            existing = existing.replace(
                "_Last updated:_",
                f"## Índice\n\n{novo_entry}\n_Last updated:_",
            )
        else:
            existing = existing.replace(
                "## Índice\n\n",
                f"## Índice\n\n{novo_entry}",
            )
        index_path.write_text(existing, encoding='utf-8')
    except (PermissionError, FileNotFoundError):
        pass

    return filename


# ============================================================
# CLI
# ============================================================

def listar_carrossel():
    ensure_output()
    files = sorted(OUTPUT_PATH.glob("*.md"), reverse=True)
    files = [f for f in files if f.name != "index.md"]
    print(f"\n[🎠 {len(files)} carrosséis salvos]\n")
    for f in files:
        print(f"  - {f.stem}")


def ler_carrossel(nome: str):
    caminho = OUTPUT_PATH / f"{nome}.md"
    if caminho.exists():
        print(caminho.read_text(encoding='utf-8'))
    else:
        print(f"Carrossel '{nome}' não encontrado.")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if "--listar" in sys.argv:
        listar_carrossel()
        return
    if "--ler" in sys.argv and len(args) > 0:
        ler_carrossel(args[0])
        return

    if not args:
        print(__doc__)
        return

    tema = args[0]
    arco_key = args[1] if len(args) > 1 else "educational"
    num_slides = int(args[2]) if len(args) > 2 and args[2].isdigit() else None
    profile_id = None
    if "--perfil" in sys.argv:
        idx = sys.argv.index("--perfil")
        if idx + 1 < len(sys.argv):
            profile_id = sys.argv[idx + 1]

    use_llm = "--no-llm" not in sys.argv

    print(f"🎠 Gerando carrossel narrativo...")
    print(f"   Tema/ideia:  {tema}")
    print(f"   Arco:        {arco_key} — {ARCO_NARRATIVO.get(arco_key, {}).get('nome', '?')}")
    if num_slides:
        print(f"   Slides:      {num_slides}")
    if profile_id:
        print(f"   Perfil:      {profile_id}")
    print(f"   LLM:         {'ativado' if use_llm and HAS_CEREBRO else 'fallback contextual'}")
    print("-" * 60)

    slides = gerar_carrossel(
        tema=tema,
        arco_key=arco_key,
        num_slides=num_slides,
        profile_id=profile_id,
        use_llm=use_llm,
    )

    print(f"\n[🎠 {len(slides)} slides gerados — narrativa completa]\n")
    for i, slide in enumerate(slides, 1):
        print(f"── Slide {i}/{len(slides)} [{slide['papel_titulo'].upper()}] ──")
        print(f"   {slide['texto'][:200]}{'...' if len(slide['texto']) > 200 else ''}")
        print()

    arquivo = salvar_carrossel(tema, slides, arco_key)
    print(f"📁 Salvo em: acervo/carrossel/{arquivo}")


if __name__ == "__main__":
    main()
