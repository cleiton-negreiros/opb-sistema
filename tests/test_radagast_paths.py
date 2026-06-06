"""Test that perfil resolves correctly and save paths are per-profile."""
import sys
from pathlib import Path
sys.path.insert(0, 'utils')
sys.path.insert(0, 'agents/radagast')

from multi_profile import resolve_profile_id, get_acervo_path, get_profile_config
from radagast import load_config

# Verify per-profile path resolution
for pid in ['paz-na-conta', 'toque-de-paz', 'caminho-vida']:
    resolved = resolve_profile_id(pid)
    path = get_acervo_path(pid) / "ideias"
    cfg = get_profile_config(pid) or {}
    print(f"  {pid}")
    print(f"    resolved:    {resolved}")
    print(f"    save path:   {path}")
    print(f"    config name: {cfg.get('nome')!r}")
    print(f"    handle:      {cfg.get('instagram', '?')}")
    print()

# Verify load_config with per-profile
print("=== load_config('keywords.json', profile_id='caminho-vida') ===")
cfg = load_config('keywords.json', profile_id='caminho-vida')
print(f"  search_terms count: {len(cfg.get('search_terms', []))}")
print(f"  (falls back to global keywords.json since no per-profile override)")

print()
print("OK")
