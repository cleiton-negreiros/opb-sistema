#!/usr/bin/env python3
"""Narvi - Editor de Vídeo para OPB Sistema"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import narvi

if __name__ == "__main__":
    raise SystemExit(narvi.main())