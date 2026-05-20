"""Hash SHA-256 chunked do arquivo bruto (D-F1)."""
from __future__ import annotations
import hashlib
from pathlib import Path

CHUNK_SIZE = 8 * 1024 * 1024  # 8 MiB


def hash_sha256(path: str | Path) -> str:
    """Calcula SHA-256 hex de arquivo via leitura chunked.

    Usado para idempotência: mesmo arquivo (mesmo conteúdo, qualquer nome)
    sempre retorna o mesmo hash. Inserir em narvi_jobs.hash_sha256 (UNIQUE).
    """
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()
