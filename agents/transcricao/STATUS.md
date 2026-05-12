# STATUS.md — Agente Transcrição

> Saúde e métricas do agente

## Status

| Métrica | Valor |
|---------|-------|
| **Online** | ✅ Pronto |
| **Biblioteca** | youtube-transcript-api |
| **Transcrições** | 0 |

## Funcionalidades

| Recurso | Status |
|---------|--------|
| Extrair ID do YouTube | ✅ |
| Baixar transcript | ✅ |
| Suporte PT/EN | ✅ |
| Timestamps | ✅ |
| Buscar em transcrições | ✅ |

## Como usar

```bash
cd agents/transcricao

# Transcrever vídeo
python main.py "https://youtube.com/watch?v=VIDEO_ID"

# Listar transcrições
python main.py --listar

# Ler transcrição
python main.py --ler "nome_do_arquivo"

# Buscar palavra
python main.py --buscar "IA"
```

## Dependências

```
pip install youtube-transcript-api
```

---

_Last updated: 2026-05-12_