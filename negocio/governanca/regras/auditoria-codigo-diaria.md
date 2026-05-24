---
name: "Auditoria de Código Diária"
description: "Rotina de verificação automática da qualidade do código frontend (HTML/CSS/JS/PWA)"
tipo: regra
updated_at: 2026-05-23
---

# Auditoria de Código Diária

> Corre automaticamente toda manhã via `morning_routine.py`. Pode ser executada manualmente a qualquer momento.

## Como Executar

```bash
# Completa (integra à rotina matinal)
python morning_routine.py --audit

# Apenas auditoria rápida (críticos + PWA)
python audit/auditoria_diaria.py --quick

# Seções específicas
python audit/auditoria_diaria.py --html
python audit/auditoria_diaria.py --css
python audit/auditoria_diaria.py --js
python audit/auditoria_diaria.py --pwa
python audit/auditoria_diaria.py --api
```

## O Que é Verificado

### HTML
- IDs duplicados (causam `getElementById` imprevisível)
- Variáveis CSS indefinidas em estilos inline
- Comentários grandes ou código morto

### CSS
- Prefixed `-webkit-` para `backdrop-filter`
- Abuso de `!important`
- Regras vazias
- Cores hardcoded fora do tema

### JavaScript
- Funções duplicadas entre arquivos
- Globais implícitas (sem `let`/`const`/`var`)
- `console.log` em produção
- Consistência de chamadas de API

### PWA
- Manifest.json completo (name, icons, display, start_url)
- Service Worker operacional (fetch handler + cache)
- apple-touch-icon para iOS
- Ícones em quantidade suficiente

### API
- Todas as chamadas frontend têm rotas correspondentes no backend
- Health check dos agentes

## Critérios de Bloqueio

| Nível | Ação |
|-------|------|
| 🔴 Erro | Deve ser corrigido antes do próximo commit |
| 🟡 Aviso | Deve ser revisado na semana |
| 🟢 OK | Tudo limpo |

## Gatilhos Automáticos

- **Ao iniciar o dia**: roda como parte da `morning_routine.py`
- **Antes de deploy**: rodar `python audit/auditoria_diaria.py` – se houver erros, não fazer deploy
- **Após grandes refatorações**: rodar completo para detectar regressões

## Histórico

| Data | Resultado | Observações |
|------|-----------|-------------|
| 2026-05-23 | ✅ Implementado | Auditoria criada e integrada à morning routine |
