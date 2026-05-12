# STATUS.md — Agente Posicionamento

> Saúde e métricas do agente

## Status

| Métrica | Valor |
|---------|-------|
| **Online** | ✅ Pronto para usar |
| **Última pesquisa** | Nenhuma |
| **Perfis salvos** | 0 |

## Funcionalidades

| Recurso | Status |
|---------|--------|
| Pesquisa Google | ✅ |
| Identificação de plataforma | ✅ |
| Cálculo de relevância | ✅ |
| Salvamento no cérebro | ✅ |
| Relatório consolidado | ✅ |

## Como usar

```bash
cd agents/posicionamento
python main.py "sua palavra-chave"
```

## Exemplos de Pesquisa

```bash
python main.py "IA para pequenos negócios"
python main.py "produtividade entrepreneur"
python main.py "automação marketing digital"
python main.py "solopreneur brasileiro"
```

## Configuração

- **API**: DuckDuckGo API (gratuita)
- **Saída**: `acervo/pesquisas/perfis/` e `acervo/pesquisas/relatorios/`

---

_Last updated: 2026-05-12_