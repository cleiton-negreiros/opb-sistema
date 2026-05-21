#!/usr/bin/env python3
"""Transcrever Audio Agent - Transcribes audio files (Telegram voice messages) to text."""

import argparse
import os
import subprocess
import sys
import datetime


def log(msg):
    print(f"[transcrever-audio] {msg}", file=sys.stderr)


def convert_to_wav(input_path, output_path):
    """Convert audio to 16kHz mono WAV using FFmpeg."""
    log(f"Converting {input_path} to WAV...")
    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        "-sample_fmt", "s16",
        output_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        log(f"FFmpeg error: {result.stderr}")
        return False
    return True


def try_ollama_whisper(wav_path):
    """Try transcription using Ollama with whisper model."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True, text=True, timeout=10
        )
        if "whisper" not in result.stdout.lower():
            return None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None

    log("Trying Ollama whisper...")
    try:
        result = subprocess.run(
            ["ollama", "run", "whisper", wav_path],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def try_vosk(wav_path):
    """Try transcription using Vosk (offline, lightweight, works on Termux)."""
    try:
        import vosk
        import wave
        import json
    except ImportError:
        return None

    log("Trying Vosk...")
    try:
        model_path = os.path.join(os.path.dirname(__file__), "vosk-model-small-pt")
        if not os.path.exists(model_path):
            model_path = os.path.join(os.path.dirname(__file__), "vosk-model-small-en-us")
        if not os.path.exists(model_path):
            log("No Vosk model found. Place vosk-model-small-pt or vosk-model-small-en-us in agent directory.")
            return None

        wf = wave.open(wav_path, "rb")
        model = vosk.Model(model_path)
        recognizer = vosk.KaldiRecognizer(model, wf.getframerate())

        text = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if "text" in result and result["text"]:
                    text.append(result["text"])

        final = json.loads(recognizer.FinalResult())
        if "text" in final and final["text"]:
            text.append(final["text"])

        wf.close()
        return " ".join(text).strip()
    except Exception as e:
        log(f"Vosk error: {e}")
        return None


def save_transcription(audio_filename, text, output_dir):
    """Save transcription to acervo/transcricoes/ directory."""
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(audio_filename)[0]
    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in base_name)
    output_path = os.path.join(output_dir, f"{safe_name}_{timestamp}.txt")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    log(f"Saved transcription to {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files to text")
    parser.add_argument("audio_file", help="Path to audio file (OGG/OPUS/MP3/WAV)")
    parser.add_argument("--output-dir", default=None, help="Output directory for transcriptions")
    args = parser.parse_args()

    audio_file = args.audio_file
    if not os.path.exists(audio_file):
        log(f"Error: File not found: {audio_file}")
        sys.exit(1)

    output_dir = args.output_dir or os.path.join(os.path.dirname(__file__), "acervo", "transcricoes")

    temp_wav = os.path.join(os.path.dirname(__file__), "temp_converted.wav")
    ext = os.path.splitext(audio_file)[1].lower()

    if ext == ".wav":
        wav_path = audio_file
    else:
        if not convert_to_wav(audio_file, temp_wav):
            log("Error: Failed to convert audio")
            sys.exit(1)
        wav_path = temp_wav

    transcription = None

    transcription = try_ollama_whisper(wav_path)

    if not transcription:
        transcription = try_vosk(wav_path)

    if not transcription:
        log("No transcription engine available.")
        log("Options:")
        log("  1. Install Ollama + whisper model: ollama pull whisper")
        log("  2. Install Vosk: pip install vosk")
        log("     Download model: https://alphacephei.com/vosk/models")
        log("     Place model in agent directory as vosk-model-small-pt")
        log("Saving audio for manual transcription.")
        save_transcription(
            os.path.basename(audio_file),
            "[PENDENTE - Transcricao manual necessaria]",
            output_dir
        )
        sys.exit(1)

    if ext != ".wav" and os.path.exists(temp_wav):
        os.remove(temp_wav)

    output_path = save_transcription(os.path.basename(audio_file), transcription, output_dir)
    print(transcription)


if __name__ == "__main__":
    main()
