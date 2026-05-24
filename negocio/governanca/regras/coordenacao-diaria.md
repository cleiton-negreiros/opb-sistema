---
name: "Coordenacao Diaria de Agentes"
description: "Rotina de orquestracao que integra consultor, coordenador e auditores para iniciar o dia com contexto e acao"
tipo: regra
updated_at: 2026-05-23
---

# Coordenacao Diaria de Agentes

> TODO dia, ao iniciar o sistema, o coordenador orquestra: auditoria → consultor (insight) → sugestao de agentes.

## Ciclo Matinal

```
[1/5] Auditoria de codigo     → audit/auditoria_diaria.py --quick
[2/5] Listar agentes          → coordinator list
[3/5] Insight diario          → consultor-negocios insight_diario
[4/5] Saude do cerebro        → load_brain_context()
[5/5] Proximos passos         → sugestao baseada em contexto
```

## Como Executar

```bash
# Ciclo completo (recomendado)
python agents/coordinator/main.py morning

# Apenas sugestao de orquestracao
python agents/coordinator/main.py orchestrate

# Insight diario direto do consultor
python agents/consultor-negocios/main.py insight_diario

# Revisao completa do contexto
python agents/consultor-negocios/main.py revisao_contexto

# Sugestao de quais agentes rodar hoje
python agents/consultor-negocios/main.py coordenacao_agentes
```

## Integracoes

| Disparo | O que roda | Onde |
|---------|------------|------|
| `morning_routine.py` | Auditoria → Coordenador → Consultor | Startup manual |
| `iniciar-startup.bat` | Auditoria → Coordenador → Morning routine | Startup automatico |
| `python coordinator/main.py morning` | Ciclo completo independente | Terminal |

## Tipos de Consulta do Consultor

| Tipo | Descricao | Quando usar |
|------|-----------|-------------|
| `insight_diario` | 3 insights baseados em TODO contexto coletado | Todo dia ao iniciar |
| `revisao_contexto` | Gap analysis + oportunidades + riscos + agenda 7 dias | Semanalmente |
| `coordenacao_agentes` | Tabela de agentes priorizados para o dia | Ao planejar o dia |
| `planejamento_estrategico` | Plano estrategico integrado (original) | Quando precisar |
| `analise_swot` | SWOT de negocio especifico | Ao lancar algo novo |

## Outputs

- `output/consultoria/consultoria_*.md` — Insights e consultorias geradas
- `output/coordenacao/morning_*.json` — Logs de coordenacao diaria

## Gatilhos

- **Startup**: roda automaticamente via `iniciar-startup.bat`
- **Manual**: `python agents/coordinator/main.py morning`
- **Apos mudancas grandes**: rodar `revisao_contexto` para recalibrar

## Historico

| Data | Resultado |
|------|-----------|
| 2026-05-23 | Implementado: consultor com 3 novos tipos, coordenador com ciclo matinal, integrado a startup |
