"""transcriber.py — Núcleo de transcrição de áudio.

Reimplementa a lógica do agents/transcrever-audio com:
- Conversão FFmpeg para WAV 16kHz mono
- Tentativa Ollama whisper → fallback Vosk
- Salvamento em acervo/transcricoes/ + acervo/ideias/
- State tracking (.state.json)
"""

import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("audio_transcriber")

PROJECT_PATH = Path(__file__).parent.parent.parent
STATE_PATH = Path(__file__).parent / ".state.json"
ACERVO_TRANS = PROJECT_PATH / "acervo" / "transcricoes"
ACERVO_IDEAS = PROJECT_PATH / "acervo" / "ideias"
ACERVO_TEMP = PROJECT_PATH / "acervo" / "temp"


def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"transcricoes": [], "total": 0, "last_run": None}


def save_state(state: dict):
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def convert_to_wav(input_path: str, output_path: str) -> bool:
    """Converte audio para WAV 16kHz mono S16."""
    logger.info(f"Convertendo {input_path} → WAV...")
    cmd = ["ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", "-sample_fmt", "s16", output_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"FFmpeg erro: {result.stderr}")
        return False
    return True


def try_ollama_whisper(wav_path: str) -> str | None:
    """Tenta transcricao via Ollama whisper."""
    try:
        r = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        if "whisper" not in r.stdout.lower():
            return None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None

    logger.info("Transcrevendo com Ollama whisper...")
    try:
        r = subprocess.run(["ollama", "run", "whisper", wav_path], capture_output=True, text=True, timeout=300)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def try_vosk(wav_path: str) -> str | None:
    """Tenta transcricao via Vosk (offline, Termux)."""
    try:
        import json as j
        import wave
        import vosk
    except ImportError:
        return None

    logger.info("Transcrevendo com Vosk...")
    try:
        model_path = str(Path(__file__).parent / "vosk-model-small-pt")
        if not os.path.exists(model_path):
            model_path = str(Path(__file__).parent / "vosk-model-small-en-us")
        if not os.path.exists(model_path):
            logger.warning("Modelo Vosk nao encontrado.")
            return None

        wf = wave.open(wav_path, "rb")
        model = vosk.Model(model_path)
        rec = vosk.KaldiRecognizer(model, wf.getframerate())

        text = []
        while True:
            data = wf.readframes(4000)
            if not data:
                break
            if rec.AcceptWaveform(data):
                result = j.loads(rec.Result())
                if result.get("text"):
                    text.append(result["text"])

        final = j.loads(rec.FinalResult())
        if final.get("text"):
            text.append(final["text"])

        wf.close()
        return " ".join(text).strip()
    except Exception as e:
        logger.error(f"Vosk erro: {e}")
        return None


def save_transcription(texto: str, audio_filename: str, usuario: str = "audio_transcriber") -> dict:
    """Salva transcricao completa + ideia. Retorna dict com caminhos."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    data_iso = datetime.now().strftime("%Y-%m-%d")
    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in Path(audio_filename).stem)

    # --- Salva transcricao completa ---
    ACERVO_TRANS.mkdir(parents=True, exist_ok=True)
    trans_path = ACERVO_TRANS / f"audio_{safe_name}_{timestamp}.md"
    trans_content = f"""---
name: "Transcricao {timestamp}"
tipo: transcricao_audio
autor: {usuario}
data: {data_iso}
origem: {audio_filename}
---

# Transcricao de Audio

**Arquivo:** {audio_filename}
**Data:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Status:** Transcrito

---

{texto}

---

*Transcrito via Audio Transcriber Agent*"""
    trans_path.write_text(trans_content.strip(), encoding="utf-8")
    logger.info(f"Transcricao salva: {trans_path}")

    # --- Salva como ideia (primeiros 500 chars) ---
    ACERVO_IDEAS.mkdir(parents=True, exist_ok=True)
    idea_texto = texto[:500].strip()
    idea_path = ACERVO_IDEAS / f"audio_{timestamp}.md"
    idea_content = f"""---
name: "Ideia por Audio {timestamp}"
description: "{idea_texto[:80]}..."
tipo: ideia
tags: [audio, transcricao]
updated_at: {data_iso}
autor: {usuario}
---

# {idea_texto}

**Data:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Fonte:** Audio ({audio_filename})
**Status:** Transcrito e salvo como ideia

---

*Gerado pelo Audio Transcriber Agent*"""
    idea_path.write_text(idea_content.strip(), encoding="utf-8")
    logger.info(f"Ideia salva: {idea_path}")

    return {
        "transcricao": str(trans_path),
        "ideia": str(idea_path),
        "timestamp": timestamp,
    }


def transcrever(audio_path: str, usuario: str = "audio_transcriber") -> dict:
    """Pipeline principal: recebe path de audio, retorna transcricao."""
    audio_path = Path(audio_path)
    if not audio_path.exists():
        return {"erro": f"Arquivo nao encontrado: {audio_path}", "sucesso": False}

    ACERVO_TEMP.mkdir(parents=True, exist_ok=True)
    temp_wav = ACERVO_TEMP / f"transc_{audio_path.stem}.wav"
    ext = audio_path.suffix.lower()

    try:
        if ext == ".wav":
            wav_path = str(audio_path)
        else:
            if not convert_to_wav(str(audio_path), str(temp_wav)):
                return {"erro": "Falha na conversao FFmpeg", "sucesso": False}
            wav_path = str(temp_wav)

        texto = try_ollama_whisper(wav_path)
        if not texto:
            texto = try_vosk(wav_path)

        if not texto:
            return {"erro": "Nenhum motor de transcricao disponivel (instale Ollama whisper ou Vosk)", "sucesso": False}

        resultado = save_transcription(texto, audio_path.name, usuario)

        # Atualiza state
        state = load_state()
        state["transcricoes"].append({
            "arquivo": audio_path.name,
            "timestamp": resultado["timestamp"],
            "tamanho": len(texto),
        })
        state["total"] = len(state["transcricoes"])
        state["last_run"] = datetime.now().isoformat()
        state["transcricoes"] = state["transcricoes"][-100:]  # keep last 100
        save_state(state)

        return {
            "sucesso": True,
            "texto": texto,
            "transcricao_path": resultado["transcricao"],
            "ideia_path": resultado["ideia"],
        }

    finally:
        if ext != ".wav" and temp_wav.exists():
            temp_wav.unlink()
