"""
Notion Integration - OPB Sistema
Integracao entre o OPB Sistema e Notion via API.

Uso:
    python utils/notion_integration.py config --token ntn_... --database-id ...
    python utils/notion_integration.py sync "Titulo" "Conteudo" --tipo ideia
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_PATH = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_PATH / "config" / "notion.json"


def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
    return {}


def save_config(config):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding='utf-8')


def save_local(titulo, conteudo, tipo):
    saida_dir = PROJECT_PATH / "acervo" / "notion"
    saida_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{tipo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = saida_dir / filename
    content = f"""# {titulo}

{conteudo}

---
*Criado via OPB Sistema em {datetime.now().isoformat()}*
*Tipo: {tipo}*
"""
    filepath.write_text(content.strip(), encoding='utf-8')
    print(f"Salvo localmente: {filepath}")
    return filepath


def sync_to_notion(titulo, conteudo, tipo="ideia"):
    config = load_config()
    token = config.get("token")
    database_id = config.get("database_id")

    if not token:
        print("Notion token nao configurado.")
        print("Use: python utils/notion_integration.py config --token ntn_...")
        filepath = save_local(titulo, conteudo, tipo)
        return {"sucesso": False, "local": str(filepath), "mensagem": "Salvo localmente (Notion nao configurado)"}

    try:
        import requests
    except ImportError:
        print("requests nao instalado. Instale com: pip install requests")
        filepath = save_local(titulo, conteudo, tipo)
        return {"sucesso": False, "local": str(filepath), "mensagem": "Salvo localmente (requests nao instalado)"}

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    children = []
    for line in conteudo.split('\n'):
        if line.strip():
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": line[:2000]}}]
                }
            })

    if not children:
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "(vazio)"}}]}
        })

    if database_id:
        data = {
            "parent": {"database_id": database_id},
            "properties": {
                "Name": {"title": [{"type": "text", "text": {"content": titulo[:100]}}]},
                "Tipo": {"select": {"name": tipo}},
                "Data": {"date": {"start": datetime.now().isoformat()[:10]}},
            },
            "children": children[:100]
        }
        url = "https://api.notion.com/v1/pages"
    else:
        data = {
            "parent": {"type": "workspace", "workspace": True},
            "properties": {
                "title": [{"type": "text", "text": {"content": titulo[:100]}}]
            },
            "children": children[:100]
        }
        url = "https://api.notion.com/v1/pages"

    try:
        resp = requests.post(url, headers=headers, json=data)
        if resp.status_code in (200, 201):
            print(f"Sincronizado com Notion: {titulo}")
            return {"sucesso": True, "mensagem": "Sincronizado com Notion"}
        else:
            print(f"Erro Notion API ({resp.status_code}): {resp.text}")
            filepath = save_local(titulo, conteudo, tipo)
            return {"sucesso": False, "local": str(filepath), "mensagem": f"Salvo localmente (erro API: {resp.status_code})"}
    except Exception as e:
        print(f"Erro ao conectar com Notion: {e}")
        filepath = save_local(titulo, conteudo, tipo)
        return {"sucesso": False, "local": str(filepath), "mensagem": f"Salvo localmente (erro: {e})"}


def main():
    parser = argparse.ArgumentParser(description="Integracao com Notion")
    subparsers = parser.add_subparsers(dest="command")

    config_parser = subparsers.add_parser("config", help="Configurar token do Notion")
    config_parser.add_argument("--token", help="Notion Internal Integration Token")
    config_parser.add_argument("--database-id", help="Database ID (opcional)")

    sync_parser = subparsers.add_parser("sync", help="Sincronizar conteudo com Notion")
    sync_parser.add_argument("titulo", help="Titulo do conteudo")
    sync_parser.add_argument("conteudo", help="Conteudo em texto")
    sync_parser.add_argument("--tipo", default="ideia", help="Tipo: ideia, resultado, transcricao")

    args = parser.parse_args()

    if args.command == "config":
        config = load_config()
        if args.token:
            config["token"] = args.token
        if args.database_id:
            config["database_id"] = args.database_id
        save_config(config)
        print("Configuracao salva em", CONFIG_PATH)
        return

    if args.command == "sync":
        result = sync_to_notion(args.titulo, args.conteudo, args.tipo)
        if result.get("sucesso"):
            print(result["mensagem"])
        else:
            print(result["mensagem"])
            if result.get("local"):
                print(f"Arquivo local: {result['local']}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
