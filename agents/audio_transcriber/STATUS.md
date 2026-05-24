# Status - Audio Transcriber

- **Implementacao**: Completa
- **Dependencias**: ffmpeg + (ollama whisper ou vosk)
- **Modelo preferido**: Ollama whisper (mais preciso)
- **Fallback**: Vosk (offline, funciona no Termux)
- **Integracao**: Telegram Bot (/audio), API Server, Plataforma Web

## Fluxo
1. Recebe audio file path
2. Converte para WAV 16kHz mono (FFmpeg)
3. Tenta Ollama whisper → fallback Vosk
4. Salva transcricao completa em acervo/transcricoes/
5. Salva como ideia em acervo/ideias/
6. Retorna texto transcrito via stdout
