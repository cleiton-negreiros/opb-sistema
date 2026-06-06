"""
templates.py — Templates paste-ready para o Agente Carrossel (v3.0).

Estrutura por (perfil, tipo, formato):
    TEMPLATES[perfil_id][tipo][formato] = {
        "titulo_visual": str,
        "slides": [
            {
                "slot": str,         # gancho, dor, fe, conselho, passo, cta, ...
                "titulo": str,       # cabeçalho do slide
                "template": str,     # texto com placeholders
                "placeholder_principal": str,  # o que o LLM (ou user) precisa preencher
            },
            ...
        ],
    }

Perfis suportados: paz-na-conta, toque-de-paz, caminho-vida.
Fallback: 'generico' (qualquer perfil não mapeado usa isso).

Tipos (arcos):
    educacional   — Dica prática (Jornada do Herói simplificada)
    inspiracional — Mini-história Antes/Virada/Depois
    contraste     — O que o mundo fala vs o que a Bíblia/DSI fala
    engajamento   — Pergunta provocadora + reflexão + CTA

Formatos de saída:
    carrossel  — slides numerados, copy-paste pra Canva
    twitter    — thread 1/n com 280 chars/tweet
    legenda    — caption única de Instagram (parágrafos)
"""

# =====================================================================
# TEMPLATES POR PERFIL
# =====================================================================

# ----- PAZ NA CONTA (Finanças católicas) -----
PAZ_NA_CONTA = {
    "educacional": {
        "carrossel": {
            "titulo_visual": "💸 {tema}",
            "slides": [
                {
                    "slot": "gancho",
                    "titulo": "O fato",
                    "template": "💸 Você sabia?\n\n[Coloque aqui 1 dado ou fato surpreendente sobre {tema_curto}. Pode ser estatística, citação bíblica ou frase de impacto.]",
                    "placeholder_principal": "DADO: estatística, citação ou fato impactante sobre o tema",
                },
                {
                    "slot": "dor",
                    "titulo": "A dor real",
                    "template": "💔 O que ninguém fala\n\nA consequência prática disso: [descreva o problema real que isso causa — números, rotina, família, sono].",
                    "placeholder_principal": "CONSEQUÊNCIA: o que acontece na prática por causa desse problema",
                },
                {
                    "slot": "fe",
                    "titulo": "O que a fé diz",
                    "template": "✝️ A palavra\n\n\"[Versículo ou citação DSI relacionada ao tema]\"\n— [Referência bíblica ou documento]",
                    "placeholder_principal": "VERSÍCULO: passagem bíblica ou citação DSI que ilumina o tema",
                },
                {
                    "slot": "conselho",
                    "titulo": "O princípio",
                    "template": "💡 A regra\n\n[1 frase direta com o princípio prático. Evite jargão. Tom de conversa de café.]",
                    "placeholder_principal": "PRINCÍPIO: a regra de ouro ou insight central em 1 frase",
                },
                {
                    "slot": "passo",
                    "titulo": "3 passos práticos",
                    "template": "👉 Como aplicar hoje\n\n1. [Passo 1 — algo que cabe em 5 minutos]\n2. [Passo 2 — algo que cabe em 1 hora]\n3. [Passo 3 — algo pra fazer essa semana]",
                    "placeholder_principal": "3 PASSOS: ações concretas, do mais simples ao mais robusto",
                },
                {
                    "slot": "cta",
                    "titulo": "E agora?",
                    "template": "💬 Salva esse post e me conta nos comentários:\n\n[1 pergunta direta relacionada ao tema. Quem responde volta, e isso ajuda o post a chegar em mais gente.]",
                    "placeholder_principal": "PERGUNTA: 1 pergunta que faça o leitor pausar e responder",
                },
            ],
        },
        "twitter": {
            "titulo_visual": "🧵 {tema}",
            "slides": [
                {"slot": "gancho", "template": "1/6 🧵\n\n💸 Você sabia?\n\n{DADO}", "placeholder_principal": "DADO"},
                {"slot": "dor", "template": "2/6\n\nA consequência real:\n\n{CONSEQUÊNCIA}", "placeholder_principal": "CONSEQUÊNCIA"},
                {"slot": "fe", "template": "3/6\n\nA palavra a gente leva a sério:\n\n\"{VERSÍCULO}\"", "placeholder_principal": "VERSÍCULO"},
                {"slot": "conselho", "template": "4/6\n\nA regra de ouro:\n\n{PRINCÍPIO}", "placeholder_principal": "PRINCÍPIO"},
                {"slot": "passo", "template": "5/6\n\n3 passos pra começar hoje:\n• {PASSO1}\n• {PASSO2}\n• {PASSO3}", "placeholder_principal": "PASSOS"},
                {"slot": "cta", "template": "6/6\n\n{PERGUNTA}\n\n(Comenta aqui, salva, e segue pra parte 2 amanhã)", "placeholder_principal": "PERGUNTA"},
            ],
        },
        "legenda": {
            "titulo_visual": "💸 {tema}",
            "slides": [
                {
                    "slot": "legenda",
                    "template": "💸 {TITULO}\n\n[Parágrafo 1: 2-3 frases que abrem com o gancho. Pode começar com pergunta ou fato. Termina deixando claro sobre o que é o post.]\n\n[Parágrafo 2: 2-3 frases que aprofundam. Aqui entra o ângulo católico, DSI, ou vivência do casal. Tom pessoal, sem pregação.]\n\n[Parágrafo 3: 2-3 frases práticas — o que o leitor pode fazer HOJE. Termina com o propósito maior: pra quê.]\n\n—\nSalva esse post pra revisar depois. Marca alguém que precisa ler isso hoje. Comenta 'eu quero' pra receber o próximo da série.\n\n#paznaconta #{tag1} #{tag2} #{tag3}",
                    "placeholder_principal": "3 parágrafos: gancho → reflexão/DSI → passo prático",
                },
            ],
        },
    },
    "inspiracional": {
        "carrossel": {
            "titulo_visual": "💛 {tema}",
            "slides": [
                {"slot": "gancho", "titulo": "Antes", "template": "🌧️ Antes\n\n[Narrativa em 1ª pessoa do plural ou singular. Situação de vulnerabilidade — financeira, emocional, espiritual. Sem dramatizar, mas sem esconder.]", "placeholder_principal": "NARRATIVA: 2-3 frases honestas sobre o momento difícil"},
                {"slot": "dor", "titulo": "A virada", "template": "⚡ O que mudou\n\n[O momento ou decisão que mudou a trajetória. Pode ser uma frase, um livro, uma conversa, um evento.]", "placeholder_principal": "VIRADA: o que aconteceu que mudou a perspectiva"},
                {"slot": "fe", "titulo": "O que a fé ensinou", "template": "✝️ A palavra que sustentou\n\n\"[Versículo ou citação que sustentou a jornada. Pode ser uma que você viveu na pele.]\"", "placeholder_principal": "VERSÍCULO VIVIDO: passagem que acompanhou essa fase"},
                {"slot": "conselho", "titulo": "O que a gente aprendeu", "template": "📝 A lição\n\n[Em 1 frase, a lição — universalizável pro leitor. Evite clichê de coach. Tom de confissão compartilhada.]", "placeholder_principal": "LIÇÃO: o que você aprendeu que pode ajudar o leitor"},
                {"slot": "cta", "titulo": "Vem comigo", "template": "💛 E se você tá passando por isso agora:\n\n[2-3 frases de acolhimento. Sem sermão. Termina com convite suave — comentar, salvar ou marcar alguém.]", "placeholder_principal": "ACOLHIMENTO: fala com quem tá na mesma situação hoje"},
            ],
        },
    },
    "contraste": {
        "carrossel": {
            "titulo_visual": "⚖️ {tema}",
            "slides": [
                {"slot": "gancho", "titulo": "O que o mercado fala", "template": "📢 O que você ouve\n\n\"[Frase típica de coach/influencer/banco sobre o tema. Pode ser real ou reconstruída. Use aspas pra deixar claro que é citação.]\"", "placeholder_principal": "FRASE DO MERCADO: o que a cultura diz sobre o tema"},
                {"slot": "dor", "titulo": "O problema", "template": "⚠️ O que isso causa\n\n[Explique em 2 frases: por que seguir essa lógica leva a problema real. Use tom sóbrio, sem ironia.]", "placeholder_principal": "PROBLEMA: consequência prática de seguir essa lógica"},
                {"slot": "fe", "titulo": "O que a Bíblia fala", "template": "✝️ A palavra\n\n\"[Versículo oposto ou complementar à frase do mercado. Mesmo tema, lente diferente.]\"\n— [Referência]", "placeholder_principal": "VERSÍCULO CONTRASTE: passagem que ilumina por outro ângulo"},
                {"slot": "conselho", "titulo": "A posição católica", "template": "📜 O que a Igreja ensina\n\n[1-2 frases de princípio DSI. Não cite documento sem saber — use a ideia geral. Ex: destinação universal dos bens, primazia do trabalho sobre capital, opção preferencial pelos pobres.]", "placeholder_principal": "PRINCÍPIO DSI: ensino social da Igreja relacionado"},
                {"slot": "passo", "titulo": "Como praticar", "template": "👉 Na prática, hoje\n\n1. [Pequena ação 1]\n2. [Pequena ação 2]", "placeholder_principal": "PRÁTICA: 1-2 ações que equilibram o tema"},
                {"slot": "cta", "titulo": "E você?", "template": "💬 Concorda ou discorda?\n\n[1 pergunta direta. Tom respeitoso — o objetivo é conversa, não vencer debate. Sem moralismo.]", "placeholder_principal": "PERGUNTA: provoca reflexão, não briga"},
            ],
        },
    },
    "engajamento": {
        "carrossel": {
            "titulo_visual": "❓ {tema}",
            "slides": [
                {"slot": "gancho", "titulo": "Pergunta séria", "template": "❓ Pergunta real\n\n[1 pergunta que toca na dor do público. Evite pergunta genérica tipo 'o que você acha de X'. Vá fundo: o que a pessoa NÃO quer admitir pra si mesma.]", "placeholder_principal": "PERGUNTA PROFUNDA: que toca na dor real"},
                {"slot": "dor", "titulo": "Por que isso importa", "template": "💔 O que está em jogo\n\n[2 frases sobre a consequência de não resolver. Sem dramatizar, mas com clareza.]", "placeholder_principal": "CONSEQUÊNCIA: o que se perde se não encarar"},
                {"slot": "conselho", "titulo": "O que muda", "template": "💡 A virada\n\n[1 frase com o insight. Pode ser uma frase só — direta, memorável, compartilhável.]", "placeholder_principal": "INSIGHT: 1 frase que muda a perspectiva"},
                {"slot": "passo", "titulo": "Convite", "template": "👉 Vem praticar\n\n[1-2 frases de convite: comenta, marca alguém, responde à pergunta do slide 1. Tom de quem convida amigo pro café.]", "placeholder_principal": "CONVITE: ação concreta e simples de engajamento"},
            ],
        },
    },
}

# ----- TOQUE DE PAZ (Música e louvor com propósito) -----
TOQUE_DE_PAZ = {
    "educacional": {
        "carrossel": {
            "titulo_visual": "🎵 {tema}",
            "slides": [
                {"slot": "gancho", "titulo": "Você sabia?", "template": "🎵 Você sabia?\n\n[Dado, curiosidade ou fato sobre {tema_curto}. Pode ser histórico, técnico ou espiritual.]", "placeholder_principal": "DADO sobre música/louvor"},
                {"slot": "dor", "titulo": "Por que isso importa", "template": "💔 O ponto\n\n[Por que esse aspecto é relevante pra quem faz ou ouve música cristã.]", "placeholder_principal": "RELEVÂNCIA"},
                {"slot": "fe", "titulo": "A palavra", "template": "✝️ \"[Versículo sobre música, louvor ou adoração]\"", "placeholder_principal": "VERSÍCULO"},
                {"slot": "conselho", "titulo": "Prática", "template": "💡 Como aplicar\n\n[1 dica concreta pra quem compõe, canta ou escuta.]", "placeholder_principal": "DICA"},
                {"slot": "cta", "titulo": "Bora?", "template": "💬 Comenta: [pergunta sobre música/louvor]", "placeholder_principal": "PERGUNTA"},
            ],
        },
    },
    "inspiracional": {
        "carrossel": {
            "titulo_visual": "🎶 {tema}",
            "slides": [
                {"slot": "gancho", "titulo": "O momento", "template": "🎶 A gente lembra\n\n[Narrativa de um momento marcante com música/louvor]", "placeholder_principal": "MEMÓRIA"},
                {"slot": "fe", "titulo": "A palavra", "template": "✝️ \"[Versículo]\"", "placeholder_principal": "VERSÍCULO"},
                {"slot": "conselho", "titulo": "O que aprendemos", "template": "💡 [Lição]", "placeholder_principal": "LIÇÃO"},
                {"slot": "cta", "titulo": "Sua vez", "template": "💛 Comenta: [pergunta]", "placeholder_principal": "PERGUNTA"},
            ],
        },
    },
    "contraste": {
        "carrossel": {
            "titulo_visual": "🎵⚖️ {tema}",
            "slides": [
                {"slot": "gancho", "titulo": "A música do mundo", "template": "🎵 \"{frase de música secular}\"", "placeholder_principal": "FRASE SECULAR"},
                {"slot": "fe", "titulo": "A música do céu", "template": "✝️ \"{versículo ou Salmo}\"", "placeholder_principal": "VERSÍCULO"},
                {"slot": "conselho", "titulo": "A diferença", "template": "💡 [O que muda quando a gente reorienta]", "placeholder_principal": "DIFERENÇA"},
                {"slot": "cta", "titulo": "Sua vez", "template": "💬 [Pergunta]", "placeholder_principal": "PERGUNTA"},
            ],
        },
    },
}

# ----- CAMINHO VIDA (Formação e espiritualidade católica) -----
CAMINHO_VIDA = {
    "educacional": {
        "carrossel": {
            "titulo_visual": "🌿 {tema}",
            "slides": [
                {"slot": "gancho", "titulo": "Reflexão", "template": "🌿 Vamos refletir sobre {tema_curto}\n\n[Contextualize o tema: o que é, por que importa hoje]", "placeholder_principal": "CONTEXTO"},
                {"slot": "fe", "titulo": "O que a Igreja ensina", "template": "📜 [Catecismo, documento ou magistério relacionado]", "placeholder_principal": "ENSINO"},
                {"slot": "conselho", "titulo": "Como viver", "template": "💡 1 aplicação prática pra vida cotidiana", "placeholder_principal": "APLICAÇÃO"},
                {"slot": "passo", "titulo": "Exercício espiritual", "template": "🙏 1 exercício simples (leitura, oração, reflexão)", "placeholder_principal": "EXERCÍCIO"},
                {"slot": "cta", "titulo": "Sua vez", "template": "💬 [Pergunta sobre a prática]", "placeholder_principal": "PERGUNTA"},
            ],
        },
    },
    "inspiracional": {
        "carrossel": {
            "titulo_visual": "🌿💛 {tema}",
            "slides": [
                {"slot": "gancho", "titulo": "Testemunho", "template": "🌿 [Narrativa pessoal de um encontro com Deus nesse tema]", "placeholder_principal": "TESTEMUNHO"},
                {"slot": "fe", "titulo": "A palavra", "template": "✝️ \"[Versículo]\"", "placeholder_principal": "VERSÍCULO"},
                {"slot": "conselho", "titulo": "O que ficou", "template": "💡 [Lição que ficou]", "placeholder_principal": "LIÇÃO"},
                {"slot": "cta", "titulo": "Sua vez", "template": "💬 [Pergunta sobre a experiência]", "placeholder_principal": "PERGUNTA"},
            ],
        },
    },
    "engajamento": {
        "carrossel": {
            "titulo_visual": "❓ {tema}",
            "slides": [
                {"slot": "gancho", "titulo": "Pergunta", "template": "❓ [Pergunta profunda sobre {tema_curto}]", "placeholder_principal": "PERGUNTA"},
                {"slot": "fe", "titulo": "A palavra", "template": "✝️ \"[Versículo]\"", "placeholder_principal": "VERSÍCULO"},
                {"slot": "conselho", "titulo": "Para pensar", "template": "💡 [Reflexão]", "placeholder_principal": "REFLEXÃO"},
                {"slot": "cta", "titulo": "Sua vez", "template": "💬 Comenta: [pergunta]", "placeholder_principal": "PERGUNTA"},
            ],
        },
    },
}

# ----- GENÉRICO (fallback) -----
GENERICO = {
    "educacional": {
        "carrossel": {
            "titulo_visual": "📌 {tema}",
            "slides": [
                {"slot": "gancho", "titulo": "Você sabia?", "template": "📌 Você sabia?\n\n[Dado/fato sobre {tema_curto}]", "placeholder_principal": "DADO"},
                {"slot": "dor", "titulo": "O problema", "template": "💔 [Consequência prática]", "placeholder_principal": "CONSEQUÊNCIA"},
                {"slot": "conselho", "titulo": "A ideia", "template": "💡 [Insight central]", "placeholder_principal": "INSIGHT"},
                {"slot": "passo", "titulo": "3 passos", "template": "👉 1. [Passo]\n2. [Passo]\n3. [Passo]", "placeholder_principal": "PASSOS"},
                {"slot": "cta", "titulo": "E você?", "template": "💬 [Pergunta]", "placeholder_principal": "PERGUNTA"},
            ],
        },
    },
}


# =====================================================================
# REGISTRY
# =====================================================================

TEMPLATES = {
    "paz-na-conta": PAZ_NA_CONTA,
    "toque-de-paz": TOQUE_DE_PAZ,
    "caminho-vida": CAMINHO_VIDA,
    "generico": GENERICO,
}


# =====================================================================
# HELPERS
# =====================================================================

TIPOS_DISPONIVEIS = ["educacional", "inspiracional", "contraste", "engajamento"]
FORMATOS_DISPONIVEIS = ["carrossel", "twitter", "legenda"]


def _tema_curto(tema: str, max_len: int = 28) -> str:
    """Versão curta do tema pra usar em títulos de slide."""
    if len(tema) <= max_len:
        return tema
    return tema[: max_len - 3].rstrip() + "..."


def _tema_titulo(tema: str) -> str:
    """Tema em CAIXA ALTA pra títulos visuais."""
    return tema.upper()[:50]


def pick_template(perfil_id: str, tipo: str, formato: str) -> dict:
    """Retorna o template (perfil, tipo, formato), com fallback para generico.

    Args:
        perfil_id: id do perfil.
        tipo: educacional | inspiracional | contraste | engajamento.
        formato: carrossel | twitter | legenda.

    Returns:
        dict com 'titulo_visual' e 'slides' (lista de slots).
    """
    perfil = TEMPLATES.get(perfil_id) or TEMPLATES["generico"]

    # Tenta tipo exato; se não, cai no educacional
    tipos_perfil = perfil.get(tipo) or perfil.get("educacional") or GENERICO["educacional"]

    # Tenta formato; se não, cai no carrossel
    formato_cfg = tipos_perfil.get(formato) or tipos_perfil.get("carrossel") or GENERICO["educacional"]["carrossel"]

    return formato_cfg


def listar_tipos(perfil_id: str) -> list[str]:
    """Lista os tipos disponíveis para um perfil."""
    perfil = TEMPLATES.get(perfil_id, GENERICO)
    return list(perfil.keys())


def listar_formatos(perfil_id: str, tipo: str) -> list[str]:
    """Lista os formatos disponíveis para um (perfil, tipo)."""
    cfg = pick_template(perfil_id, tipo, "carrossel")
    return ["carrossel", "twitter", "legenda"]
