"""formatter.py — Formata transcricao de audio para mensagem Telegram."""

from datetime import datetime

MAX_MSG_LENGTH = 4096


def format_telegram_message(texto: str, stats: dict = None) -> list[str]:
    """Formata transcricao em mensagens Telegram (HTML parse_mode).

    Retorna lista de mensagens (divide se passar do limite de 4096 chars).
    """
    if stats is None:
        stats = {}

    cabecalho = (
        f"🎤 <b>AUDIO TRANSCRIBER</b> — {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        f"📝 Transcricao concluida\n"
        f"📊 Tamanho: {len(texto)} caracteres\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
    )

    rodape = (
        f"\n━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 Ideia salva em acervo/ideias/\n"
        f"📄 Transcricao em acervo/transcricoes/"
    )

    if not texto.strip():
        return [cabecalho + "<i>Transcricao vazia</i>" + rodape]

    messages = []
    current = cabecalho + f"<pre>{texto[:3000]}</pre>"

    if len(current) + len(rodape) > MAX_MSG_LENGTH:
        corte = MAX_MSG_LENGTH - len(cabecalho) - len(rodape) - 100
        current = cabecalho + f"<pre>{texto[:corte]}</pre>" + f"\n\n<i>(truncado, {len(texto)} chars ao todo)</i>"
        current += rodape
        messages.append(current)

        if len(texto) > corte:
            resto = texto[corte:]
            while resto:
                bloco = f"🎤 <b>Audio Transcriber</b> (cont.)\n<pre>{resto[:3500]}</pre>"
                if len(resto) > 3500:
                    resto = resto[3500:]
                else:
                    bloco += "\n\n✅ Fim da transcricao"
                    resto = ""
                messages.append(bloco)
    else:
        current += rodape
        messages.append(current)

    return messages


def format_error_message(erro: str) -> list[str]:
    """Formata mensagem de erro."""
    return [
        f"❌ <b>Audio Transcriber</b>\n\n"
        f"Erro ao transcrever:\n<code>{erro}</code>\n\n"
        f"💡 Dica: Envie a ideia em texto com /ideia [texto]"
    ]
