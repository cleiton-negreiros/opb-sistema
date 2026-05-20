#!/usr/bin/env python3
"""formatter.py — Formata ideias de Reels para mensagem Telegram."""

from datetime import datetime

# Limite do Telegram para uma mensagem
MAX_MSG_LENGTH = 4096


EMOJI_DIGITOS = {
    "0": "0️⃣", "1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣",
    "5": "5️⃣", "6": "6️⃣", "7": "7️⃣", "8": "8️⃣", "9": "9️⃣",
}


def _numero_emoji(n: int) -> str:
    """Converte número inteiro em dígitos emoji (10 → 1️⃣0️⃣)."""
    return "".join(EMOJI_DIGITOS[d] for d in str(n))


def format_telegram_message(ideas: list[dict], stats: dict) -> list[str]:
    """Formata ideias em mensagens Telegram (HTML parse_mode).

    Retorna lista de mensagens (divide se passar do limite).
    """
    header = (
        f"🦉 <b>RADAGAST</b> — Curadoria {datetime.now().strftime('%d/%m/%Y')}\n\n"
        f"📊 Varridos: {stats.get('total_items', 0)} posts de {stats.get('platforms', 0)} plataformas\n"
        f"💡 Ideias geradas: {len(ideas)}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
    )

    footer = (
        f"\n━━━━━━━━━━━━━━━━━━━━\n"
        f"⏰ Proximo scan: amanha 6h30"
    )

    idea_blocks = []
    for i, idea in enumerate(ideas, 1):
        pontos = ""
        if idea.get("pontos"):
            pontos = "\n".join(f"  • {p}" for p in idea["pontos"])

        numero = _numero_emoji(i)
        block = (
            f"\n{numero} <b>{idea.get('titulo', 'Sem titulo')}</b>\n"
            f"🎣 <i>\"{idea.get('hook', '')}\"</i>\n"
        )
        if pontos:
            block += f"{pontos}\n"
        if idea.get("formato_sugerido"):
            block += f"🎬 {idea['formato_sugerido']}\n"
        if idea.get("fonte_url"):
            block += f"🔗 {idea['fonte_url']}\n"
        if idea.get("angulo_br"):
            block += f"🇧🇷 {idea['angulo_br']}\n"

        idea_blocks.append(block)

    # Montar mensagens respeitando limite
    messages = []
    current = header

    for block in idea_blocks:
        if len(current) + len(block) + len(footer) > MAX_MSG_LENGTH:
            # Fechar mensagem atual
            current += f"\n<i>(continua...)</i>"
            messages.append(current)
            current = f"🦉 <b>RADAGAST</b> (cont.)\n"

        current += block

    current += footer
    messages.append(current)

    return messages
