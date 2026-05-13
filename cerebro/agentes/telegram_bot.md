---
name: "Agente Telegram Bot"
description: "NegreirosBot — captura de ideias e execução remota via Telegram"
tipo: agente
updated_at: 2026-05-12
---

# Agente Telegram Bot

> Bot de captura de ideias + execução remota via Telegram (PC / Termux)

## Capacidades

- **Captura de ideias**: Mensagens de texto são salvas automaticamente em `acervo/ideias/`
- **Notas de voz**: Mensagens de voz são registradas para transcrição futura
- **Execução remota**: Comando `/executar` roda comandos no dispositivo
- **Cérebro completo**: Acessa identidade, projetos, agentes e regras via comandos
- **Rotina matinal**: `/iniciar` mostra resumo do dia

## Comandos

| Comando | Função |
|---------|--------|
| `/start` | Apresentação inicial |
| `/help` | Lista de comandos |
| `/ideia [texto]` | Cadastrar ideia formal |
| `/listar` | Ver últimas 5 ideias |
| `/status` | Estatísticas do sistema |
| `/agents` | Listar agentes disponíveis |
| `/hub` | URL do hub de produtividade |
| `/executar [cmd]` | Executar comando no dispositivo |
| `/projetos` | Projetos ativos do cérebro |
| `/regras` | Regras de identidade |
| `/cerebro` | Resumo completo do cérebro |
| `/ideias` | Últimas 10 ideias |
| `/transcrever` | Instruções de transcrição |
| `/obsidian` | Integração com Obsidian |
| `/iniciar` | Rotina matinal |

## Uso

```bash
cd agents/telegram_bot
python main.py
```

## Saída

- `acervo/ideias/AAAA-MM-DD_HH-MM-SS.md`

## Dependências

- python-telegram-bot
- requests
- Ollama (para rotina matinal)
- Python 3.8+