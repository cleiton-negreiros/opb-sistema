---
name: "Telegram Carrossel Interativo"
description: "Integração botão-inline no Telegram para gerar carrosséis com perfil e tipo"
tipo: tarefa
status: pendente
prioridade: alta
created_at: 2026-06-25
---

# Telegram Carrossel Interativo

> Comando `/carrossel [ideia]` com botões inline para perfil e tipo

## Objetivo
Enviar uma ideia no bot Telegram → selecionar perfil e tipo via botões inline → gerar carrossel → receber resultado no chat.

## Fluxo
1. Usuário envia `/carrossel [ideia]`
2. Bot mostra botões inline: **Perfil** (paz-na-conta, toque-de-paz, caminho-vida)
3. Usuário seleciona perfil
4. Bot mostra botões inline: **Tipo** (educacional, inspiracional, contraste, engajamento)
5. Bot gera carrossel com `agents/carrossel/main.py --perfil <sel> --tipo <sel>`
6. Bot envia resultado (texto se < 4000 chars, documento .md se maior)

## Arquivos
- `agents/telegram_bot/main.py` — adicionar ConversationHandler + CallbackQueryHandler
- Imports: `ConversationHandler`, `CallbackQueryHandler`, `InlineKeyboardButton`, `InlineKeyboardMarkup`

## States
```
PROFILE_SELECTED = 0
TYPE_SELECTED = 1
```

## Callbacks
- `perfil:<id>` — ex: `perfil:paz-na-conta`
- `tipo:<tipo>` — ex: `tipo:educacional`
- `carrossel:cancelar` — cancela operação

## Comandos extras
- `/carrossels` — listar carrosséis salvos (usando `--listar` do agente)
- `/carrossel [ideia] --perfil paz-na-conta --tipo contraste` — modo rápido (sem botões)

## Notas
- Agente carrossel já suporta `--perfil` e `--tipo`
- Fallback `--sem-llm` quando Ollama offline
- Output salvo em `perfis/<id>/acervo/carrossel/` e `_conteudo/carrossel/`
