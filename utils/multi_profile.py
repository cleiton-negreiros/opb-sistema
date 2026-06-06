"""
utils/multi_profile.py — Helper compartilhado para suporte a multi-perfil.

Lê e expõe o perfil ativo do sistema (perfis/perfis.json) sem depender
do api_server. Funciona DENTRO de subprocess (agentes), standalone (CLI),
e em qualquer cwd (usa Path(__file__) para resolver a raiz do projeto).

Convenção de resolução do profile_id (em ordem):
    1. Argumento explícito passado pelo caller
    2. Env var OPB_PROFILE_ID (injetada pelo api_server antes do subprocess)
    3. perfis/perfis.json → campo "ativo"
    4. Fallback: "paz-na-conta"

Uso:
    from utils.multi_profile import resolve_profile_id, get_active_profile_id

    pid = resolve_profile_id()              # resolve pelo critério acima
    pid = resolve_profile_id("toque-de-paz") # explícito vence

    # Em CLI (extrai --perfil <id> do sys.argv):
    from utils.multi_profile import parse_perfil_arg
    profile_id, remaining = parse_perfil_arg(sys.argv[1:])
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional


PROJECT_PATH = Path(__file__).parent.parent.resolve()
PERFIS_PATH = PROJECT_PATH / "perfis"
PERFIS_CONFIG = PERFIS_PATH / "perfis.json"
DEFAULT_PROFILE_ID = "paz-na-conta"
ENV_VAR = "OPB_PROFILE_ID"


# ============================================================
# CORE
# ============================================================

def _read_perfis_config() -> dict:
    """Lê perfis.json bruto. Retorna {} se não existir ou inválido."""
    if not PERFIS_CONFIG.exists():
        return {}
    try:
        return json.loads(PERFIS_CONFIG.read_text(encoding="utf-8"))
    except Exception:
        return {}


def get_active_profile_id() -> str:
    """Retorna o id do perfil ativo em perfis.json. Default: paz-na-conta."""
    cfg = _read_perfis_config()
    ativo = cfg.get("ativo")
    if ativo and isinstance(ativo, str):
        return ativo
    return DEFAULT_PROFILE_ID


def list_profiles() -> list[dict]:
    """Retorna a lista de perfis declarados em perfis.json."""
    cfg = _read_perfis_config()
    perfis = cfg.get("perfis", [])
    return perfis if isinstance(perfis, list) else []


def get_profile_config(profile_id: Optional[str] = None) -> Optional[dict]:
    """Retorna o config.json do perfil (se existir)."""
    pid = profile_id or get_active_profile_id()
    config_path = PERFIS_PATH / pid / "perfil" / "config.json"
    if not config_path.exists():
        return None
    try:
        return json.loads(config_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def resolve_profile_id(arg: Optional[str] = None) -> str:
    """Resolve o profile_id pelo critério: arg > env > ativo > default.

    Args:
        arg: id explícito passado pelo caller (vence).

    Returns:
        id do perfil a ser usado.
    """
    if arg and isinstance(arg, str) and arg.strip():
        return arg.strip()

    env_val = os.environ.get(ENV_VAR, "").strip()
    if env_val:
        return env_val

    return get_active_profile_id()


# ============================================================
# PATHS POR PERFIL
# ============================================================

def get_profile_path(profile_id: Optional[str] = None, subdir: Optional[str] = None) -> Path:
    """Retorna o path base do perfil (perfis/<id>[/<subdir>])."""
    pid = resolve_profile_id(profile_id)
    base = PERFIS_PATH / pid
    if subdir:
        base = base / subdir
    return base


def get_acervo_path(profile_id: Optional[str] = None) -> Path:
    return get_profile_path(profile_id, "acervo")


def get_cerebro_path(profile_id: Optional[str] = None) -> Path:
    return get_profile_path(profile_id, "cerebro")


def get_output_path(profile_id: Optional[str] = None) -> Path:
    return get_profile_path(profile_id, "output")


def get_perfil_path(profile_id: Optional[str] = None) -> Path:
    return get_profile_path(profile_id, "perfil")


def get_profile_paths(profile_id: Optional[str] = None) -> dict:
    """Retorna dict com os paths principais do perfil resolvido."""
    pid = resolve_profile_id(profile_id)
    return {
        "id": pid,
        "raiz": PERFIS_PATH / pid,
        "perfil": get_perfil_path(pid),
        "cerebro": get_cerebro_path(pid),
        "acervo": get_acervo_path(pid),
        "output": get_output_path(pid),
    }


# ============================================================
# CLI HELPER
# ============================================================

def parse_perfil_arg(args: list[str]) -> tuple[Optional[str], list[str]]:
    """Extrai `--perfil <id>` ou `--perfil=<id>` da lista de args.

    Suporta tanto espaço quanto `=`. Aceita `-p` como atalho.

    Returns:
        (profile_id, remaining_args). profile_id é None se não veio.
    """
    remaining = []
    pid: Optional[str] = None
    skip_next = False

    for i, arg in enumerate(args):
        if skip_next:
            skip_next = False
            continue
        if arg in ("--perfil", "-p") and i + 1 < len(args):
            pid = args[i + 1]
            skip_next = True
            continue
        if arg.startswith("--perfil="):
            pid = arg.split("=", 1)[1]
            continue
        if arg.startswith("-p=") and len(arg) > 3:
            pid = arg.split("=", 1)[1]
            continue
        remaining.append(arg)

    return (pid.strip() if pid else None), remaining


# ============================================================
# BOOTSTRAP DO AMBIENTE
# ============================================================

def set_active_profile_env(profile_id: str) -> None:
    """Seta a env var OPB_PROFILE_ID. Usado pelo api_server antes de
    chamar subprocessos, para que os agentes herdem o perfil ativo
    sem precisar reescrever a CLI de cada um."""
    os.environ[ENV_VAR] = profile_id


# ============================================================
# CLI STANDALONE
# ============================================================

def _cli_main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        print("\nComandos disponíveis:")
        print("  ativo              → mostra o id do perfil ativo")
        print("  listar             → lista todos os perfis cadastrados")
        print("  paths [perfil_id]  → mostra os paths de um perfil")
        print("  resolve [perfil_id]→ resolve qual id seria usado (arg > env > ativo)")
        return

    cmd = sys.argv[1]
    if cmd == "ativo":
        print(f"Perfil ativo: {get_active_profile_id()}")
    elif cmd == "listar":
        perfis = list_profiles()
        if not perfis:
            print("(nenhum perfil cadastrado em perfis/perfis.json)")
        else:
            for p in perfis:
                marca = " ← ativo" if p.get("id") == get_active_profile_id() else ""
                print(f"  {p.get('id', '?')}{marca}  —  {p.get('nome', '?')}")
    elif cmd == "paths":
        pid = sys.argv[2] if len(sys.argv) > 2 else None
        paths = get_profile_paths(pid)
        for k, v in paths.items():
            print(f"  {k}: {v}")
    elif cmd == "resolve":
        arg = sys.argv[2] if len(sys.argv) > 2 else None
        print(f"Resolvido: {resolve_profile_id(arg)}")
    else:
        print(f"Comando desconhecido: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    _cli_main()
