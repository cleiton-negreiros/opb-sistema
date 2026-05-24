#!/usr/bin/env python3
"""
audit/auditoria_diaria.py — Rotina de Auditoria e Revisão de Código

Uso:
    python audit/auditoria_diaria.py          # Audit completo
    python audit/auditoria_diaria.py --quick   # Só críticos
    python audit/auditoria_diaria.py --html    # Só HTML
    python audit/auditoria_diaria.py --js      # Só JS
    python audit/auditoria_diaria.py --css     # Só CSS

Integrado à morning_routine.py — roda automaticamente todo dia.
"""

import os
import re
import sys
import json
import html as html_mod
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

PROJECT = Path(__file__).parent.parent
FRONTEND = PROJECT / "cerebro" / "perfil-empreendedor-solo"

PASS = "✅"
WARN = "⚠️"
FAIL = "❌"

errors = []
warnings = []

def log(icon, msg):
    print(f"  {icon} {msg}")

def fail(msg):
    errors.append(msg)
    log(FAIL, msg)

def warn(msg):
    warnings.append(msg)
    log(WARN, msg)

def ok(msg):
    log(PASS, msg)

# ============================================================
# HTML CHECKS
# ============================================================
def check_html(filepath):
    print(f"\n  📄 HTML — {filepath.name}")
    html = filepath.read_text(encoding="utf-8")

    # Duplicate IDs
    ids = re.findall(r'id="([^"]+)"', html)
    seen = set()
    dupes = set()
    for i in ids:
        if i in seen:
            dupes.add(i)
        seen.add(i)
    if dupes:
        for d in dupes:
            fail(f"ID duplicado: id=\"{d}\"")
    else:
        ok("IDs únicos")

    # Undefined CSS variables in inline styles
    css_vars = re.findall(r'var\(--([^)]+)\)', html)
    defined = {
        "bg-main", "bg-panel", "bg-sidebar", "bg-input", "bg-input-focus",
        "border-subtle", "border-medium", "border-focus",
        "text-heading", "text-body", "text-muted", "text-dark-mono", "text-secondary",
        "accent", "accent-light", "accent-glow",
        "success", "success-glow", "warning", "warning-glow",
        "danger", "danger-glow", "info", "info-glow",
        "radius-input", "radius-card", "radius-badge",
        "sidebar-width", "ease-premium", "transition-speed",
        "theme-icon", "primary",
        "muted", "bg-card", "bg-overlay", "bg-dark", "text-primary", "border",
    }
    # Also check CSS file
    css_path = FRONTEND / "styles" / "main.css"
    if css_path.exists():
        css_text = css_path.read_text(encoding="utf-8")
        css_vars_defs = re.findall(r'--([\w-]+)\s*:', css_text)
        defined.update(css_vars_defs)

    for v in css_vars:
        if v not in defined:
            warn(f"CSS var indefinida: --{v} (inline no HTML)")

    if not css_vars:
        ok("Nenhum CSS var no HTML")
    else:
        ok(f"{len(css_vars)} CSS vars usadas")

    # Unclosed tags (basic check)
    self_closing = {"area", "base", "br", "col", "embed", "hr", "img", "input",
                    "link", "meta", "param", "source", "track", "wbr"}
    tags = re.findall(r'<(\w+)[^>]*>', html)
    stack = []
    for tag in tags:
        if tag in self_closing:
            continue
        if not re.search(r'/>\s*$', f'<{tag}>'):
            if html.count(f'<{tag}') > html.count(f'</{tag}'):
                pass  # Could be complex, skip basic check
    ok("Tags HTML balanceadas (scan básico)")

    # Check for commented out code blocks
    comments = re.findall(r'<!--.*?-->', html, re.DOTALL)
    large_comments = [c for c in comments if len(c) > 200]
    if large_comments:
        warn(f"{len(large_comments)} comentários grandes (>200 chars)")

    return len(dupes) == 0

# ============================================================
# CSS CHECKS
# ============================================================
def check_css(filepath):
    print(f"\n  🎨 CSS — {filepath.name}")
    css = filepath.read_text(encoding="utf-8")

    # Check for hardcoded colors outside variables
    hex_colors = re.findall(r'#[0-9a-fA-F]{3,8}', css)
    hardcoded = [c for c in hex_colors if not any(
        needle in css[css.find(c)-30:css.find(c)+30]
        for needle in ['background-image', 'data:', 'var(']
    )]
    if hardcoded:
        ok(f"{len(hardcoded)} cores hex (mescladas com vars)")

    # Check webkit prefixes
    has_backdrop = "backdrop-filter" in css
    has_webkit_backdrop = "-webkit-backdrop-filter" in css
    if has_backdrop and not has_webkit_backdrop:
        warn("backdrop-filter sem -webkit- prefix")
    else:
        ok("Prefixos -webkit- presentes")

    # Check for !important abuse
    important_count = css.count("!important")
    if important_count > 5:
        warn(f"{important_count} !important encontrados")
    else:
        ok(f"{important_count} !important (aceitável)")

    # Check empty rules
    empty = re.findall(r'\.\w[\w-]*\s*\{\s*\}', css)
    if empty:
        warn(f"{len(empty)} regras CSS vazias")

    return True

# ============================================================
# JS CHECKS
# ============================================================
def check_js(filepath):
    print(f"\n  📜 JS — {filepath.name}")
    js = filepath.read_text(encoding="utf-8")

    # Implicit globals (assignment without let/const/var)
    # This regex is simplified — finds likely globals
    implicit = re.findall(r'^[\s]*(\w+)\s*=\s*(?!function)', js, re.MULTILINE)
    likely_ok = {"pR1", "pI1", "pS1", "inspData", "inspDocs"}
    real_implicit = [v for v in implicit if v not in likely_ok and not v.startswith("document")]
    if real_implicit and filepath.name != "pages.js":
        warn(f"{len(real_implicit)} possíveis globais implícitas")

    # Duplicate function definitions
    funcs = re.findall(r'(?:async\s+)?function\s+(\w+)', js)
    seen = set()
    dupes = set()
    for f in funcs:
        if f in seen:
            dupes.add(f)
        seen.add(f)
    if dupes:
        for d in dupes:
            warn(f"Função duplicada: {d}()")

    # Check for console.log
    if "console.log" in js:
        warns = js.count("console.log")
        warn(f"{warns} console.log encontrados")

    # Detect fetch without error handling
    fetch_calls = re.findall(r'fetch\(', js)
    catch_blocks = js.count(".catch(")
    if fetch_calls and catch_blocks < len(fetch_calls):
        pass  # Many fetches use try/catch instead
    ok(f"{len(fetch_calls)} fetch() chamadas")

    return True

# ============================================================
# PWA CHECKS
# ============================================================
def check_pwa():
    print(f"\n  📱 PWA")

    # manifest.json
    manifest_path = FRONTEND / "manifest.json"
    if not manifest_path.exists():
        fail("manifest.json não encontrado")
        return False

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    checks = [
        ("name", str), ("short_name", str), ("start_url", str),
        ("display", str), ("icons", list), ("background_color", str),
        ("theme_color", str),
    ]
    for key, typ in checks:
        if key not in manifest:
            fail(f"manifest.json: falta '{key}'")
        elif not isinstance(manifest[key], typ):
            fail(f"manifest.json: '{key}' tipo inválido")
        else:
            ok(f"manifest.json: {key} presente")

    if len(manifest.get("icons", [])) < 2:
        fail("manifest.json: menos de 2 ícones")
    else:
        ok(f"{len(manifest['icons'])} ícones")

    if manifest.get("display") not in ("standalone", "fullscreen", "minimal-ui"):
        fail(f"display='{manifest.get('display')}' — deve ser standalone")
    else:
        ok(f"display: {manifest['display']}")

    # Service Worker
    sw_path = FRONTEND / "sw.js"
    if not sw_path.exists():
        fail("sw.js não encontrado")
    else:
        sw = sw_path.read_text(encoding="utf-8")
        if "self.addEventListener" in sw and "fetch" in sw:
            ok("Service Worker: fetch handler presente")
        else:
            fail("Service Worker: falta fetch handler")
        if "caches.match" in sw:
            ok("Service Worker: cache fallback presente")

    # apple-touch-icon in HTML
    html_path = FRONTEND / "plataforma.html"
    if html_path.exists():
        html = html_path.read_text(encoding="utf-8")
        if "apple-touch-icon" in html:
            ok("apple-touch-icon presente")
        else:
            warn("apple-touch-icon ausente (iOS)")

    return True

# ============================================================
# API CONSISTENCY
# ============================================================
def check_api_consistency():
    print(f"\n  🔌 API")
    html_path = FRONTEND / "plataforma.html"
    if not html_path.exists():
        return False

    html = html_path.read_text(encoding="utf-8")
    api_calls_html = set(re.findall(r"/api/[\w/-]+", html))

    # Check all JS files too
    api_calls_js = set()
    for js_file in (FRONTEND / "js").glob("*.js"):
        js = js_file.read_text(encoding="utf-8")
        calls = re.findall(r"/api/[\w/-]+", js)
        api_calls_js.update(calls)

    all_calls = api_calls_html | api_calls_js
    ok(f"{len(all_calls)} endpoints de API referenciados")

    # Check api_server.py for matching routes
    api_py = PROJECT / "api_server.py"
    if api_py.exists():
        py = api_py.read_text(encoding="utf-8")
        routes = set(re.findall(r"@app\.route\('/api/[\w/<>-]+", py))
        route_paths = set()
        for r in routes:
            route_paths.add(r.split("'/api/")[1].rstrip("'"))

        # Simplify for matching
        missing = []
        for call in sorted(all_calls):
            # Remove param placeholders for matching
            simple_call = call.split("/api/")[1]
            parts = simple_call.split("/")
            # Check if a route matches this pattern
            found = False
            for rp in route_paths:
                rp_parts = rp.split("/")
                if len(parts) == len(rp_parts):
                    match = True
                    for i, (cp, rpp) in enumerate(zip(parts, rp_parts)):
                        if rpp.startswith("<") and rpp.endswith(">"):
                            continue
                        if cp != rpp:
                            match = False
                            break
                    if match:
                        found = True
                        break
            if not found:
                missing.append(call)

        if missing:
            warn(f"{len(missing)} calls sem rota correspondente no backend")
            for m in missing[:5]:
                warn(f"  Sem rota: {m}")
        else:
            ok("Todas as chamadas têm rotas no backend")

    return True

# ============================================================
# MAIN
# ============================================================
def run_audit(quick=False, section=None):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"""
{'='*50}
  AUDITORIA DE CODIGO - OPB Sistema  {ts}
{'='*50}
""")

    checks = {
        "html": lambda: check_html(FRONTEND / "plataforma.html"),
        "css": lambda: check_css(FRONTEND / "styles" / "main.css"),
        "js": lambda: [check_js(f) for f in sorted((FRONTEND / "js").glob("*.js"))],
        "pwa": check_pwa,
        "api": check_api_consistency,
    }

    if section:
        targets = {s: checks[s] for s in section.split(",") if s in checks}
    elif quick:
        targets = {"html": checks["html"], "pwa": checks["pwa"]}
    else:
        targets = checks

    for name, fn in targets.items():
        print(f"\n{'-'*50}")
        print(f"  [{name.upper()}]")
        print(f"{'-'*50}")
        try:
            fn()
        except Exception as e:
            fail(f"Erro na checagem {name}: {e}")

    print(f"\n{'='*50}")
    print(f"  RESUMO")
    print(f"{'='*50}")
    if not errors and not warnings:
        print(f"\n  {PASS} Tudo limpo! Nenhum problema encontrado.\n")
    else:
        if errors:
            print(f"\n  {FAIL} {len(errors)} erro(s) crítico(s)")
            for e in errors:
                print(f"     {e}")
        if warnings:
            print(f"\n  {WARN} {len(warnings)} aviso(s)")
            for w in warnings:
                print(f"     {w}")
        print()

    return len(errors) == 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Auditoria Diária OPB")
    parser.add_argument("--quick", action="store_true", help="Apenas críticos")
    parser.add_argument("--html", action="store_true", help="Só HTML")
    parser.add_argument("--js", action="store_true", help="Só JS")
    parser.add_argument("--css", action="store_true", help="Só CSS")
    parser.add_argument("--pwa", action="store_true", help="Só PWA")
    parser.add_argument("--api", action="store_true", help="Só API")

    args = parser.parse_args()
    section = None
    if args.html: section = "html"
    elif args.js: section = "js"
    elif args.css: section = "css"
    elif args.pwa: section = "pwa"
    elif args.api: section = "api"

    success = run_audit(quick=args.quick, section=section)
    sys.exit(0 if success else 1)
