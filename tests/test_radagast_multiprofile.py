import sys, os
sys.path.insert(0, 'utils')
from multi_profile import resolve_profile_id, get_profile_config
from profile_loader import load_profile
sys.path.insert(0, 'agents/radagast')
from analyzer import build_system_prompt, _pilares_para, _carregar_contexto_perfil, PILARES_DEFAULT

print('PILARES_DEFAULT keys:', list(PILARES_DEFAULT.keys()))
for pid in ['paz-na-conta', 'toque-de-paz', 'caminho-vida']:
    p = load_profile(pid)
    pc = get_profile_config(pid)
    prompt = build_system_prompt(p, pc, pid)
    print()
    print('===', pid, '===')
    print('  nome:', (p.get('nome') or (pc or {}).get('nome') or ''))
    print('  publico:', repr((p.get('publico_alvo') or '')[:60]))
    print('  tom:', p.get('tom_de_voz', [])[:2])
    print('  pilares:', [x[0] for x in _pilares_para(pid)])
    print('  prompt len:', len(prompt), 'chars')
print()
print('OK')
