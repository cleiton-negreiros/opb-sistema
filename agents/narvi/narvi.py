#!/usr/bin/env python3
"""narvi.py — Editor de vídeo CLI one-shot.

Versão pública distribuída para alunos OPB School via `opb-school/agente-narvi`.
Roda cross-platform: Mac (Apple Silicon e Intel) + Windows (com/sem GPU NVIDIA).

Fluxo: argv[1] (vídeo) → Whisper word-level (com cache) → trim dinâmico
→ ASS subtitle phrase-level → 2 ffmpegs paralelos (9x16 + 16x9, HEVC) →
output em ~/Desktop/narvi-saida/<stem>/.

Encoder auto-detect (runtime via `ffmpeg -encoders`):
  - Mac com VideoToolbox → hevc_videotoolbox
  - PC com GPU NVIDIA → hevc_nvenc
  - Fallback CPU → libx265

Whisper dual-path:
  - Mac Apple Silicon (ARM) → mlx-whisper (GPU MLX, rápido)
  - Outras plataformas → faster-whisper (CUDA se disponível, senão CPU)

Uso: python3 narvi.py /caminho/para/video.mp4 [flags]
Veja `python3 narvi.py --help` para as flags disponíveis.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
import traceback
from pathlib import Path

import yaml

# ============================================================
# Detecção de plataforma — Whisper dual path (Mac ARM vs outros)
# ============================================================
IS_MAC_ARM = (platform.system() == "Darwin" and platform.machine() == "arm64")

# .env opcional — só se aluno criou o arquivo
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env", verbose=False)
except ImportError:
    pass  # python-dotenv não é obrigatório; aluno pode usar variáveis de ambiente direto

# Imports locais (pipeline está no mesmo repo)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline.glossario import aplicar_glossario, carregar_glossario
from pipeline.hasher import hash_sha256  # noqa: F401  (reservado pra uso futuro)


# ============================================================
# Helpers locais (transcrição + impressão de status)
# ============================================================
def transcrever_com_word_timestamps(video_path: Path) -> list[dict]:
    """Transcrição word-level via Whisper. Dual path:

    - Mac Apple Silicon (ARM): mlx-whisper (GPU MLX, preserva velocidade Phase 19)
    - Outras plataformas (Mac Intel, Windows, Linux): faster-whisper
      (CUDA float16 se disponível, senão CPU int8)
    """
    if IS_MAC_ARM:
        return _transcrever_mlx(video_path)
    return _transcrever_faster(video_path)


def _transcrever_mlx(video_path: Path) -> list[dict]:
    """Mac ARM: mlx-whisper roda na GPU MLX da Apple."""
    import mlx_whisper  # import lazy: só carrega se Mac ARM

    lang = os.environ.get("WHISPER_LANGUAGE", "pt")
    result = mlx_whisper.transcribe(
        str(video_path),
        path_or_hf_repo="mlx-community/whisper-large-v3-mlx",
        word_timestamps=True,
        language=lang,
    )
    words = []
    for seg in result.get("segments", []):
        for w in seg.get("words", []):
            words.append({
                "text": w["word"],
                "startMs": int(w["start"] * 1000),
                "endMs": int(w["end"] * 1000),
            })
    return words


def _transcrever_faster(video_path: Path) -> list[dict]:
    """Outras plataformas: faster-whisper. Auto-detecta GPU NVIDIA via torch."""
    from faster_whisper import WhisperModel  # import lazy

    # Auto-detect GPU/CPU. torch é dependência transitiva de faster-whisper mas
    # nem toda instalação trás CUDA; defensivamente tratamos ImportError.
    try:
        import torch
        cuda_available = torch.cuda.is_available()
    except ImportError:
        cuda_available = False

    if cuda_available:
        device, compute_type = "cuda", "float16"
    else:
        device, compute_type = "cpu", "int8"

    lang = os.environ.get("WHISPER_LANGUAGE", "pt")
    model = WhisperModel("large-v3", device=device, compute_type=compute_type)
    segments, _ = model.transcribe(
        str(video_path),
        language=lang,
        word_timestamps=True,
        beam_size=5,
    )
    words = []
    for seg in segments:
        for w in (seg.words or []):
            words.append({
                "text": w.word,
                "startMs": int(w.start * 1000),
                "endMs": int(w.end * 1000),
            })
    return words


def alertar_erro(agent: str, titulo: str, detalhe: str = "") -> None:
    """Print de erro em stderr."""
    print(f"[ERRO] {titulo}: {detalhe}", file=sys.stderr)


def alertar_sucesso(agent: str, mensagem: str) -> None:
    """Print de sucesso em stdout."""
    print(f"[OK] {mensagem}")


# ============================================================
# Constantes
# ============================================================
AGENT_NAME = "narvi"
NARVI_DIR = Path(__file__).resolve().parent
GLOSSARIO_YAML = NARVI_DIR / "glossario.yaml"
CACHE_DIR = NARVI_DIR / "cache" / "whisper"
FFMPEG = "ffmpeg"
DEFAULT_OUTPUT_BASE = Path.home() / "Desktop" / "narvi-saida"


# ============================================================
# Detecção runtime do encoder HEVC disponível
# ============================================================
def detectar_encoder_video() -> tuple[str, str]:
    """Detecta melhor encoder HEVC disponível no ffmpeg local.

    Ordem de preferência:
      1. hevc_videotoolbox (Mac) — GPU da Apple, qualidade Phase 19
      2. hevc_nvenc (NVIDIA) — GPU NVIDIA em PC com CUDA
      3. libx265 (CPU) — fallback universal, qualquer plataforma

    Retorna (encoder_name, kind) onde kind ∈ {videotoolbox, nvenc, software}.
    """
    try:
        out = subprocess.run(
            [FFMPEG, "-hide_banner", "-encoders"],
            capture_output=True, text=True, timeout=10,
        ).stdout
    except Exception:
        return ("libx265", "software")  # fallback safe se ffmpeg quebrar
    if "hevc_videotoolbox" in out:
        return ("hevc_videotoolbox", "videotoolbox")
    if "hevc_nvenc" in out:
        return ("hevc_nvenc", "nvenc")
    if "libx265" in out:
        return ("libx265", "software")
    return ("libx265", "software")


ENCODER, ENCODER_KIND = detectar_encoder_video()

# Presets de corte (D-04 + D-05) — em ms.
# Valores negativos sao clampados a zero antes de aplicar.
CORTE_PRESETS = {
    "brando":    {"lead": 300, "tail": 500},
    "medio":     {"lead": 150, "tail": 300},
    "agressivo": {"lead":  80, "tail": 150},
}

SENTENCE_END = re.compile(r"[.!?…]\s*$")
SOFT_BREAK = re.compile(r"[,;:]\s*$")


# ============================================================
# CLI parser — 8 flags do D-05
# ============================================================
def parse_args(argv):
    p = argparse.ArgumentParser(prog="narvi", description="Narvi — editor de vídeo one-shot")
    p.add_argument("source", type=Path, help="Caminho do video de origem (.mp4/.mov)")
    p.add_argument("--corte", choices=["brando", "medio", "agressivo"], default="medio")
    p.add_argument("--sem-trim", action="store_true", help="Desliga trim dinamico (lead=tail=0)")
    p.add_argument("--trim-lead", type=int, default=None, help="Override lead em ms (D-04)")
    p.add_argument("--trim-tail", type=int, default=None, help="Override tail em ms (D-04)")
    p.add_argument("--ratio", choices=["9x16", "16x9", "both"], default="both")
    p.add_argument("--cta", type=str, default=None, help="Texto CTA (stub — Phase futura)")
    p.add_argument("--sample", action="store_true", help="Processa so primeiros 15s")
    p.add_argument("--output-dir", type=Path, default=None, help="Override pasta saida")
    return p.parse_args(argv)


def resolver_trim_ms(args) -> tuple[int, int]:
    """Resolve lead/tail ms aplicando overrides e clampando negativos a 0."""
    if args.sem_trim:
        return 0, 0
    preset = CORTE_PRESETS[args.corte]
    lead = args.trim_lead if args.trim_lead is not None else preset["lead"]
    tail = args.trim_tail if args.trim_tail is not None else preset["tail"]
    return max(0, int(lead)), max(0, int(tail))


# ============================================================
# Whisper + cache
# ============================================================
def transcrever_com_cache(src: Path) -> tuple[str, list[dict]]:
    """Retorna (hash16, words). Reusa cache em cache/whisper/."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    src_hash = hashlib.sha256(src.read_bytes()[:4_000_000]).hexdigest()[:16]
    cache_path = CACHE_DIR / f"narvi_words_{src_hash}.json"
    if cache_path.exists():
        print(f"[1/4] Cache hit Whisper ({cache_path.name})")
        return src_hash, json.loads(cache_path.read_text())
    print(f"[1/4] Transcrevendo {src.name}...")
    t0 = time.time()
    words = transcrever_com_word_timestamps(src)
    cache_path.write_text(json.dumps(words))
    print(f"      {len(words)} palavras em {time.time()-t0:.1f}s | cached")
    return src_hash, words


# ============================================================
# Funcoes COPIADAS VERBATIM de dev/quickedit_ffmpeg.py
# ============================================================
def adjust_words(words, trim_start_ms, total_ms):
    out = []
    for w in words:
        start = w["startMs"] - trim_start_ms
        end = w["endMs"] - trim_start_ms
        if end <= 0:
            continue
        if start >= total_ms:
            break
        out.append({
            "text": w["text"],
            "startMs": max(0, start),
            "endMs": min(total_ms, end),
        })
    return out


def group_phrases(words, max_chars=60, max_ms=4500):
    phrases = []
    cur = []
    for w in words:
        cur.append(w)
        word_text = w["text"]
        if SENTENCE_END.search(word_text):
            phrases.append(cur)
            cur = []
            continue
        text = "".join(x["text"] for x in cur).strip()
        span = w["endMs"] - cur[0]["startMs"]
        if len(text) >= max_chars or span >= max_ms:
            split_at = None
            for i in range(len(cur) - 1, 0, -1):
                if SOFT_BREAK.search(cur[i]["text"]):
                    split_at = i + 1
                    break
            if split_at is not None and split_at < len(cur):
                phrases.append(cur[:split_at])
                cur = cur[split_at:]
            else:
                phrases.append(cur)
                cur = []
    if cur:
        phrases.append(cur)
    return phrases


def ms_to_ass(ms: int) -> str:
    h = ms // 3_600_000
    m = (ms // 60_000) % 60
    s = (ms // 1000) % 60
    cs = (ms % 1000) // 10
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def build_ass(phrases, play_w, play_h, fontsize, margin_v):
    header = f"""[Script Info]
Title: Narvi quickedit
ScriptType: v4.00+
PlayResX: {play_w}
PlayResY: {play_h}
Timer: 100.0000
ScaledBorderAndShadow: yes
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Avenir Next Heavy,{fontsize},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,8,0,8,80,80,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for i, phr in enumerate(phrases):
        text = "".join(w["text"] for w in phr).strip()
        if len(text) > 36:
            words_split = text.split()
            mid = len(words_split) // 2
            text = " ".join(words_split[:mid]) + r"\N" + " ".join(words_split[mid:])
        text = text.upper()
        start = ms_to_ass(phr[0]["startMs"])
        if i + 1 < len(phrases):
            end_ms = min(phr[-1]["endMs"] + 150, phrases[i + 1][0]["startMs"] - 1)
        else:
            end_ms = phr[-1]["endMs"] + 200
        end = ms_to_ass(end_ms)
        events.append(f"Dialogue: 0,{start},{end},Caption,,0,0,0,,{text}")
    return header + "\n".join(events) + "\n"


def ff_args(crop_filter: str, scale: str, ass_path: Path, src: Path,
            start_ts: float, end_ts: float, out_path: Path) -> list[str]:
    # Phase 19 hotfix (2026-05-11): qualidade real 4K + tone mapping HDR→SDR.
    # iPhone moderno grava em HDR HLG BT.2020. Sem tone mapping, players SDR
    # (Reels, Meta Ads, QuickTime sem HDR) reinterpretam primaries BT.2020 como
    # BT.709 e gamma HLG como 2.2, deslocando cores (avermelhado/saturado).
    #
    # Pipeline:
    #   1. zscale: linearize HLG (npl=100 nits SDR reference)
    #   2. tonemap=hable: HDR -> SDR (Reinhard/Hable preserva contraste)
    #   3. zscale: re-tag BT.709 SDR
    #   4. format=yuv420p: 8-bit pra libass (subtitle precisa)
    #   5. crop + scale + ass overlay
    #   6. format=yuv420p10le: re-eleva pra 10-bit antes do encode
    # Encoder: VideoToolbox HEVC Main10, 25 Mbps (vs 12M default antigo),
    # tags color BT.709 SDR explícitas pra player não adivinhar.
    # Source iPhone Pro é Dolby Vision Profile 8.4 (HDR HLG BT.2020 + RPU).
    # Sem libplacebo, tonemap ignora o RPU. Solução validada na Phase 19
    # (Elton aprovou 2026-05-11): tonemap=hable + desat=0 + tags BT.709 SDR.
    # - hable: preserva contraste/cor mais natural pra conteúdo iPhone
    # - desat=0: evita lavagem desnecessária (conteúdo já dentro do gamut SDR)
    # - npl=100: target SDR reference de 100 nits
    # - tags BT.709 SDR explícitas pra player não adivinhar primaries
    # Filter chain idêntico em todas as plataformas — o tone mapping HDR HLG → SDR
    # BT.709 funciona em qualquer encoder (é processamento via libavfilter, não GPU).
    vf = (
        f"zscale=t=linear:npl=100,"
        f"format=gbrpf32le,"
        f"zscale=p=bt709,"
        f"tonemap=tonemap=hable:desat=0,"
        f"zscale=t=bt709:m=bt709:r=tv,"
        f"format=yuv420p,"
        f"{crop_filter}scale={scale}:flags=lanczos,"
        f"ass={ass_path},"
        f"format=yuv420p10le"
    )

    # pix_fmt 10-bit difere entre HW (p010le) e SW (yuv420p10le).
    pix_fmt = "yuv420p10le" if ENCODER_KIND == "software" else "p010le"

    base = [
        FFMPEG, "-y",
        "-ss", f"{start_ts}", "-to", f"{end_ts}",
        "-i", str(src),
        "-vf", vf,
        "-pix_fmt", pix_fmt,
        "-c:v", ENCODER,
    ]

    if ENCODER_KIND == "videotoolbox":
        # Mac — qualidade Phase 19 validada (25 Mbps Main10).
        base += [
            "-profile:v", "main10",
            "-allow_sw", "1",
            "-b:v", "25M",
            "-tag:v", "hvc1",
        ]
    elif ENCODER_KIND == "nvenc":
        # NVIDIA — VBR balanced, target ~25 Mbps com headroom até 30.
        # preset p5 = balanced; p1=fastest, p7=slowest. p5 mantém qualidade próxima
        # do VideoToolbox sem virar gargalo.
        base += [
            "-profile:v", "main10",
            "-preset", "p5",
            "-rc", "vbr",
            "-b:v", "25M",
            "-maxrate", "30M",
            "-bufsize", "50M",
            "-tag:v", "hvc1",
        ]
    else:
        # libx265 (CPU) — CRF 22 ≈ 25 Mbps em 4K para conteúdo típico iPhone.
        # preset medium é o ponto razoável entre velocidade e qualidade no software.
        base += [
            "-preset", "medium",
            "-crf", "22",
            "-x265-params", "log-level=error",
            "-tag:v", "hvc1",
        ]

    base += [
        "-color_range", "tv",
        "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "192k",
        str(out_path),
    ]
    return base


# ============================================================
# Pipeline
# ============================================================
def main(argv=None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    print(f"[Narvi] Encoder: {ENCODER} ({ENCODER_KIND}) | Whisper: {'mlx' if IS_MAC_ARM else 'faster'}")
    src: Path = args.source.expanduser().resolve()
    if not src.exists():
        print(f"ERRO: arquivo nao existe: {src}", file=sys.stderr)
        return 2

    # D-07 — output canonical em ~/Desktop/narvi-saida/<stem>/
    out_base = (args.output_dir or DEFAULT_OUTPUT_BASE).expanduser().resolve()
    out_dir = out_base / src.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    lead_ms, tail_ms = resolver_trim_ms(args)
    t_inicio = time.time()

    try:
        # ============================================================
        # [1/4] Whisper + glossario
        # ============================================================
        src_hash, words = transcrever_com_cache(src)
        rules = carregar_glossario(GLOSSARIO_YAML)
        words = aplicar_glossario(words, rules)

        # ============================================================
        # Duracao bruta via ffprobe
        # ============================================================
        src_dur_ms = int(float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(src),
        ]).strip()) * 1000)

        # ============================================================
        # Trim dinamico (D-04 + D-05) ou --sem-trim
        # ============================================================
        if words:
            first_speech_ms = words[0]["startMs"]
            last_speech_ms = words[-1]["endMs"]
        else:
            first_speech_ms = 0
            last_speech_ms = src_dur_ms

        trim_start_ms = max(0, first_speech_ms - lead_ms)
        trim_end_from_src_end_ms = max(0, src_dur_ms - last_speech_ms - tail_ms)
        start_ts = trim_start_ms / 1000.0
        end_ts = float(src_dur_ms) / 1000 - trim_end_from_src_end_ms / 1000.0

        # --sample: limita a 15s a partir do start trimmed
        if args.sample:
            end_ts = min(end_ts, start_ts + 15.0)

        total_ms = int((end_ts - start_ts) * 1000)
        print(f"      trim start={start_ts:.2f}s end={end_ts:.2f}s "
              f"dur_final={total_ms/1000:.2f}s | lead={lead_ms}ms tail={tail_ms}ms")

        words_trim = adjust_words(words, trim_start_ms, total_ms)
        phrases = group_phrases(words_trim)
        print(f"[2/4] {len(phrases)} frases pra legendar")

        # ============================================================
        # ASS subtitles (9x16 top-aligned, 16x9 bottom-quarter)
        # ============================================================
        ass_v = Path("/tmp/narvi_cap_9x16.ass")
        ass_h = Path("/tmp/narvi_cap_16x9.ass")
        ass_v.write_text(build_ass(phrases, 2160, 3840, fontsize=120, margin_v=2530))
        ass_h.write_text(build_ass(phrases, 3840, 2160, fontsize=96, margin_v=1620))

        # ============================================================
        # [3/4] FFmpeg paralelos — respeitando --ratio
        # ============================================================
        stem = src.stem
        out_v = out_dir / f"{stem}-9x16.mp4"
        out_h = out_dir / f"{stem}-16x9.mp4"
        log_v = out_dir / "ffmpeg-9x16.log"
        log_h = out_dir / "ffmpeg-16x9.log"

        # 9:16 crop center 1215x2160 de 3840x2160, scale 2160x3840
        args_v = ff_args("crop=ih*9/16:ih,", "2160:3840", ass_v, src, start_ts, end_ts, out_v)
        # 16:9 sem crop, manter 4K
        args_h = ff_args("", "3840:2160", ass_h, src, start_ts, end_ts, out_h)

        gerar_v = args.ratio in ("9x16", "both")
        gerar_h = args.ratio in ("16x9", "both")

        print(f"[3/4] Disparando ffmpeg(s) em paralelo ({ENCODER}) — ratio={args.ratio}...")

        procs = []
        if gerar_v:
            procs.append(("9x16", out_v, log_v,
                         subprocess.Popen(args_v, stdout=open(log_v, "wb"), stderr=subprocess.STDOUT)))
        if gerar_h:
            procs.append(("16x9", out_h, log_h,
                         subprocess.Popen(args_h, stdout=open(log_h, "wb"), stderr=subprocess.STDOUT)))

        t1 = time.time()
        results = []
        for label, out_p, log_p, proc in procs:
            rc = proc.wait()
            results.append((label, out_p, log_p, rc))
        elapsed = time.time() - t1

        print(f"[4/4] " + " | ".join(f"{lbl} rc={rc}" for lbl, _, _, rc in results)
              + f" | {elapsed:.1f}s")

        outputs_gerados: list[Path] = []
        for label, out_p, log_p, rc in results:
            if rc != 0:
                raise RuntimeError(f"ffmpeg {label} falhou (rc={rc}). Log: {log_p}")
            outputs_gerados.append(out_p)

        duracao_final_s = total_ms / 1000.0

        print(f"\nPronto em {out_dir}")
        for p in outputs_gerados:
            print(f"  - {p.name} ({p.stat().st_size/1_000_000:.1f} MB)")

        alertar_sucesso(
            AGENT_NAME,
            f"{src.name} editado em {time.time()-t_inicio:.0f}s ({len(outputs_gerados)} mp4 em {out_dir})",
        )
        return 0

    except Exception as e:
        traceback.print_exc()
        alertar_erro(AGENT_NAME, f"Falhou editando {src.name}", str(e))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
