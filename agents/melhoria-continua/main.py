#!/usr/bin/env python3
"""
Agente de Melhoria Continua - OPB Sistema
Analisa o codigo e sugere melhorias por severidade.
"""
import os
import re
import sys
import io
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()

# Padrões de problemas conhecidos
PATTERNS = {
    "critical": [
        {
            "name": "apiCall args trocados",
            "pattern": r"apiCall\([^)]+\{[^}]+\},\s*['\"]POST['\"]",
            "file": "*.js",
            "fix": "Trocar ordem: apiCall(url, 'POST', body)"
        },
        {
            "name": "Path traversal",
            "pattern": r"PROJECT_PATH\s*/\s*caminho",
            "file": "*.py",
            "fix": "Adicionar validação: if '..' in caminho: return 400"
        },
        {
            "name": "DEBUG=True em produção",
            "pattern": r"DEBUG\s*=\s*True",
            "file": "*.py",
            "fix": "Alterar para DEBUG = False"
        },
        {
            "name": "XSS via onclick",
            "pattern": r"onclick=\"[^\"]*\$\{escapeHtml\([^)]+\)",
            "file": "*.js",
            "fix": "Usar escapeAttr() ou data-* attributes"
        },
    ],
    "high": [
        {
            "name": "JSON.parse sem try-catch",
            "pattern": r"JSON\.parse\((?!.*try)",
            "file": "*.js",
            "fix": "Envolver em try-catch"
        },
        {
            "name": "async sem await",
            "pattern": r"(?<!await\s)gerarCarrossel\(\)|(?<!await\s)runTextGenerator\(\)",
            "file": "*.js",
            "fix": "Adicionar await ou .catch()"
        },
        {
            "name": "clipboard sem catch",
            "pattern": r"navigator\.clipboard\.writeText\([^)]+\)(?!\s*\.catch)",
            "file": "*.js",
            "fix": "Adicionar .catch() com fallback"
        },
        {
            "name": "int() sem validação",
            "pattern": r"int\(request\.args\.get\(",
            "file": "*.py",
            "fix": "Envolver em try-except ValueError"
        },
    ],
    "medium": [
        {
            "name": "Sys.path em loop",
            "pattern": r"sys\.path\.insert\(",
            "file": "*.py",
            "fix": "Mover para início do arquivo"
        },
        {
            "name": "Glob sem sort por data",
            "pattern": r"sorted\([^.]*\.glob\([\"']\*\.md[\"']\)",
            "file": "*.py",
            "fix": "Usar key=lambda f: f.stat().st_mtime"
        },
        {
            "name": "Null check ausente",
            "pattern": r"getElementById\('[^']+'\)\.(?!classList|style|value|checked|textContent|innerHTML)",
            "file": "*.js",
            "fix": "Adicionar verificação null"
        },
    ],
    "low": [
        {
            "name": "Import redundante",
            "pattern": r"import\s+\w+\s+as\s+\w+.*#\s*already",
            "file": "*.py",
            "fix": "Remover import duplicado"
        },
        {
            "name": "Empty catch block",
            "pattern": r"}\s*catch\s*\{\s*\}",
            "file": "*.js",
            "fix": "Adicionar console.error() ou tratamento"
        },
        {
            "name": "Inline style excessivo",
            "pattern": r"style=\"[^\"]{50,}\"",
            "file": "*.html",
            "fix": "Mover para classe CSS"
        },
    ]
}

# Páginas sem handler no loadPageData
PAGES_WITHOUT_HANDLER = [
    "rotinas", "pipeline", "capa-video", "consumo", "text-generator",
    "narvi", "radagast", "consultor-negocios", "jornada-ia",
    "produtividade", "aprendizados"
]

# Melhorias sugeridas por área
SUGGESTIONS = {
    "carousel": [
        "Adicionar preview do carrossel antes de gerar (swipe nos slides)",
        "Botão 'Gerar Varições' - criar 3 versões do mesmo carrossel",
        "Timeline visual dos slides (arrastar para reordenar)",
        "Exportar como PNG individuais (cada slide = 1 imagem)",
        "Salvar como rascunho e continuar depois",
        "Histórico de carrosséis gerados com busca",
    ],
    "mobile": [
        "Swipe entre páginas (gesto de arrastar)",
        "Pull-to-refresh no dashboard",
        "Botão flutuante 'Gerar Conteúdo' sempre visível",
        "Bottom sheet para ações (em vez de modais)",
        "Haptic feedback ao salvar (vibração)",
        "Modo offline com cache de últimos resultados",
    ],
    "pipeline": [
        "Agendamento de pipeline (horário fixo diário)",
        "Notificação quando pipeline completa",
        "Fila de ideias (adicionar várias, processar em batch)",
        "Comparar versões (antes/depois de editar)",
        "Estatísticas de produção (posts/dia, carrosséis/semana)",
    ],
    "perfil": [
        "Quiz gamificado (barra de progresso animada)",
        "Dicas contextuais durante o preenchimento",
        "Preview do perfil (como outros veem)",
        "Importar dados do Instagram (bio, posts)",
        "Sugestões automáticas baseadas nas respostas",
    ],
}


def scan_file(filepath: Path) -> list:
    """Escaneia um arquivo e retorna problemas encontrados."""
    issues = []
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')
        
        for severity, patterns in PATTERNS.items():
            for pat in patterns:
                if not filepath.match(pat["file"]):
                    continue
                for i, line in enumerate(lines, 1):
                    if re.search(pat["pattern"], line):
                        issues.append({
                            "severity": severity,
                            "name": pat["name"],
                            "file": str(filepath.relative_to(PROJECT_ROOT)),
                            "line": i,
                            "code": line.strip()[:80],
                            "fix": pat["fix"]
                        })
    except Exception as e:
        issues.append({
            "severity": "low",
            "name": f"Erro ao ler arquivo: {e}",
            "file": str(filepath.relative_to(PROJECT_ROOT)),
            "line": 0,
            "code": "",
            "fix": "Verificar permissões"
        })
    
    return issues


def scan_project() -> dict:
    """Escaneia todo o projeto e retorna problemas agrupados."""
    all_issues = []
    
    # Arquivos para escanear
    extensions = ["*.py", "*.js", "*.html"]
    exclude_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv"}
    
    for ext in extensions:
        for filepath in PROJECT_ROOT.rglob(ext):
            # Pular diretórios excluídos
            if any(excluded in filepath.parts for excluded in exclude_dirs):
                continue
            all_issues.extend(scan_file(filepath))
    
    # Agrupar por severidade
    grouped = {"critical": [], "high": [], "medium": [], "low": []}
    for issue in all_issues:
        grouped[issue["severity"]].append(issue)
    
    return grouped


def generate_report(issues: dict) -> str:
    """Gera relatório formatado dos problemas."""
    total = sum(len(v) for v in issues.values())
    
    report = []
    report.append("=" * 60)
    report.append("  RELATORIO DE MELHORIA CONTINUA")
    report.append(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("=" * 60)
    report.append(f"\n  Total de problemas: {total}")
    report.append(f"  Criticos: {len(issues['critical'])}")
    report.append(f"  Altos: {len(issues['high'])}")
    report.append(f"  Medios: {len(issues['medium'])}")
    report.append(f"  Baixos: {len(issues['low'])}")
    report.append("")
    
    severity_emoji = {
        "critical": "[CRITICO]",
        "high": "[ALTO]",
        "medium": "[MEDIO]",
        "low": "[BAIXO]"
    }
    
    for severity in ["critical", "high", "medium", "low"]:
        if issues[severity]:
            report.append(f"\n{'─' * 60}")
            report.append(f"  {severity_emoji[severity]} {severity.upper()} ({len(issues[severity])})")
            report.append(f"{'─' * 60}")
            
            for issue in issues[severity]:
                report.append(f"\n  >> {issue['name']}")
                report.append(f"     Arquivo: {issue['file']}:{issue['line']}")
                if issue['code']:
                    report.append(f"     Codigo: {issue['code'][:60]}...")
                report.append(f"     Solucao: {issue['fix']}")
    
    # Sugestões
    report.append(f"\n{'═' * 60}")
    report.append("  SUGESTOES DE MELHORIA")
    report.append(f"{'═' * 60}")
    
    for area, suggestions in SUGGESTIONS.items():
        report.append(f"\n  [{area.upper()}]")
        for s in suggestions:
            report.append(f"     - {s}")
    
    # Páginas sem handler
    report.append(f"\n{'─' * 60}")
    report.append("  PAGINAS SEM HANDLER NO loadPageData")
    report.append(f"{'─' * 60}")
    for page in PAGES_WITHOUT_HANDLER:
        report.append(f"     - {page}")
    
    report.append(f"\n{'═' * 60}")
    report.append("  FIM DO RELATORIO")
    report.append(f"{'═' * 60}")
    
    return "\n".join(report)


def main():
    """Executa o scan e gera relatório."""
    print("\nEscaneando projeto...\n")
    
    issues = scan_project()
    report = generate_report(issues)
    
    print(report)
    
    # Salvar relatório
    report_path = PROJECT_ROOT / "acervo" / "relatorios"
    report_path.mkdir(parents=True, exist_ok=True)
    
    filename = f"melhoria_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    filepath = report_path / filename
    filepath.write_text(report, encoding='utf-8')
    
    print(f"\nRelatorio salvo em: {filepath}")
    
    # Retornar código de saída baseado em bugs críticos
    if issues["critical"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
