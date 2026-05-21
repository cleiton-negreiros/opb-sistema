# SOUL.md — Agente Corta Silencio

> Cortador de silencios leve e rapido via FFmpeg

## Identidade

- **Nome**: Corta Silencio
- **Tipo**: Editor de Video — corte de silencios por analise de audio
- **Stack**: Python 3.8+, FFmpeg (apenas)
- **Versao**: 1.0

## Proposito

Alternativa simples e mobile-friendly ao agente Narvi. Remove silencios
de videos usando apenas o filtro `silencedetect` do FFmpeg — sem Whisper,
sem transcricao, sem bibliotecas pesadas de audio.

Ideal para:
- Processamento rapido em Termux (Android)
- PCs sem GPU
- Videos onde transcricao por Whisper e exagero
- Lotes de videos que precisam de limpeza automatica

## Como funciona

```
Video de entrada
       ↓
[1/3] FFmpeg silencedetect → detecta silencios (dB + duracao)
       ↓
[2/3] Corta segmentos nao-silenciosos (-c copy, sem re-encode)
       ↓
[3/3] Concat demuxer → junta tudo em um arquivo
       ↓
Video limpo em output/corta-silencio/
```

## Configuracoes

| Parametro | Padrao | Descricao |
|-----------|--------|-----------|
| `--threshold` | -30dB | Nivel de silencio (mais negativo = mais sensivel) |
| `--min-duration` | 0.5s | Duracao minima para considerar como silencio |
| `--keep-silence` | 0.0s | Segundos de silencio para manter nos cortes |

## Exemplos de Uso

```bash
# Basico — usa padroes
python main.py video.mp4

# Mais sensivel (corta mais)
python main.py video.mp4 --threshold -25

# Mais agressivo (corta silencios curtos tambem)
python main.py video.mp4 --min-duration 0.3

# Mantem 0.3s de transicao em cada corte
python main.py video.mp4 --keep-silence 0.3

# Saida customizada
python main.py video.mp4 --output resultado.mp4
```

## Instalacao

### PC (Windows)
```bash
choco install ffmpeg
# ou baixe de https://ffmpeg.org/download.html
```

### Termux (Android)
```bash
pkg install ffmpeg python
pip install --no-deps .
```

## Diferencas vs Narvi

| Caracteristica | Narvi | Corta Silencio |
|----------------|-------|----------------|
| Deteccao | Whisper (IA) | FFmpeg silencedetect |
| Preciso | Word-level | Audio level |
| Velocidade | Lento (minutos) | Rapido (segundos) |
| Dependencias | torch, faster-whisper | So FFmpeg |
| Termux | Nao roda | Roda |
| GPU | Opcional | Nao precisa |
| Re-encode | Sim (HEVC) | Nao (-c copy) |

---

_Last updated: 2026-05-21_
