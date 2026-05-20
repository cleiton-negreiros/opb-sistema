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
from flask import Flask, request, jsonify, send_from_directory, g
from flask_cors import CORS

# Configurar encoding para UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['LANG'] = 'en_US.UTF-8'
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

# === CONFIGURAÇÃO ===
PROJECT_PATH = Path(__file__).parent.resolve()
FRONTEND_PATH = PROJECT_PATH / "cerebro" / "perfil-empreendedor-solo"
PORT = 5000
DEBUG = True

app = Flask(__name__, static_folder=str(FRONTEND_PATH), static_url_path='')
CORS(app)

# === VALIDATION INIT ===
try:
    from validation import required_fields, validate_field, validate_email, validate_username, max_length, rate_limit, handle_errors
    VALIDATION_ENABLED = True
    print("✅ Validação de inputs ativada")
except Exception as e:
    print(f"⚠️  Validação não carregada: {e}")
    VALIDATION_ENABLED = False
    def required_fields(*fields):
        def decorator(f):
            return f
        return decorator
    def validate_field(field_name, validator, error_message):
        def decorator(f):
            return f
        return decorator
    def max_length(field_name, max_len):
        def decorator(f):
            return f
        return decorator
    def rate_limit(max_requests=60, window=60):
        def decorator(f):
            return f
        return decorator
    def handle_errors(f):
        return f

# === AUTH INIT ===
AUTH_ENABLED = False  # Disabled for now
try:
    from auth import init_db, close_db, require_auth, optional_auth, authenticate_user, create_user, validate_token, logout_user, complete_onboarding, get_user_settings, update_user_settings, track_usage, get_usage_stats, get_user_data_dir, get_user_acervo_dir, get_user_cerebro_dir, get_user_output_dir
    init_db()
    app.teardown_appcontext(close_db)
    # AUTH_ENABLED = True  # Disabled for now
    print("⚠️  Sistema de autenticação desabilitado (temporariamente)")
except Exception as e:
    print(f"⚠️  Auth não carregado: {e}")

def require_auth(f):
    return f

def optional_auth(f):
    return f

def get_user_acervo_dir(user_id):
    return str(PROJECT_PATH / "acervo")

def get_user_cerebro_dir(user_id):
    return str(PROJECT_PATH / "cerebro")

def get_user_output_dir(user_id):
    return str(PROJECT_PATH / "output")

# === PROFILE MANAGER ===
try:
    from profile_manager import (
        get_active_profile, set_active_profile, list_profiles,
        get_profile_config, get_acervo_path, get_cerebro_path,
        get_output_path, get_perfil_path
    )
    PROFILE_ENABLED = True
    print(f"✅ Multi-perfil ativado (ativo: {get_active_profile()})")
except Exception as e:
    print(f"⚠️  Profile manager não carregado: {e}")
    PROFILE_ENABLED = False
    def get_active_profile(): return "paz-na-conta"
    def set_active_profile(p): return {"success": False}
    def list_profiles(): return []
    def get_profile_config(p=None): return None
    def get_acervo_path(p=None): return PROJECT_PATH / "acervo"
    def get_cerebro_path(p=None): return PROJECT_PATH / "cerebro"
    def get_output_path(p=None): return PROJECT_PATH / "output"
    def get_perfil_path(p=None): return PROJECT_PATH / "cerebro" / "perfil-empreendedor-solo"

def get_project_path_for_user():
    """Get project path, user-specific if authenticated"""
    if AUTH_ENABLED and hasattr(request, 'user'):
        return Path(get_user_data_dir(request.user['id']))
    return PROJECT_PATH

def get_acervo_path_for_user():
    """Get acervo path - uses active profile"""
    return get_acervo_path()

def get_output_path_for_user():
    """Get output path - uses active profile"""
    return get_output_path()

def get_cerebro_path_for_user():
    """Get cerebro path - uses active profile"""
    return get_cerebro_path()

def get_perfil_path_for_user():
    """Get perfil path - uses active profile"""
    return get_perfil_path()

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
            timeout=180,
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
    acervo_path = get_acervo_path_for_user()
    output_path = get_output_path_for_user()

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

    # Contar agentes (shared)
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
    ideias_path = acervo_path / "ideias"
    if ideias_path.exists():
        stats["ideias_salvas"] = len([f for f in ideias_path.glob("*.md") if f.name != "index.md"])

    # Contar transcricoes
    transc_path = acervo_path / "transcricoes"
    if transc_path.exists():
        stats["transcricoes"] = len([f for f in transc_path.glob("*.md") if f.name != "index.md"])

    # Contar carrosséis
    carrossel_path = acervo_path / "carrossel"
    if carrossel_path.exists():
        stats["carrossel_gerados"] = len([f for f in carrossel_path.glob("*.md") if f.name != "index.md"])

    # Contar conhecimento
    conhecimento_path = acervo_path / "conhecimento"
    if conhecimento_path.exists():
        stats["conhecimento_salvo"] = len([f for f in conhecimento_path.glob("*.md") if f.name != "index.md"])

    # Contar capas
    capas_path = acervo_path / "capas"
    if capas_path.exists():
        stats["capas_geradas"] = len([f for f in capas_path.glob("*.md") if f.name != "index.md"])

    # Contar posts
    posts_path = output_path / "text_posts"
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
    """Redirect para a plataforma."""
    from flask import redirect
    return redirect('/plataforma.html')


@app.route('/landing.html')
def serve_landing():
    """Serve a landing page."""
    index_path = FRONTEND_PATH / "landing.html"
    if index_path.exists():
        return send_from_directory(str(FRONTEND_PATH), "landing.html")
    return jsonify({"error": "Landing page não encontrada"}), 404


@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "online",
        "project_path": str(PROJECT_PATH),
        "timestamp": datetime.now().isoformat(),
        "auth_enabled": AUTH_ENABLED
    })


# ============================================
# API — AUTENTICAÇÃO
# ============================================

@app.route('/api/auth/register', methods=['POST'])
@rate_limit(max_requests=5, window=300)  # 5 registrations per 5 minutes
@handle_errors
def api_auth_register():
    """Registrar novo usuário."""
    if not AUTH_ENABLED:
        return jsonify({"error": "Auth não disponível"}), 503

    data = request.get_json()
    email = data.get('email', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    full_name = data.get('full_name', '').strip()

    if not email or not username or not password:
        return jsonify({"error": "Email, usuário e senha são obrigatórios"}), 400

    if not validate_email(email):
        return jsonify({"error": "Email inválido"}), 400

    if not validate_username(username):
        return jsonify({"error": "Usuário deve ter 3-30 caracteres (letras, números, underscore)"}), 400

    if len(password) < 6:
        return jsonify({"error": "Senha deve ter no mínimo 6 caracteres"}), 400

    full_name = full_name[:100] if full_name else None

    result = create_user(email, username, password, full_name)
    if result['success']:
        return jsonify({"message": result['message'], "user_id": result['user_id']}), 201
    return jsonify({"error": result['message']}), 400


@app.route('/api/auth/login', methods=['POST'])
@rate_limit(max_requests=10, window=60)  # 10 logins per minute
@handle_errors
def api_auth_login():
    """Login de usuário."""
    if not AUTH_ENABLED:
        return jsonify({"error": "Auth não disponível"}), 503

    data = request.get_json()
    email_or_username = data.get('email_or_username', '').strip()
    password = data.get('password', '')

    if not email_or_username or not password:
        return jsonify({"error": "Usuário e senha são obrigatórios"}), 400

    result = authenticate_user(email_or_username, password)
    if result['success']:
        response = jsonify({
            "message": result['message'],
            "token": result['token'],
            "user": result['user']
        })
        response.set_cookie('opb_token', result['token'], httponly=True, max_age=86400, samesite='Lax')
        return response
    return jsonify({"error": result['message']}), 401


@app.route('/api/auth/validate', methods=['GET'])
def api_auth_validate():
    """Validar token."""
    if not AUTH_ENABLED:
        return jsonify({"error": "Auth não disponível"}), 503

    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        token = request.cookies.get('opb_token')
    if not token:
        token = request.args.get('token')

    if not token:
        return jsonify({"success": False, "message": "Token não fornecido"}), 401

    result = validate_token(token)
    if result['success']:
        return jsonify(result)
    return jsonify(result), 401


@app.route('/api/auth/logout', methods=['POST'])
@require_auth
def api_auth_logout():
    """Logout de usuário."""
    if not AUTH_ENABLED:
        return jsonify({"error": "Auth não disponível"}), 503

    result = logout_user(request.token)
    response = jsonify(result)
    response.delete_cookie('opb_token')
    return response


@app.route('/api/auth/onboarding', methods=['POST'])
@require_auth
def api_auth_onboarding():
    """Completar onboarding."""
    if not AUTH_ENABLED:
        return jsonify({"error": "Auth não disponível"}), 503

    data = request.get_json()
    user_id = request.user['id']

    # Save onboarding data to user settings
    settings = {
        'theme': data.get('theme', 'dark'),
        'notifications_enabled': 1 if data.get('notifications') == 'enabled' else 0,
    }
    if data.get('telegram_token'):
        settings['telegram_connected'] = 1
        settings['telegram_chat_id'] = data.get('telegram_token')
    if data.get('api_url'):
        settings['api_url'] = data.get('api_url')

    update_user_settings(user_id, settings)
    complete_onboarding(user_id)

    # Track onboarding completion
    track_usage(user_id, 'onboarding_complete', details=data)

    return jsonify({"success": True, "message": "Onboarding completo"})


@app.route('/api/auth/settings', methods=['GET'])
@require_auth
def api_auth_settings():
    """Obter configurações do usuário."""
    if not AUTH_ENABLED:
        return jsonify({"error": "Auth não disponível"}), 503

    settings = get_user_settings(request.user['id'])
    return jsonify(settings)


@app.route('/api/auth/settings', methods=['PUT'])
@require_auth
def api_auth_update_settings():
    """Atualizar configurações do usuário."""
    if not AUTH_ENABLED:
        return jsonify({"error": "Auth não disponível"}), 503

    data = request.get_json()
    result = update_user_settings(request.user['id'], data)
    return jsonify(result)


@app.route('/api/auth/analytics', methods=['GET'])
@require_auth
def api_auth_analytics():
    """Obter analytics do usuário."""
    if not AUTH_ENABLED:
        return jsonify({"error": "Auth não disponível"}), 503

    days = request.args.get('days', 30, type=int)
    stats = get_usage_stats(request.user['id'], days)
    return jsonify({"stats": stats, "days": days})


# ============================================
# API — PERFIS (Multi-Profile)
# ============================================

@app.route('/api/perfis', methods=['GET'])
def api_perfis_list():
    """Lista todos os perfis disponíveis."""
    perfis = list_profiles()
    ativo = get_active_profile()
    return jsonify({
        "perfis": perfis,
        "ativo": ativo,
        "total": len(perfis)
    })


@app.route('/api/perfis/ativo', methods=['GET'])
def api_perfil_ativo():
    """Retorna o perfil ativo."""
    perfil_id = get_active_profile()
    config = get_profile_config(perfil_id)
    return jsonify({
        "id": perfil_id,
        "config": config or {}
    })


@app.route('/api/perfis/ativo', methods=['POST'])
def api_perfil_switch():
    """Troca o perfil ativo."""
    data = request.get_json()
    perfil_id = data.get('perfil_id', '')

    if not perfil_id:
        return jsonify({"error": "perfil_id obrigatório"}), 400

    result = set_active_profile(perfil_id)
    if result['success']:
        config = get_profile_config(perfil_id)
        return jsonify({
            "success": True,
            "message": f"Perfil trocado para {config.get('nome', perfil_id)}",
            "perfil_id": perfil_id,
            "config": config
        })
    return jsonify(result), 400


@app.route('/api/perfis/<perfil_id>/config', methods=['GET'])
def api_perfil_config(perfil_id):
    """Retorna config de um perfil específico."""
    config = get_profile_config(perfil_id)
    if config:
        return jsonify(config)
    return jsonify({"error": "Perfil não encontrado"}), 404


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
     tema = data.get('tema', data.get('texto', ''))
     tipo = data.get('tipo', 'educational')
     slides = data.get('slides', None)

     if not tema:
         return jsonify({"error": "Tema ou texto não informado"}), 400

     # Trunca texto longo para usar como tema
     if len(tema) > 60:
         tema = tema[:57] + '...'

     args = [tema, tipo]
     if slides:
         args.append(str(slides))

     result = run_agent("agents/carrossel/main.py", args)

     # Pega o arquivo gerado mais recente (user-specific)
     carrossel_path = get_acervo_path_for_user() / "carrossel"
     conteudo = ""
     filename = ""
     if result.get("success", False) and carrossel_path.exists():
         files = sorted(carrossel_path.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
         files = [f for f in files if f.name != "index.md"]
         if files:
             filename = files[0].name
             conteudo = files[0].read_text(encoding='utf-8')

     return jsonify({
         "sucesso": result.get("success", False),
         "saida": result.get("stdout", ""),
         "conteudo": conteudo,
         "filename": filename,
         "erro": result.get("stderr", result.get("error", "")),
         "mensagem": f"Carrossel gerado: {tema}" if result.get("success", False) else f"Erro ao gerar carrossel: {result.get('error', result.get('stderr', 'Erro desconhecido'))}"
     })

@app.route('/api/carrossel/lista', methods=['GET'])
def api_carrossel_lista():
    """Lista todos os carrosséis gerados."""
    carrossel_path = get_acervo_path_for_user() / "carrossel"
    if not carrossel_path.exists():
        return jsonify({"carrosseis": []})

    files = sorted(carrossel_path.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    files = [f for f in files if f.name != "index.md"]

    lista = []
    for f in files:
        content = f.read_text(encoding='utf-8')
        titulo = f.stem.replace('-', ' ').title()
        slides = 0
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                for line in parts[1].split('\n'):
                    line = line.strip()
                    if line.startswith('name:') or line.startswith('titulo:'):
                        titulo = line.split(':', 1)[-1].strip().strip('"').strip("'")
                    if line.startswith('slides:'):
                        try: slides = int(line.split(':', 1)[-1].strip())
                        except: pass

        lista.append({
            "filename": f.name,
            "titulo": titulo,
            "slides": slides,
            "data": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
            "tamanho": len(content)
        })

    return jsonify({"carrosseis": lista})

@app.route('/api/carrossel/<filename>', methods=['GET'])
def api_carrossel_get(filename):
    """Retorna o conteúdo de um carrossel."""
    filepath = get_acervo_path_for_user() / "carrossel" / filename
    if not filepath.exists():
        return jsonify({"error": "Carrossel não encontrado"}), 404
    content = filepath.read_text(encoding='utf-8')
    return jsonify({"filename": filename, "conteudo": content})

@app.route('/api/carrossel/<filename>', methods=['PUT'])
def api_carrossel_update(filename):
    """Atualiza um carrossel existente."""
    filepath = get_acervo_path_for_user() / "carrossel" / filename
    if not filepath.exists():
        return jsonify({"error": "Carrossel não encontrado"}), 404
    data = request.get_json()
    novo_conteudo = data.get('conteudo', '')
    if not novo_conteudo:
        return jsonify({"error": "Conteúdo não informado"}), 400
    filepath.write_text(novo_conteudo, encoding='utf-8')
    return jsonify({"sucesso": True, "mensagem": "Carrossel atualizado"})

@app.route('/api/carrossel/<filename>', methods=['DELETE'])
def api_carrossel_delete(filename):
    """Deleta um carrossel."""
    filepath = get_acervo_path_for_user() / "carrossel" / filename
    if not filepath.exists():
        return jsonify({"error": "Carrossel não encontrado"}), 404
    filepath.unlink()
    return jsonify({"sucesso": True, "mensagem": "Carrossel deletado"})


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
    ideias_path = get_acervo_path_for_user() / "ideias"
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
# API — NARVI (Editor de Vídeo)
# ============================================

@app.route('/api/narvi', methods=['POST'])
def api_narvi():
    """Executa o agente Narvi para edição de vídeo."""
    data = request.get_json()
    video = data.get('video', '')
    corte = data.get('corte', 'medio')
    ratio = data.get('ratio', 'both')

    return jsonify({
        "sucesso": True,
        "mensagem": "Narvi requer FFmpeg instalado",
        "instrucao": f"python agents/narvi/narvi.py \"{video}\" --corte={corte} --ratio={ratio}",
        "saida": "~/Desktop/narvi-saida/"
    })


# ============================================
# API — RADAGAST (Curadoria de Conteúdo)
# ============================================

@app.route('/api/radagast', methods=['POST'])
def api_radagast():
    """Executa o agente Radagast para curadoria de conteúdo."""
    data = request.get_json()
    days_back = data.get('days_back', 1)

    return jsonify({
        "sucesso": True,
        "mensagem": "Radagast usa fontes gratuitas (yt-dlp + RSS)",
        "instrucao": "Configure agents/radagast/.env (só Telegram) e config/keywords.json",
        "execucao": "python agents/radagast/radagast.py --dry-run (teste) / python agents/radagast/radagast.py (executar)"
    })


# ============================================
# API — LISTAR TRANSCRIÇÕES
# ============================================

@app.route('/api/transcricoes', methods=['GET'])
def api_listar_transcricoes():
    """Lista transcrições salvas."""
    transc_path = get_acervo_path_for_user() / "transcricoes"
    arquivos = []
    if transc_path.exists():
        for f in sorted(transc_path.glob("*.md"), reverse=True):
            if f.name == "index.md":
                continue
            metadata = {}
            content = f.read_text(encoding='utf-8', errors='replace')
            for line in content.split('\n'):
                if line.startswith('name: "') or line.startswith("name: '"):
                    metadata['titulo'] = line.split('"')[1] if '"' in line else line.split("'")[1]
                if line.startswith('video_id:'):
                    metadata['video_id'] = line.split(':')[1].strip()
                if 'data:' in line:
                    val = line.split(':')[1].strip().strip('"')
                    if val.count('-') == 2 and len(val) == 10:
                        metadata['data'] = val
                if line.startswith('duracao:'):
                    metadata['duracao'] = line.split(':')[1].strip()
            arquivos.append({
                "nome": f.stem,
                "arquivo": f.name,
                "metadata": metadata
            })
    return jsonify({"transcricoes": arquivos, "total": len(arquivos)})


# ============================================
# API — LER TRANSCRIÇÃO
# ============================================

@app.route('/api/transcricao/ler', methods=['POST'])
def api_ler_transcricao():
    """Lê uma transcrição específica."""
    data = request.get_json()
    nome = data.get('nome', '')
    if not nome:
        return jsonify({"error": "Nome não informado"}), 400
    path = get_acervo_path_for_user() / "transcricoes" / nome
    if not path.exists():
        arquivos = list((get_acervo_path_for_user() / "transcricoes").glob(f"*{nome}*.md"))
        if arquivos:
            path = arquivos[0]
        else:
            return jsonify({"error": "Transcrição não encontrada"}), 404
    return jsonify({
        "sucesso": True,
        "conteudo": path.read_text(encoding='utf-8', errors='replace'),
        "arquivo": path.name
    })


# ============================================
# API — LISTAR ARQUIVOS (navegador de arquivos)
# ============================================

@app.route('/api/arquivos', methods=['POST'])
def api_listar_arquivos():
    """Lista arquivos em um diretório do projeto."""
    data = request.get_json()
    caminho = data.get('caminho', '')
    base = PROJECT_PATH
    if caminho:
        target = (base / caminho).resolve()
        if not str(target).startswith(str(base)):
            return jsonify({"error": "Acesso negado"}), 403
        if not target.exists():
            return jsonify({"error": "Diretório não encontrado"}), 404
    else:
        target = base

    arquivos = []
    for item in sorted(target.iterdir()):
        if item.name.startswith('.'):
            continue
        if item.name == '__pycache__':
            continue
        if item.name.endswith('.pyc'):
            continue
        info = {
            "nome": item.name,
            "tipo": "pasta" if item.is_dir() else "arquivo",
            "tamanho": item.stat().st_size if item.is_file() else 0,
        }
        if item.is_file():
            ext = item.suffix.lower()
            if ext in ['.md', '.txt', '.py', '.html', '.css', '.js', '.json', '.bat', '.env']:
                info["editavel"] = True
            else:
                info["editavel"] = False
        arquivos.append(info)

    rel = target.relative_to(base)
    return jsonify({
        "arquivos": arquivos,
        "caminho_atual": str(rel) if rel != Path(".") else "",
        "pai": str(target.parent.relative_to(base)) if base in target.parent.parents else ""
    })


# ============================================
# API — LER ARQUIVO
# ============================================

@app.route('/api/arquivo/ler', methods=['POST'])
def api_ler_arquivo():
    """Lê conteúdo de um arquivo."""
    data = request.get_json()
    caminho = data.get('caminho', '')
    if not caminho:
        return jsonify({"error": "Caminho não informado"}), 400
    base = PROJECT_PATH
    target = (base / caminho).resolve()
    if not str(target).startswith(str(base)):
        return jsonify({"error": "Acesso negado"}), 403
    if not target.exists() or not target.is_file():
        return jsonify({"error": "Arquivo não encontrado"}), 404
    return jsonify({
        "sucesso": True,
        "conteudo": target.read_text(encoding='utf-8', errors='replace'),
        "nome": target.name
    })


# ============================================
# API — START (iniciar serviços remotamente)
# ============================================

@app.route('/api/start', methods=['POST'])
def api_start():
    """Inicia serviços do OPB (útil para celular)."""
    resultados = []
    try:
        p = subprocess.Popen(
            [sys.executable, str(PROJECT_PATH / "agents" / "telegram_bot" / "main.py")],
            cwd=str(PROJECT_PATH),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        resultados.append({"servico": "telegram_bot", "status": "ok", "pid": p.pid})
    except Exception as e:
        resultados.append({"servico": "telegram_bot", "status": "erro", "detalhe": str(e)})
    return jsonify({"servicos": resultados, "mensagem": "Sistema iniciado!"})


# ============================================
# API — PAINEL DE CONTROLE (PWA)
# ============================================

SERVICES = {
    "api": {"pid": None, "name": "API Server"},
    "bot": {"pid": None, "name": "Telegram Bot"}
}

@app.route('/api/servicos/status', methods=['GET'])
def api_servicos_status():
    """Status dos serviços do OPB."""
    api_ok = True

    bot_pid = None
    try:
        if sys.platform == 'win32':
            r = subprocess.run(['tasklist', '/FI', 'imagename eq python.exe'],
                               capture_output=True, text=True, encoding='utf-8', errors='replace')
            for line in r.stdout.split('\n'):
                if 'telegram_bot' in line.lower() or ('main.py' in line.lower() and 'telegram' in str(PROJECT_PATH)):
                    bot_pid = line.strip()
        else:
            r = subprocess.run(['pgrep', '-f', 'telegram_bot/main.py'],
                               capture_output=True, text=True)
            bot_pid = r.stdout.strip() if r.returncode == 0 else None
    except:
        pass

    return jsonify({
        "api": {"rodando": api_ok, "porta": PORT},
        "bot": {"rodando": bool(bot_pid), "pid": bot_pid or None},
        "projeto": str(PROJECT_PATH),
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/servicos/parar', methods=['POST'])
def api_servicos_parar():
    """Para serviços do OPB."""
    parados = []

    try:
        if sys.platform == 'win32':
            r = subprocess.run(['tasklist', '/FI', 'imagename eq python.exe'],
                               capture_output=True, text=True, encoding='utf-8', errors='replace')
            for line in r.stdout.split('\n'):
                if 'telegram_bot' in line.lower():
                    pid = line.split()[1].strip() if len(line.split()) > 1 else None
                    if pid:
                        subprocess.run(['taskkill', '/F', '/PID', pid],
                                       capture_output=True, text=True)
                        parados.append("bot")
        else:
            r = subprocess.run(['pkill', '-f', 'telegram_bot/main.py'],
                               capture_output=True, text=True)
            if r.returncode == 0:
                parados.append("bot")
    except:
        pass

    return jsonify({
        "sucesso": True,
        "parados": parados,
        "mensagem": "Serviços parados!" if parados else "Nenhum serviço rodando."
    })


@app.route('/api/agentes/executar', methods=['POST'])
def api_agentes_executar():
    """Executa um agente pelo nome."""
    data = request.get_json()
    agente = data.get('agente', '')
    args = data.get('args', [])

    AGENTES = {
        "radagast": "agents/radagast/radagast.py",
        "carrossel": "agents/carrossel/main.py",
        "text_generator": "agents/text_generator/main.py",
        "consumo": "agents/consumo/main.py",
        "capa_video": "agents/capa_video/main.py",
    }

    if agente not in AGENTES:
        return jsonify({"error": f"Agente '{agente}' não encontrado. Disponíveis: {list(AGENTES.keys())}", "sucesso": False}), 400

    path = AGENTES[agente]
    result = run_agent(path, args)

    if "error" in result:
        return jsonify({"error": result["error"], "sucesso": False}), result.get("code", 500)

    return jsonify({
        "sucesso": result["success"],
        "stdout": result["stdout"][:3000] if result["stdout"] else "",
        "stderr": result["stderr"][:1000] if result["stderr"] else "",
        "agente": agente,
        "mensagem": f"✅ {agente} executado com sucesso!" if result["success"] else f"❌ {agente} falhou."
    })


@app.route('/api/servicos/reiniciar', methods=['POST'])
def api_servicos_reiniciar():
    """Reinicia serviços: para bot + inicia novamente."""
    try:
        if sys.platform == 'win32':
            r = subprocess.run(['tasklist', '/FI', 'imagename eq python.exe'],
                               capture_output=True, text=True, encoding='utf-8', errors='replace')
            for line in r.stdout.split('\n'):
                if 'telegram_bot' in line.lower():
                    pid = line.split()[1].strip() if len(line.split()) > 1 else None
                    if pid:
                        subprocess.run(['taskkill', '/F', '/PID', pid],
                                       capture_output=True, text=True)
        else:
            subprocess.run(['pkill', '-f', 'telegram_bot/main.py'],
                           capture_output=True, text=True)
    except:
        pass

    import time
    time.sleep(1)
    try:
        p = subprocess.Popen(
            [sys.executable, str(PROJECT_PATH / "agents" / "telegram_bot" / "main.py")],
            cwd=str(PROJECT_PATH),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )
        return jsonify({"sucesso": True, "mensagem": "🔄 Serviços reiniciados!", "bot_pid": p.pid})
    except Exception as e:
        return jsonify({"error": str(e), "sucesso": False}), 500


# ============================================
# SERVIR ARQUIVOS ESTÁTICOS
# ============================================

@app.route('/<path:path>', methods=['GET'])
def serve_static(path):
    """Serve arquivos estáticos do frontend."""
    static_files = ['plataforma.html', 'landing.html', 'dashboard.html', 'auth.html', 'onboarding.html', 'favicon.ico', 'manifest.json', 'sw.js']
    if path in static_files or path.endswith(('.js', '.css', '.json', '.png', '.jpg', '.svg', '.ico')):
        filepath = FRONTEND_PATH / path
        if filepath.exists():
            return send_from_directory(str(FRONTEND_PATH), path)
    return serve_frontend()


# ============================================
# INICIALIZAÇÃO
# ============================================

# ============================================
# API — SALVAR PERFIL
# ============================================

@app.route('/api/save-profile', methods=['POST'])
def api_save_profile():
    """Salva conteúdo do perfil em arquivo .md"""
    data = request.get_json()
    modulo = data.get('modulo', '')
    content = data.get('content', '')
    filename = data.get('filename', '')

    if not filename:
        return jsonify({"error": "Nome do arquivo não informado"}), 400

    perfil_path = get_perfil_path() / filename

    try:
        perfil_path.write_text(content, encoding='utf-8')
        return jsonify({"sucesso": True, "mensagem": f"{filename} salvo com sucesso!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/load-profile', methods=['GET'])
def api_load_profile():
    """Carrega dados do perfil salvos"""
    perfil_dir = get_perfil_path()
    arquivos = {
        'basico': perfil_dir / "PERFIL.md",
        'habilidades': perfil_dir / "HABILIDADES.md",
        'historias': perfil_dir / "HISTORIAS.md",
        'cosmovisao': perfil_dir / "COSMOVISAO.md",
        'publico': perfil_dir / "PUBLICO-ALVO.md",
        'posicionamento': perfil_dir / "POSICIONAMENTO.md",
        'narrativa': perfil_dir / "NARRATIVA.md",
    }
    dados = {}
    for modulo, path in arquivos.items():
        if path.exists():
            content = path.read_text(encoding='utf-8')
            section = {}
            current_key = None
            for line in content.split('\n'):
                if line.startswith('## '):
                    current_key = line[3:].strip().lower()
                    section[current_key] = ''
                elif current_key and line.strip():
                    section[current_key] = (section.get(current_key, '') + line + '\n').strip()
            dados[modulo] = section
    return jsonify(dados)


@app.route('/api/inspiracoes', methods=['GET'])
def api_inspiracoes():
    """Retorna a lista de perfis de inspiração (influenciadores)"""
    insp_path = PROJECT_PATH / "agents" / "radagast" / "config" / "inspiracoes.json"
    if not insp_path.exists():
        return jsonify({"profiles": [], "erro": "Arquivo não encontrado"})
    try:
        data = json.loads(insp_path.read_text(encoding='utf-8'))
        return jsonify(data)
    except Exception as e:
        return jsonify({"profiles": [], "erro": str(e)})


# ============================================
# API — QUADRO DE AVISOS
# ============================================

QUADRO_PATH = PROJECT_PATH / "agents" / "quadro-de-avisos"

@app.route('/api/quadro-avisos', methods=['GET'])
def api_quadro_avisos_listar():
    """Lista tarefas do Quadro de Avisos."""
    agente = request.args.get('agente')
    try:
        sys.path.insert(0, str(QUADRO_PATH))
        from main import listar as q_listar
        tarefas = q_listar(agente)
        pendentes = len([t for t in tarefas if t["status"] == "pendente"])
        return jsonify({"tarefas": tarefas, "pendentes": pendentes})
    except Exception as e:
        return jsonify({"error": str(e), "tarefas": []}), 500

@app.route('/api/quadro-avisos', methods=['POST'])
def api_quadro_avisos_adicionar():
    """Adiciona tarefa ao Quadro de Avisos."""
    data = request.get_json()
    descricao = data.get('tarefa', data.get('descricao', ''))
    agente = data.get('agente', 'geral')
    prioridade = data.get('prioridade', 'media')
    if not descricao:
        return jsonify({"error": "Descrição da tarefa não informada"}), 400
    try:
        sys.path.insert(0, str(QUADRO_PATH))
        from main import adicionar as q_adicionar
        tarefa = q_adicionar(descricao, agente, prioridade)
        return jsonify({"sucesso": True, "tarefa": tarefa})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/quadro-avisos/<int:tarefa_id>/concluir', methods=['POST'])
def api_quadro_avisos_concluir(tarefa_id):
    """Conclui uma tarefa."""
    try:
        sys.path.insert(0, str(QUADRO_PATH))
        from main import concluir as q_concluir
        tarefa = q_concluir(tarefa_id)
        if tarefa:
            return jsonify({"sucesso": True, "tarefa": tarefa})
        return jsonify({"error": "Tarefa não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/quadro-avisos/<int:tarefa_id>', methods=['DELETE'])
def api_quadro_avisos_excluir(tarefa_id):
    """Exclui uma tarefa."""
    try:
        sys.path.insert(0, str(QUADRO_PATH))
        from main import excluir as q_excluir
        if q_excluir(tarefa_id):
            return jsonify({"sucesso": True})
        return jsonify({"error": "Tarefa não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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