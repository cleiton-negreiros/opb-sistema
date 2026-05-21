# Transcrever Audio Agent

Agente que transcreve arquivos de audio (mensagens de voz do Telegram) para texto.

## Funcao

Converte audio OGG/OPUS/MP3 para WAV 16kHz mono e transcreve usando o motor disponivel.

## Motores (ordem de preferencia)

1. **Ollama + Whisper** - Se disponivel
2. **Vosk** - Offline, leve, funciona no Termux/Android
3. **Fallback** - Salva audio para transcricao manual

## Uso

```bash
python main.py audio.ogg
python main.py audio.opus --output-dir /path/to/output
```

## Dependencias

- FFmpeg (conversao de audio)
- vosk (opcional, transcricao offline)
- ollama + whisper (opcional, transcricao via IA)

## Compatibilidade

- Windows (PC)
- Linux
- Termux (Android)

## Output

Transcricoes salvas em `acervo/transcricoes/` com timestamp.
