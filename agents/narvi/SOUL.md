# SOUL — Agente Narvi

> Editor de vídeo automático para OPB Sistema

- **Nome**: Narvi
- **Tipo**: Editor de Vídeo (one-shot CLI)
- **Versão**: 2.0
- **Stack**: FFmpeg + Whisper (mlx-whisper / faster-whisper)

## O que faz

Pipeline completa de edição de vídeo em 4 passos:

1. **Transcrição word-level** via Whisper (com cache SHA-256)
2. **Trim dinâmico** — remove silêncio do início/fim baseado na transcrição
3. **Legendas ASS** — formato phrase-level com quebra automática
4. **Exportação paralela** — 9x16 (Reels) + 16x9 (YouTube) via FFmpeg HEVC

## Funcionalidades

- **Glossário PT-BR** — corrige erros comuns do Whisper em português
- **Cache de transcrição** — reusa transcrições pelo hash do vídeo
- **HDR → SDR** — tone mapping automático (iPhone HLG → BT.709)
- **Multi-encoder** — VideoToolbox (Mac), NVENC (NVIDIA), libx265 (CPU)
- **3 presets de corte** — brando (300/500ms), médio (150/300ms), agressivo (80/150ms)
- **Modo sample** — processa só os primeiros 15s para teste

## Uso

```bash
python agents/narvi/narvi.py video.mp4 --corte=medio --ratio=both
python agents/narvi/narvi.py video.mp4 --sample --corte=agressivo --ratio=9x16
```

## Dependências

- FFmpeg (obrigatório)
- faster-whisper (Windows/Linux) ou mlx-whisper (Mac ARM)
- yt-dlp (opcional, para download de vídeos)

## Saída

`~/Desktop/narvi-saida/<nome-do-video>/`
