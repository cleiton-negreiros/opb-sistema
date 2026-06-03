# STATUS.md — NegreirosBot

> Saúde e métricas do agente

## Status

| Métrica | Valor |
|---------|-------|
| **Online** | ✅ Sim |
| **Token** | Configurado via .env ou variável de ambiente |
| **Ideias salvas** | (automático) |
| **Plataformas** | ✅ Windows, ✅ Termux (Android), ✅ Linux/Mac |

## Comandos Disponíveis

| Comando | Status | Ollama? | Mobile? |
|---------|--------|---------|---------|
| `/start`, `/help`, `/status` | ✅ | Não | ✅ |
| `/ideia`, `/ideias`, `/listar` | ✅ | Não | ✅ |
| `/cerebro`, `/regras`, `/projetos` | ✅ | Não | ✅ |
| `/posicionamento`, `/meuid` | ✅ | Não | ✅ |
| `/agents`, `/hub`, `/executar` | ✅ | Não | ✅ |
| `/tarefas`, `/tarefa`, `/concluir` | ✅ | Não | ✅ |
| `/plano`, `/briefing` | ✅ | Não | ✅ |
| `/liturgico` | ✅ | Não (standalone) | ✅ |
| `/reels` | ✅ | Fallback offline | ✅ |
| `/hashtags` | ✅ | Fallback offline | ✅ |
| `/cortarsilencio` | ✅ | Não (FFmpeg) | ✅ |
| `/carrossel` | ✅ | Sim | ⚠️ |
| `/texto` | ✅ | Sim | ⚠️ |
| `/capavideo` | ✅ | Sim | ⚠️ |
| `/consumo` | ✅ | Sim | ⚠️ |
| `/radagast` | ✅ | Sim | ⚠️ |
| `/iniciar` | ✅ | Adaptativo | ✅ |
| `/audio` | ✅ | Whisper | ⚠️ lento |
| Enviar vídeo | ✅ | Não (FFmpeg) | ✅ |

## Configuração

- **Token**: `(configurado via .env ou variável de ambiente)`
- **Pasta de saída**: `acervo/ideias/`
- **Modo**: Polling (contínuo)

---

_Last updated: 2026-05-24_
