---
name: "Inconsistência caminho transcrição — profile-aware vs global"
description: "Agente de transcrição salvava em acervo/ raiz, mas endpoints liam de perfis/<id>/acervo/ — resolvido com fallback"
tipo: licao
updated_at: 2026-06-26
tags: transcricao, profile, path, api
---

# Inconsistência de Caminhos — Transcrição

## Problema
O agente `agents/transcricao/main.py` salvava transcrições em `PROJECT_PATH / "acervo" / "transcricoes"` (caminho hardcoded), enquanto os endpoints da API (`/api/transcricoes`, `/api/transcricao/ler`, `/api/transcricao/analisar`) liam de `get_acervo_path_for_user() / "transcricoes"`, que resolvia para `perfis/<ativo>/acervo/transcricoes/`.

Resultado: transcrições salvas nunca eram encontradas pelos endpoints.

## Causa Raiz
- O agente foi escrito antes do sistema multi-perfil existir
- Quando o multi-perfil foi implementado, `get_acervo_path_for_user()` passou a retornar caminho profile-aware
- Mas o agente de transcrição nunca foi atualizado

## Solução
1. **Agente**: `ACERVO_PATH` agora usa `profile_manager.get_acervo_path()`, com fallback para o caminho global se falhar
2. **API**: helper `_encontrar_transcricao(nome)` que busca no profile ativo primeiro, depois no `acervo/` global
3. **Listagem**: `GET /api/transcricoes` agora varre ambos os diretórios, deduplicando por nome de arquivo

## Lições
- **Sempre atualizar agentes existentes ao mudar a estrutura de paths**
- **Fallbacks são essenciais**: o caminho global antigo continua existindo com dados históricos
- **Testar ponta-a-ponta**: o bug só apareceu ao testar o fluxo completo (transcrição → análise)
