#!/usr/bin/env python3
"""main.py — Entry point do Audio Transcriber Agent.

Uso:
    python agents/audio_transcriber/main.py <caminho_do_audio>
    python agents/audio_transcriber/main.py <caminho_do_audio> --usuario "Nome"
    python agents/audio_transcriber/main.py --check
    python agents/audio_transcriber/main.py --status
"""

import argparse
import json
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="[audio-transcriber] %(levelname)s %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("audio_transcriber")

PROJECT_PATH = Path(__file__).parent.parent.parent


def run_check():
    """Verifica dependencias do ambiente."""
    issues = []

    # FFmpeg
    import shutil
    if shutil.which("ffmpeg"):
        logger.info("ffmpeg: OK")
    else:
        issues.append("FFmpeg nao encontrado (necessario para converter audio)")

    # Ollama whisper
    import subprocess
    try:
        r = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        if "whisper" in r.stdout.lower():
            logger.info("Ollama whisper: OK")
        else:
            issues.append("Ollama whisper nao encontrado (execute: ollama pull whisper)")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        issues.append("Ollama nao encontrado (opcional se tiver Vosk)")

    # Vosk
    try:
        import vosk
        logger.info("Vosk: OK")
    except ImportError:
        issues.append("Vosk nao instalado (opcional, pip install vosk)")

    # Diretorios
    for d in ["acervo/ideias", "acervo/transcricoes", "acervo/temp"]:
        p = PROJECT_PATH / d
        p.mkdir(parents=True, exist_ok=True)
        logger.info(f"Diretorio {d}: OK")

    if issues:
        logger.warning("Issues encontrados:")
        for i in issues:
            logger.warning(f"  - {i}")
        return False
    logger.info("Todos os checks OK!")
    return True


def run_status():
    """Exibe estado atual do agente."""
    state_path = Path(__file__).parent / ".state.json"
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        print(json.dumps(state, indent=2, ensure_ascii=False))
    else:
        print("Nenhum estado encontrado. Ainda nao foram processados audios.")


def main():
    parser = argparse.ArgumentParser(description="Audio Transcriber Agent - Transcreve audio e salva como ideia")
    parser.add_argument("audio_file", nargs="?", help="Caminho do arquivo de audio (OGG/OPUS/MP3/WAV)")
    parser.add_argument("--usuario", default="audio_transcriber", help="Nome do usuario (para metadados)")
    parser.add_argument("--check", action="store_true", help="Verifica dependencias")
    parser.add_argument("--status", action="store_true", help="Mostra estado do agente")
    parser.add_argument("--json", action="store_true", help="Saida em JSON (para integracoes)")

    args = parser.parse_args()

    if args.check:
        ok = run_check()
        sys.exit(0 if ok else 1)

    if args.status:
        run_status()
        return

    if not args.audio_file:
        parser.print_help()
        sys.exit(1)

    from transcriber import transcrever

    resultado = transcrever(args.audio_file, args.usuario)

    if args.json:
        print(json.dumps(resultado, ensure_ascii=False))
    elif resultado.get("sucesso"):
        print(resultado["texto"])
        logger.info(f"Transcricao: {resultado['transcricao_path']}")
        logger.info(f"Ideia: {resultado['ideia_path']}")
    else:
        logger.error(resultado.get("erro", "Erro desconhecido"))
        print(f"❌ {resultado.get('erro', 'Erro desconhecido')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
