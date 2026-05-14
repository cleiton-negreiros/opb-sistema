#!/usr/bin/env python3
"""
🚀 OPB API Server — Micro servidor Flask
Conecta a plataforma web aos agentes reais via API REST.

Uso:
    python api_server.py
    Acesse: http://localhost:5000
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Configurar encoding para UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# === CONFIGURAÇÃO ===
PROJECT_PATH = Path(__file__).parent.resolve()
FRONTEND_PATH = PROJECT_PATH / "cerebro" / "perfil-empreendedor-solo"
PORT = 5000
DEBUG = True

app = Flask(__name__, static_folder=str(FRONTEND_PATH), static_url_path='')
CORS(app)

# ============================================
# UTILIDADES
# ============================================

def run_agent(agent_path: str, args: list = None) -> dict:
    """Executa um agente Python e retorna stdout/stderr."""
    full_path = PROJECT_PATH / agent_path
    if not full_path.exists():
        return {"error": f"Agente não encontrado: {agent_path}", "code": 404}

    try:
        cmd = [sys.executable, str(full_path)] + (args or [])
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(PROJECT_PATH),
            encoding='utf-8',
            errors='replace'
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "success": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {"error": "Timeout: agente demorou demais", "code": 408}
    except Exception as e:
        return {"error": str(e), "code": 500}


def get_project_stats() -> dict:
    """Coleta estatísticas do projeto."""
    stats = {
        "agentes_total": 0,
        "agentes_ativos": 0,
        "ideias_salvas": 0,
        "transcricoes": 0,
        "carrossel_gerados": 0,
        "conhecimento_salvo": 0,
        "capas_geradas": 0,
        "posts_gerados": 0,
    }

    # Contar agentes
    agents_path = PROJECT_PATH / "agents"
    if agents_path.exists():
        for d in agents_path.iterdir():
            if d.is_dir() and (d / "main.py").exists():
                stats["agentes_total"] += 1
                if (d / "STATUS.md").exists():
                    content = (d / "STATUS.md").read_text(errors='ignore')
                    if "✅ Concluído" in content:
                        stats["agentes_ativos"] += 1

    # Contar ideias
    ideias_path = PROJECT_PATH / "acervo" / "ideias"
    if ideias_path.exists():
        stats["ideias_salvas"] = len([f for f in ideias_path.glob("*.md") if f.name != "index.md"])

    # Contar transcricoes
    transc_path = PROJECT_PATH / "acervo" / "transcricoes"
    if transc_path.exists():
        stats["transcricoes"] = len([f for f in transc_path.glob("*.md") if f.name != "index.md"])

    # Contar carrosséis
    carrossel_path = PROJECT_PATH / "acervo" / "carrossel"
    if carrossel_path.exists():
        stats["carrossel_gerados"] = len([f for f in carrossel_path.glob("*.md") if f.name != "index.md"])

    # Contar conhecimento
    conhecimento_path = PROJECT_PATH / "acervo" / "conhecimento"
    if conhecimento_path.exists():
        stats["conhecimento_salvo"] = len([f for f in conhecimento_path.glob("*.md") if f.name != "index.md"])

    # Contar capas
    capas_path = PROJECT_PATH / "acervo" / "capas"
    if capas_path.exists():
        stats["capas_geradas"] = len([f for f in capas_path.glob("*.md") if f.name != "index.md"])

    # Contar posts
    posts_path = PROJECT_PATH / "output" / "text_posts"
    if posts_path.exists():
        stats["posts_gerados"] = len([f for f in posts_path.glob("*.txt")])

    stats["timestamp"] = datetime.now().isoformat()
    return stats


def read_file_safe(path: Path) -> str:
    """Lê arquivo com fallback seguro."""
    try:
        if path.exists():
            return path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        pass
    return ""


# ============================================
# ROTA PRINCIPAL — SERVIR FRONTEND
# ============================================

@app.route('/')
def serve_frontend():
    """Serve a plataforma HTML."""
    index_path = FRONTEND_PATH / "plataforma.html"
    if index_path.exists():
        return send_from_directory(str(FRONTEND_PATH), "plataforma.html")
    return jsonify({"error": "Frontend não encontrado"}), 404


@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "online",
        "project_path": str(PROJECT_PATH),
        "timestamp": datetime.now().isoformat()
    })


# ============================================
# API — DASHBOARD
# ============================================

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Retorna estatísticas do projeto."""
    return jsonify(get_project_stats())


@app.route('/api/agentes', methods=['GET'])
def api_agentes():
    """Lista todos os agentes disponíveis."""
    agentes = []
    agents_path = PROJECT_PATH / "agents"

    if agents_path.exists():
        for d in sorted(agents_path.iterdir()):
            if d.is_dir() and (d / "main.py").exists():
                soul = {}
                soul_path = d / "SOUL.md"
                if soul_path.exists():
                    lines = soul_path.read_text(errors='ignore').split('\n')
                    for line in lines:
                        if line.startswith('- **Nome**: '):
                            soul['nome'] = line.replace('- **Nome**: ', '')
                        elif line.startswith('- **Tipo**: '):
                            soul['tipo'] = line.replace('- **Tipo**: ', '')
                        elif line.startswith('> '):
                            soul['descricao'] = line[2:]

                status_path = d / "STATUS.md"
                status = "desconhecido"
                if status_path.exists():
                    content = status_path.read_text(errors='ignore')
                    if "✅ Concluído" in content:
                        status = "ativo"
                    elif "🔜" in content:
                        status = "em_desenvolvimento"

                agentes.append({
                    "nome": soul.get('nome', d.name),
                    "pasta": d.name,
                    "tipo": soul.get('tipo', 'Agente'),
                    "descricao": soul.get('descricao', ''),
                    "status": status,
                    "icone": {
                        "transcricao": "fa-microphone-alt",
                        "capa_video": "fa-image",
                        "carrossel": "fa-layer-group",
                        "consumo": "fa-book-reader",
                        "text_generator": "fa-pen-fancy",
                        "posicionamento": "fa-crosshairs",
                        "designer": "fa-paint-brush",
                        "coordinator": "fa-cogs",
                        "telegram_bot": "fa-paper-plane",
                    }.get(d.name, "fa-robot")
                })

    return jsonify(agentes)


# ============================================
# API — CERÉBRO
# ============================================

@app.route('/api/cerebro/arvore', methods=['GET'])
def api_cerebro_arvore():
    """Retorna a árvore de arquivos do cérebro."""
    cerebro_path = PROJECT_PATH / "cerebro"
    arvore = []

    if cerebro_path.exists():
        for item in sorted(cerebro_path.rglob("*")):
            if '.git' in str(item):
                continue
            rel = item.relative_to(PROJECT_PATH)
            if item.is_dir():
                arvore.append({
                    "nome": item.name,
                    "caminho": str(rel),
                    "tipo": "pasta"
                })
            else:
                arvore.append({
                    "nome": item.name,
                    "caminho": str(rel),
                    "tipo": "arquivo",
                    "tamanho": item.stat().st_size if item.exists() else 0,
                    "modificado": datetime.fromtimestamp(item.stat().st_mtime).isoformat() if item.exists() else None
                })

    return jsonify(arvore)


@app.route('/api/cerebro/ler', methods=['GET'])
def api_cerebro_ler():
    """Lê o conteúdo de um arquivo do cérebro."""
    caminho = request.args.get('caminho', '')
    if not caminho:
        return jsonify({"error": "Parâmetro 'caminho' obrigatório"}), 400

    full_path = PROJECT_PATH / caminho
    if not full_path.exists():
        return jsonify({"error": "Arquivo não encontrado"}), 404

    conteudo = read_file_safe(full_path)
    return jsonify({
        "caminho": caminho,
        "conteudo": conteudo,
        "nome": full_path.name
    })


@app.route('/api/cerebro/mapas', methods=['GET'])
def api_cerebro_mapas():
    """Lista todos os MAPAs disponíveis."""
    mapas = []
    for f in PROJECT_PATH.rglob("MAPA.md"):
        rel = f.relative_to(PROJECT_PATH)
        conteudo = read_file_safe(f)
        # Extrai primeira linha de conteúdo como descrição
        linhas = conteudo.split('\n')
        desc = ""
        for l in linhas:
            if l.strip() and not l.startswith('#') and not l.startswith('---') and not l.startswith('>'):
                desc = l.strip()[:80]
                break
        mapas.append({
            "caminho": str(rel),
            "pasta": str(rel.parent),
            "descricao": desc
        })
    return jsonify(mapas)


# ============================================
# API — TRANCRIÇÃO
# ============================================

@app.route('/api/transcricao', methods=['POST'])
def api_transcricao():
    """Inicia transcrição de vídeo do YouTube."""
    data = request.get_json()
    url = data.get('url', '')

    if not url:
        return jsonify({"error": "URL não informada"}), 400

    # Executar agente de transcrição
    result = run_agent("agents/transcricao/main.py", [url])

    return jsonify({
        "sucesso": result["success"],
        "saida": result["stdout"],
        "erro": result["stderr"],
        "mensagem": "Transcrição iniciada!" if result["success"] else "Falha na transcrição"
    })


# ============================================
# API — CAPA DE VÍDEO
# ============================================

@app.route('/api/capa-video', methods=['POST'])
def api_capa_video():
    """Gera ideias de capa de vídeo."""
    data = request.get_json()
    tema = data.get('tema', '')
    quantidade = data.get('quantidade', 5)

    if not tema:
        return jsonify({"error": "Tema não informado"}), 400

    result = run_agent("agents/capa_video/main.py", [tema, str(quantidade)])

    return jsonify({
        "sucesso": result["success"],
        "saida": result["stdout"],
        "mensagem": f"Capas geradas para: {tema}"
    })


# ============================================
# API — CARROSSEL
# ============================================

@app.route('/api/carrossel', methods=['POST'])
def api_carrossel():
     """Gera carrossel para Instagram."""
     data = request.get_json()
     tema = data.get('tema', '')
     tipo = data.get('tipo', 'educational')
     slides = data.get('slides', None)

     if not tema:
         return jsonify({"error": "Tema não informado"}), 400

     args = [tema, tipo]
     if slides:
         args.append(str(slides))

     result = run_agent("agents/carrossel/main.py", args)

     return jsonify({
         "sucesso": result.get("success", False),
         "saida": result.get("stdout", ""),
         "erro": result.get("stderr", result.get("error", "")),
         "mensagem": f"Carrossel gerado: {tema}" if result.get("success", False) else f"Erro ao gerar carrossel: {result.get('error', result.get('stderr', 'Erro desconhecido'))}"
     })


# ============================================
# API — CONSUMO DE CONTEÚDO
# ============================================

@app.route('/api/consumo', methods=['POST'])
def api_consumo():
    """Processa conteúdo via Agente de Consumo."""
    data = request.get_json()
    input_text = data.get('input', '')
    tipo = data.get('tipo', 'completo')
    titulo = data.get('titulo', '')

    if not input_text:
        return jsonify({"error": "Conteúdo não informado"}), 400

    # Salva o input temporariamente
    input_file = PROJECT_PATH / "agents" / "consumo" / "_input_temp.txt"
    input_file.write_text(input_text, encoding='utf-8')

    result = run_agent("agents/consumo/alimentar_com_input.py", [input_text[:2000], tipo, titulo])

    return jsonify({
        "sucesso": True,
        "mensagem": "Conteúdo processado e salvo no cérebro",
        "tipo": tipo,
        "titulo": titulo
    })


# ============================================
# API — TEXT GENERATOR
# ============================================

@app.route('/api/text-generator', methods=['POST'])
def api_text_generator():
    """Gera posts para Instagram."""
    data = request.get_json()
    objetivo = data.get('objetivo', '')
    tipo = data.get('tipo', 'educational')

    if not objetivo:
        return jsonify({"error": "Objetivo não informado"}), 400

    result = run_agent("agents/text_generator/main.py", [objetivo, tipo])

    return jsonify({
        "sucesso": result["success"],
        "saida": result["stdout"],
        "mensagem": "Post gerado com sucesso!"
    })


# ============================================
# API — POSICIONAMENTO
# ============================================

@app.route('/api/posicionamento', methods=['POST'])
def api_posicionamento():
    """Analisa posicionamento."""
    data = request.get_json()
    nicho = data.get('nicho', '')
    concorrentes = data.get('concorrentes', '')

    result_text = f"Análise de posicionamento para o nicho: {nicho}\n"
    if concorrentes:
        lista = [c.strip() for c in concorrentes.split('\n') if c.strip()]
        result_text += f"\nConcorrentes ({len(lista)}):\n"
        for i, c in enumerate(lista, 1):
            result_text += f"  {i}. @{c}\n"

    return jsonify({
        "sucesso": True,
        "analise": result_text,
        "mensagem": "Análise de posicionamento gerada"
    })


# ============================================
# API — ALIMENTAR CÉREBRO
# ============================================

@app.route('/api/alimentar', methods=['POST'])
def api_alimentar():
     """Alimenta o cérebro com conteúdo."""
     data = request.get_json()
     input_text = data.get('input', '')
     tipo = data.get('tipo', 'completo')
     titulo = data.get('titulo', 'Conteudo')

     if not input_text:
         return jsonify({"error": "Conteúdo não informado"}), 400

     # Usa o alimentar_com_input.py via subprocess (igual ao /api/consumo)
     result = run_agent("agents/consumo/alimentar_com_input.py", [input_text[:2000], tipo, titulo])

     sucesso = result["returncode"] == 0
     return jsonify({
         "sucesso": sucesso,
         "saida": result.get("stdout", ""),
         "erro": result.get("stderr", ""),
         "mensagem": "Cérebro alimentado com sucesso!" if sucesso else "Erro ao alimentar"
     })


# ============================================
# API — IDEIAS (via Telegram)
# ============================================

@app.route('/api/ideias', methods=['GET'])
def api_ideias():
    """Lista ideias salvas."""
    ideias_path = PROJECT_PATH / "acervo" / "ideias"
    ideias = []

    if ideias_path.exists():
        for f in sorted(ideias_path.glob("*.md"), reverse=True)[:20]:
            content = read_file_safe(f)
            # Extrair título
            titulo = f.stem
            linhas = content.split('\n')
            for linha in linhas:
                if linha.startswith('# '):
                    titulo = linha[2:]
                    break
            ideias.append({
                "titulo": titulo[:80],
                "arquivo": f.name,
                "data": f.stem[:16] if len(f.stem) > 16 else f.stem
            })

    return jsonify({"ideias": ideias, "total": len(ideias)})


# ============================================
# API — INICIAR TELEGRAM BOT
# ============================================

@app.route('/api/bot/start', methods=['POST'])
def api_start_bot():
    """Inicia o Telegram Bot em background."""
    bot_path = PROJECT_PATH / "agents" / "telegram_bot" / "main.py"

    if not bot_path.exists():
        return jsonify({"error": "Bot script não encontrado", "sucesso": False}), 404

    try:
        # Verifica se já está rodando
        result = subprocess.run(
            ['tasklist', '/FI', 'imagename eq python.exe'],
            capture_output=True, text=True, encoding='utf-8', errors='replace'
        )
        if 'telegram_bot' in result.stdout.lower() or 'main.py' in result.stdout.lower():
            return jsonify({
                "sucesso": True,
                "mensagem": "🤖 Bot já está em execução!",
                "status": "already_running"
            })

        # Inicia o bot em background
        subprocess.Popen(
            [sys.executable, str(bot_path)],
            cwd=str(PROJECT_PATH),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )

        return jsonify({
            "sucesso": True,
            "mensagem": "🤖 Bot iniciado com sucesso!",
            "status": "started"
        })
    except Exception as e:
        return jsonify({"error": str(e), "sucesso": False}), 500


# ============================================
# SERVIR ARQUIVOS ESTÁTICOS
# ============================================

@app.route('/<path:path>', methods=['GET'])
def serve_static(path):
    """Serve arquivos estáticos do frontend."""
    static_files = ['plataforma.html', 'favicon.ico', 'manifest.json']
    if path in static_files or path.endswith(('.js', '.css', '.json', '.png', '.jpg', '.svg', '.ico')):
        filepath = FRONTEND_PATH / path
        if filepath.exists():
            return send_from_directory(str(FRONTEND_PATH), path)
    return serve_frontend()


# ============================================
# INICIALIZAÇÃO
# ============================================

if __name__ == '__main__':
    print("=" * 50)
    print("OPB API Server")
    print("Projeto: " + str(PROJECT_PATH))
    print("Porta: " + str(PORT))
    print("URL: http://localhost:" + str(PORT))
    print("=" * 50)

    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=DEBUG,
        use_reloader=False
    )