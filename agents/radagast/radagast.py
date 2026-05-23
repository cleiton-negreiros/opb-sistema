#!/usr/bin/env python3
"""radagast.py — Curadoria diaria de conteudo EN para Reels.

Versao publica OPB School: enxuta, sem dependencias do fellowship.
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, date
from pathlib import Path

from dotenv import load_dotenv

REPO_DIR = Path(__file__).parent
load_dotenv(REPO_DIR / ".env", override=True)

load_dotenv()  # fallback: tenta .env do diretório atual

from scrapers import scrape_youtube, scrape_instagram, scrape_twitter, scrape_linkedin, scrape_web_news
from analyzer import generate_reel_ideas
from formatter import format_telegram_message


AGENT_NAME = "Radagast"
STATE_FILE = REPO_DIR / ".state.json"
CONFIG_DIR = REPO_DIR / "config"
LOG_DIR = REPO_DIR / "logs"

LOG_DIR.mkdir(exist_ok=True)
log_file = LOG_DIR / f"radagast_{date.today().isoformat()}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("radagast")


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def load_config(name: str) -> dict:
    path = CONFIG_DIR / name
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def deduplicate(items: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    for item in items:
        url = item.get("url", "")
        if url and url in seen:
            continue
        if url:
            seen.add(url)
        unique.append(item)
    return unique


def check_required_env() -> list[str]:
    """Retorna lista de variaveis obrigatorias que faltam no .env."""
    required = ["RADAGAST_BOT_TOKEN", "RADAGAST_CHAT_ID"]
    missing = [k for k in required if not os.environ.get(k, "").strip()]
    return missing


def check_config_files() -> list[str]:
    """Retorna lista de arquivos de config que faltam ou estao vazios."""
    issues = []
    inspiracoes = CONFIG_DIR / "inspiracoes.json"
    keywords = CONFIG_DIR / "keywords.json"

    if not inspiracoes.exists():
        issues.append(
            "config/inspiracoes.json nao existe. Copie config/inspiracoes.example.json "
            "para config/inspiracoes.json e preencha com seus perfis EN."
        )
    else:
        try:
            data = json.loads(inspiracoes.read_text(encoding="utf-8"))
            profiles = data.get("profiles", [])
            if not profiles:
                issues.append(
                    "config/inspiracoes.json esta vazio. Adicione ao menos 1 perfil "
                    "(ver exemplo comentado em config/inspiracoes.example.json)."
                )
        except json.JSONDecodeError as e:
            issues.append(f"config/inspiracoes.json invalido: {e}")

    if not keywords.exists():
        issues.append(
            "config/keywords.json nao existe. Copie config/keywords.example.json "
            "para config/keywords.json e preencha com seus termos de busca."
        )
    else:
        try:
            data = json.loads(keywords.read_text(encoding="utf-8"))
            terms = data.get("search_terms", [])
            if not terms:
                issues.append(
                    "config/keywords.json esta vazio. Adicione ao menos 1 termo de busca."
                )
        except json.JSONDecodeError as e:
            issues.append(f"config/keywords.json invalido: {e}")

    return issues


def send_telegram_messages(messages: list[str]) -> None:
    """Envia mensagens pro bot Telegram do aluno."""
    import requests

    bot_token = os.environ.get("RADAGAST_BOT_TOKEN", "").strip() or os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("RADAGAST_CHAT_ID", "").strip()
    if not bot_token or not chat_id:
        logger.error(
            "RADAGAST_BOT_TOKEN ou RADAGAST_CHAT_ID nao configurado no .env. "
            "Veja docs/manual.pdf paginas 3-4 para configurar."
        )
        raise RuntimeError("Telegram nao configurado")

    for msg in messages:
        for attempt in range(3):
            try:
                resp = requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": msg,
                        "parse_mode": "HTML",
                        "disable_web_page_preview": True,
                    },
                    timeout=30,
                )
                resp.raise_for_status()
                break
            except Exception as e:
                logger.warning(f"Telegram tentativa {attempt+1}/3 falhou: {e}")
                if attempt == 2:
                    logger.error("Erro ao enviar Telegram apos 3 tentativas")


def run_check() -> int:
    """Valida configuracao sem rodar curadoria. Retorna exit code."""
    print("=" * 60)
    print("Radagast - Verificacao de configuracao")
    print("=" * 60)

    missing_env = check_required_env()
    if missing_env:
        print("\n[ERRO] Variaveis obrigatorias faltando no .env:")
        for k in missing_env:
            print(f"  - {k}")
        print("\nAbra o arquivo .env (na raiz do projeto) e preencha esses valores.")
        print("Veja o passo a passo no docs/manual.pdf.")
        return 1
    print("\n[OK] Todas as variaveis obrigatorias do .env estao preenchidas.")

    config_issues = check_config_files()
    if config_issues:
        print("\n[ERRO] Problemas nos arquivos de configuracao:")
        for issue in config_issues:
            print(f"  - {issue}")
        return 1
    print("[OK] Arquivos de configuracao validos.")

    print("\nTestando conexao com Telegram...")
    try:
        send_telegram_messages([
            "Radagast - teste de conexao. Se voce esta vendo isso, esta tudo configurado corretamente."
        ])
        print("[OK] Mensagem de teste enviada. Confira no seu Telegram.")
    except Exception as e:
        print(f"[ERRO] Telegram falhou: {e}")
        return 1

    print("\nTudo pronto. O Radagast vai rodar automaticamente no horario configurado.")
    print("Voce tambem pode disparar manualmente com /radagast-rodar-agora no Claude Code.")
    return 0


def run_discover(profiles: list[dict], search_terms: list[str]) -> None:
    """Busca perfis EN relevantes e envia sugestoes no Telegram."""
    logger.info("=" * 60)
    logger.info("RADAGAST - Modo Descoberta")
    logger.info("=" * 60)

    existing_names = {p["name"].lower() for p in profiles}

    suggestions = []
    yt_results = scrape_youtube([], search_terms[:3], days_back=7)
    tw_results = scrape_twitter([], search_terms[:3], days_back=7)

    seen_authors = set()
    for item in yt_results + tw_results:
        author = item.get("author", "").strip()
        if (
            author
            and author.lower() not in existing_names
            and author.lower() not in seen_authors
        ):
            seen_authors.add(author.lower())
            engagement = item.get("engagement", {})
            suggestions.append({
                "name": author,
                "source": item["source"],
                "sample": item.get("title") or item.get("text", "")[:100],
                "url": item.get("url", ""),
                "engagement": engagement,
            })

    suggestions.sort(
        key=lambda x: x.get("engagement", {}).get("views", 0)
        + x.get("engagement", {}).get("likes", 0) * 10,
        reverse=True,
    )
    suggestions = suggestions[:10]

    if not suggestions:
        send_telegram_messages([
            "Radagast - Modo descoberta: nenhum perfil novo encontrado para seus termos."
        ])
        return

    lines = [
        "<b>Radagast - Descoberta de Perfis</b>\n",
        f"Encontrei {len(suggestions)} perfis EN relevantes para seus termos:\n",
    ]
    for i, s in enumerate(suggestions, 1):
        eng_str = ""
        if s.get("engagement"):
            eng_str = " | ".join(
                f"{k}={v}" for k, v in s["engagement"].items() if v
            )
        lines.append(
            f"\n{i}. <b>{s['name']}</b> ({s['source']})\n"
            f"   {s['sample'][:80]}\n"
            f"   {eng_str}\n"
            f"   {s['url']}"
        )

    lines.append(
        "\n\n<i>Para adicionar um perfil, edite config/inspiracoes.json manualmente.</i>"
    )

    send_telegram_messages(["\n".join(lines)])
    logger.info(f"Enviadas {len(suggestions)} sugestoes no Telegram")


def run_curadoria(profiles: list[dict], search_terms: list[str],
                  days_back: int, dry_run: bool) -> None:
    """Fluxo principal: scrape -> analyze -> format -> enviar."""
    state = load_state()
    logger.info(f"Perfis: {len(profiles)} | Keywords: {len(search_terms)} | Dias: {days_back}")
    logger.info("=" * 60)

    all_contents = []
    platforms_ok = 0

    logger.info("--- KEYWORDS (primario) ---")
    try:
        yt = scrape_youtube([], search_terms, days_back)
        all_contents.extend(yt)
        if yt:
            platforms_ok += 1
    except Exception as e:
        logger.error(f"YouTube keywords falhou: {e}")

    # Twitter por keywords indisponivel gratuitamente (apenas por perfis)

    logger.info("--- PERFIS (complemento) ---")
    try:
        all_contents.extend(scrape_youtube(profiles, [], days_back))
    except Exception as e:
        logger.error(f"YouTube perfis falhou: {e}")

    try:
        ig = scrape_instagram(profiles, days_back)
        all_contents.extend(ig)
        if ig:
            platforms_ok += 1
    except Exception as e:
        logger.error(f"Instagram falhou: {e}")

    try:
        all_contents.extend(scrape_twitter(profiles, [], days_back))
    except Exception as e:
        logger.error(f"Twitter perfis falhou: {e}")

    try:
        li = scrape_linkedin(profiles, days_back)
        all_contents.extend(li)
        if li:
            platforms_ok += 1
    except Exception as e:
        logger.error(f"LinkedIn falhou: {e}")

    try:
        web = scrape_web_news(search_terms, days_back)
        all_contents.extend(web)
        if web:
            platforms_ok += 1
    except Exception as e:
        logger.error(f"Web news falhou: {e}")

    all_contents = deduplicate(all_contents)
    logger.info(f"Total coletado (deduplicado): {len(all_contents)} items de {platforms_ok} plataformas")

    if dry_run:
        logger.info("--- DRY RUN - conteudos coletados ---")
        for i, c in enumerate(all_contents[:20], 1):
            logger.info(f"  {i}. [{c['source']}] {c['author']}: {c.get('title') or c['text'][:80]}")
        logger.info(f"Total: {len(all_contents)} items. Nenhuma ideia gerada (dry-run).")
        return

    if not all_contents:
        send_telegram_messages([
            "<b>Radagast</b>\nNenhum conteudo coletado hoje. Pode ter sido instabilidade dos scrapers ou seus termos nao retornaram resultados recentes."
        ])
        return

    logger.info("--- GERANDO IDEIAS ---")
    try:
        ideas = []
        for c in all_contents[:8]:
            ideas.append({
                "titulo": c.get("title") or c.get("text", "")[:80],
                "hook": c.get("text", "")[:120],
                "pontos": [f"Fonte: {c.get('author', 'desconhecido')}"],
                "fonte_url": c.get("url", ""),
                "fonte_autor": c.get("author", ""),
                "angulo_br": "Adaptar para o contexto brasileiro de financas com fe catolica",
                "formato_sugerido": "talking head"
            })
        logger.info(f"Geradas {len(ideas)} ideias a partir dos {len(all_contents)} itens coletados")
    except Exception as e:
        send_telegram_messages([f"<b>Radagast</b>\nFalha ao gerar ideias: {e}"])
        return

    if not ideas:
        send_telegram_messages([
            "<b>Radagast</b>\nNenhuma ideia gerada. O Claude retornou resposta vazia ou houve erro de parse."
        ])
        return

    stats = {"total_items": len(all_contents), "platforms": platforms_ok}
    messages = format_telegram_message(ideas, stats)
    send_telegram_messages(messages)

    state["last_run"] = datetime.now().isoformat()
    state.setdefault("stats", {})
    state["stats"]["last_ideas"] = len(ideas)
    state["stats"]["last_items"] = len(all_contents)
    state["stats"]["last_platforms"] = platforms_ok

    processed = state.get("processed_urls", [])
    new_urls = [c["url"] for c in all_contents if c.get("url")]
    processed = list(set(processed + new_urls))[-500:]
    state["processed_urls"] = processed

    # Salva ideias em disco
    ideas_dir = Path(__file__).parent.parent.parent / "acervo" / "ideias"
    ideas_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ideas_content = f"""# Ideias Geradas pelo Radagast — {datetime.now().strftime('%d/%m/%Y %H:%M')}

> Geradas a partir de {len(all_contents)} itens coletados de {platforms_ok} plataformas.

"""
    for i, idea in enumerate(ideas, 1):
        ideas_content += f"""## {i}. {idea.get('titulo', 'Ideia')}

**Hook:** {idea.get('hook', '')}
**Fonte:** {idea.get('fonte_autor', 'desconhecido')}
**URL:** {idea.get('fonte_url', '')}
**Ângulo:** {idea.get('angulo_br', '')}
**Formato:** {idea.get('formato_sugerido', 'reels')}
**Pontos-chave:** {', '.join(idea.get('pontos', []))}

---
"""
    idea_file = ideas_dir / f"radagast_{timestamp}.md"
    idea_file.write_text(ideas_content.strip(), encoding='utf-8')
    logger.info(f"Ideias salvas em: {idea_file}")

    save_state(state)
    logger.info(f"Sucesso: {len(ideas)} ideias de Reels geradas e enviadas no Telegram.")


def main():
    parser = argparse.ArgumentParser(description="Radagast - Curadoria de conteudo EN para Reels")
    parser.add_argument("--check", action="store_true", help="Valida .env e configs, sem rodar curadoria")
    parser.add_argument("--dry-run", action="store_true", help="Coleta conteudo mas nao gera ideias")
    parser.add_argument("--discover", action="store_true", help="Busca novos perfis de inspiracao")
    parser.add_argument("--days-back", type=int, default=None, help="Dias de historico (default: RADAGAST_SCAN_DAYS ou 3)")
    args = parser.parse_args()

    if args.check:
        sys.exit(run_check())

    missing_env = check_required_env()
    if missing_env:
        logger.error(
            f"Variaveis obrigatorias faltando no .env: {', '.join(missing_env)}. "
            f"Rode 'python3 radagast.py --check' para diagnostico."
        )
        sys.exit(1)

    config_issues = check_config_files()
    if config_issues:
        for issue in config_issues:
            logger.error(issue)
        sys.exit(1)

    days_back = args.days_back or int(os.environ.get("RADAGAST_SCAN_DAYS", "3"))
    inspiracoes = load_config("inspiracoes.json")
    keywords = load_config("keywords.json")
    profiles = inspiracoes.get("profiles", [])
    search_terms = keywords.get("search_terms", [])

    logger.info("=" * 60)
    logger.info(f"RADAGAST - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    logger.info("=" * 60)

    if args.discover:
        run_discover(profiles, search_terms)
    else:
        run_curadoria(profiles, search_terms, days_back, args.dry_run)


if __name__ == "__main__":
    main()
