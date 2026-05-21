#!/usr/bin/env python3
"""Corta Silencio - Agente de corte de silencios via FFmpeg.

Alternativa leve e mobile-friendly ao Narvi. Usa apenas o filtro
silencedetect do FFmpeg (sem Whisper, sem bibliotecas de audio).

Funciona em PC e Termux (Android).

Uso:
    python main.py video.mp4
    python main.py video.mp4 --threshold -25 --min-duration 1.0
    python main.py video.mp4 --keep-silence 0.3
"""

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

AGENT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = AGENT_DIR / "output" / "corta-silencio"

FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"

DEFAULT_THRESHOLD_DB = -30
DEFAULT_MIN_DURATION = 0.5
DEFAULT_KEEP_SILENCE = 0.0


def check_ffmpeg() -> None:
    """Verifica se o FFmpeg esta disponivel."""
    try:
        subprocess.run(
            [FFMPEG, "-version"],
            capture_output=True,
            timeout=10,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        print("[ERRO] FFmpeg nao encontrado. Instale antes de usar.")
        print("  PC:      choco install ffmpeg  (ou baixe de ffmpeg.org)")
        print("  Termux:  pkg install ffmpeg")
        raise SystemExit(1)


def get_video_duration(video_path: Path) -> float:
    """Retorna a duracao do video em segundos via ffprobe."""
    result = subprocess.run(
        [
            FFPROBE, "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    return float(result.stdout.strip())


def detect_silences(
    video_path: Path,
    threshold_db: float = DEFAULT_THRESHOLD_DB,
    min_duration: float = DEFAULT_MIN_DURATION,
) -> list[dict]:
    """Detecta silencios usando o filtro silencedetect do FFmpeg.

    Retorna lista de dicionarios com:
        {"start": float, "end": float}
    """
    print(f"[1/3] Detectando silencios (threshold={threshold_db}dB, min={min_duration}s)...")

    cmd = [
        FFMPEG, "-y",
        "-i", str(video_path),
        "-af", f"silencedetect=noise={threshold_db}dB:d={min_duration}",
        "-f", "null",
        "-",
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=300,
    )

    stderr = result.stderr

    silences = []
    silence_start = None

    for line in stderr.split("\n"):
        match_start = re.search(r"silence_start:\s*([\d.e+-]+)", line)
        match_end = re.search(r"silence_end:\s*([\d.e+-]+)\s*\|", line)

        if match_start:
            silence_start = float(match_start.group(1))

        if match_end and silence_start is not None:
            silence_end = float(match_end.group(1))
            silences.append({
                "start": silence_start,
                "end": silence_end,
            })
            silence_start = None

    print(f"      {len(silences)} silencios encontrados")
    return silences


def build_segments(
    duration: float,
    silences: list[dict],
    keep_silence: float = DEFAULT_KEEP_SILENCE,
) -> list[tuple[float, float]]:
    """Constroi lista de segmentos nao-silenciosos.

    keep_silence: segundos de silencio para manter em cada corte
                  (evita cortes bruscos, deixa transicao natural)
    """
    segments = []
    current_pos = 0.0

    for silence in silences:
        seg_start = current_pos
        seg_end = silence["start"] + keep_silence

        if seg_end > seg_start:
            segments.append((seg_start, seg_end))

        current_pos = silence["end"] - keep_silence

    segmento_final = (current_pos, duration)
    if segmento_final[1] > segmento_final[0]:
        segments.append(segmento_final)

    print(f"      {len(segments)} segmentos para concatenar")
    return segments


def concat_segments(
    video_path: Path,
    segments: list[tuple[float, float]],
    output_path: Path,
) -> None:
    """Concatena segmentos usando o demuxer concat do FFmpeg."""
    temp_dir = output_path.parent / ".temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

    print(f"[2/3] Cortando {len(segments)} segmentos...")

    segment_files = []

    for i, (start, end) in enumerate(segments):
        seg_output = temp_dir / f"seg_{i:04d}.mp4"
        duration = end - start

        cmd = [
            FFMPEG, "-y",
            "-ss", str(start),
            "-t", str(duration),
            "-i", str(video_path),
            "-c", "copy",
            "-avoid_negative_ts", "make_zero",
            str(seg_output),
        ]

        subprocess.run(cmd, capture_output=True, check=True)
        segment_files.append(seg_output)
        print(f"      Segmento {i+1}/{len(segments)}: {start:.1f}s - {end:.1f}s")

    print(f"[3/3] Concatenando segmentos...")

    concat_file = temp_dir / "concat_list.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for seg in segment_files:
            f.write(f"file '{seg}'\n")

    cmd = [
        FFMPEG, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(output_path),
    ]

    subprocess.run(cmd, capture_output=True, check=True)

    for seg in segment_files:
        seg.unlink(missing_ok=True)
    concat_file.unlink(missing_ok=True)
    temp_dir.rmdir()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Corta Silencio - Remove silencios de videos usando FFmpeg",
    )
    parser.add_argument(
        "video",
        type=str,
        help="Caminho do video de entrada",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD_DB,
        help=f"Threshold de silencio em dB (padrao: {DEFAULT_THRESHOLD_DB})",
    )
    parser.add_argument(
        "--min-duration",
        type=float,
        default=DEFAULT_MIN_DURATION,
        help=f"Duracao minima de silencio em segundos (padrao: {DEFAULT_MIN_DURATION})",
    )
    parser.add_argument(
        "--keep-silence",
        type=float,
        default=DEFAULT_KEEP_SILENCE,
        help="Segundos de silencio para manter nos cortes (padrao: 0)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Caminho do arquivo de saida (padrao: output/corta-silencio/<nome>_sem_silencio.mp4)",
    )

    args = parser.parse_args()

    t0 = time.time()

    video_path = Path(args.video).expanduser().resolve()
    if not video_path.exists():
        print(f"[ERRO] Arquivo nao encontrado: {video_path}")
        return 1

    check_ffmpeg()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
    else:
        stem = video_path.stem
        ext = video_path.suffix
        output_path = OUTPUT_DIR / f"{stem}_sem_silencio{ext}"

    print(f"\n[Corta Silencio]")
    print(f"  Entrada: {video_path.name}")
    print(f"  Saida:   {output_path.name}")
    print()

    try:
        duration = get_video_duration(video_path)
        print(f"      Duracao: {duration:.1f}s")

        silences = detect_silences(
            video_path,
            threshold_db=args.threshold,
            min_duration=args.min_duration,
        )

        if not silences:
            print("\n[OK] Nenhum silencio detectado. Video ja esta limpo.")
            return 0

        segments = build_segments(
            duration,
            silences,
            keep_silence=args.keep_silence,
        )

        if len(segments) <= 1:
            print("\n[OK] Video praticamente sem silencios para cortar.")
            return 0

        concat_segments(video_path, segments, output_path)

        elapsed = time.time() - t0
        output_size = output_path.stat().st_size / 1_000_000
        output_duration = get_video_duration(output_path)

        print(f"\n[OK] Concluido em {elapsed:.1f}s")
        print(f"   -> {output_path.name} ({output_size:.1f} MB)")
        print(f"   -> Duracao: {output_duration:.1f}s (original: {duration:.1f}s)")
        print(f"   -> Tempo removido: {duration - output_duration:.1f}s")

        return 0

    except subprocess.CalledProcessError as e:
        print(f"\n[ERRO] FFmpeg falhou: {e}")
        return 1
    except Exception as e:
        print(f"\n[ERRO] {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
