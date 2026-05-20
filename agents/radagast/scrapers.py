import json
import logging
import os
import urllib.parse
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger("radagast.scrapers")

try:
    import feedparser
except ImportError:
    feedparser = None


def _cutoff_date(days_back: int) -> str:
    return (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")


def _fetch_url(url: str, timeout: int = 15) -> str | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        logger.debug(f"Erro ao buscar {url[:60]}: {e}")
        return None


def _safe_int(val, default=0) -> int:
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


# =====================================================================
# YouTube
# =====================================================================

_CHANNEL_CACHE = {}


def _get_channel_id_from_url(url: str) -> str | None:
    """Obtém channel_id de uma URL do YouTube usando yt-dlp."""
    if url in _CHANNEL_CACHE:
        return _CHANNEL_CACHE[url]

    try:
        import yt_dlp
        with yt_dlp.YoutubeDL({"quiet": True, "extract_flat": True, "playlistend": 1}) as ydl:
            info = ydl.extract_info(url, download=False)
            if info:
                cid = info.get("channel_id") or info.get("uploader_id")
                if cid:
                    _CHANNEL_CACHE[url] = cid
                    return cid
    except Exception as e:
        logger.debug(f"yt-dlp channel_id para {url}: {e}")

    _CHANNEL_CACHE[url] = None
    return None


def _parse_youtube_rss(channel_id: str, days_back: int) -> list[dict]:
    """Parseia RSS feed de um canal YouTube."""
    results = []
    cutoff = _cutoff_date(days_back)
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

    xml_data = _fetch_url(rss_url)
    if not xml_data:
        return results

    try:
        root = ET.fromstring(xml_data)
        ATOM = "http://www.w3.org/2005/Atom"
        YT = "http://www.youtube.com/xml/schemas/2015"
        MEDIA = "http://search.yahoo.com/mrss/"
        ns = {"atom": ATOM, "yt": YT, "media": MEDIA}
        for entry in root.findall("atom:entry", ns):
            pub = entry.findtext("atom:published", "", ns)[:10]
            if pub and pub < cutoff:
                continue

            video_id = entry.findtext("yt:videoId", "", ns)
            title = entry.findtext("atom:title", "", ns)
            author_el = entry.find("atom:author", ns)
            author = ""
            if author_el is not None:
                author = author_el.findtext("atom:name", "", ns)
            link_el = entry.find("atom:link", ns)
            url = ""
            if link_el is not None:
                url = link_el.get("href", f"https://youtu.be/{video_id}")
            media_group = entry.find("media:group", ns)
            desc = ""
            if media_group is not None:
                desc_el = media_group.find("media:description", ns)
                if desc_el is not None:
                    desc = desc_el.text or ""

            results.append({
                "source": "youtube",
                "author": author,
                "title": title,
                "text": desc[:500],
                "url": url,
                "date": pub,
                "engagement": {},
                "language": "en",
            })
    except ET.ParseError as e:
        logger.warning(f"Erro ao parsear RSS YouTube: {e}")

    return results


def _search_youtube_ytdlp(term: str, days_back: int) -> list[dict]:
    """Busca vídeos no YouTube por termo usando yt-dlp."""
    results = []
    cutoff = _cutoff_date(days_back)

    try:
        import yt_dlp
        with yt_dlp.YoutubeDL({
            "quiet": True, "extract_flat": True,
            "dateafter": f"now-{days_back}days",
        }) as ydl:
            info = ydl.extract_info(f"ytsearch10:{term}", download=False)
            entries = info.get("entries", []) if info else []
            for data in entries:
                if not data:
                    continue
                pub = (data.get("upload_date") or "")[:10]
                if pub:
                    pub = f"{pub[:4]}-{pub[4:6]}-{pub[6:8]}"
                if pub and pub < cutoff:
                    continue

                results.append({
                    "source": "youtube",
                    "author": data.get("channel", data.get("uploader", "")),
                    "title": data.get("title", ""),
                    "text": data.get("description", "")[:500],
                    "url": data.get("webpage_url", data.get("url", "")),
                    "date": pub,
                    "engagement": {
                        "views": _safe_int(data.get("view_count")),
                        "likes": _safe_int(data.get("like_count")),
                    },
                    "language": "en",
                })
    except Exception as e:
        logger.debug(f"yt-dlp search '{term}' falhou: {e}")

    return results


def scrape_youtube(profiles: list[dict], search_terms: list[str],
                   days_back: int = 3) -> list[dict]:
    """Busca vídeos recentes via RSS (canais) e yt-dlp (keywords)."""
    results = []

    for term in search_terms[:5]:
        logger.info(f"  YT busca: '{term}'")
        results.extend(_search_youtube_ytdlp(term, days_back))

    for profile in profiles:
        yt_url = profile.get("platforms", {}).get("youtube")
        if not yt_url:
            continue
        channel_id = _get_channel_id_from_url(yt_url)
        if not channel_id:
            logger.warning(f"  YT canal {profile['name']}: não foi possível obter channel_id")
            continue
        logger.info(f"  YT RSS canal: {profile['name']}")
        results.extend(_parse_youtube_rss(channel_id, days_back))

    logger.info(f"  YT total: {len(results)} items")
    return results


# =====================================================================
# Instagram (via RSS alternativo - dumpor ou bibliogram)
# =====================================================================

def scrape_instagram(profiles: list[dict], days_back: int = 3) -> list[dict]:
    """Instagram está bloqueado para scraping gratuito. Retorna vazio."""
    logger.info("  IG: scraping gratuito indisponível (API bloqueada). Pule esta plataforma.")
    return []


# =====================================================================
# Twitter / X (via Nitter RSS, gratuito e sem API key)
# =====================================================================

_NITTER_INSTANCES = [
    "https://nitter.net",
    "https://nitter.lacontrevoie.fr",
    "https://nitter.uni-x.de",
]


def _try_nitter_rss(username: str, days_back: int) -> list[dict]:
    """Tenta buscar tweets de um perfil via RSS do Nitter."""
    results = []
    cutoff = _cutoff_date(days_back)

    for instance in _NITTER_INSTANCES:
        rss_url = f"{instance}/{username}/rss"
        xml_data = _fetch_url(rss_url)
        if not xml_data:
            continue

        try:
            root = ET.fromstring(xml_data)
            ATOM = "http://www.w3.org/2005/Atom"
            ns = {"atom": ATOM}
            for entry in root.findall("atom:entry", ns):
                pub = entry.findtext("atom:published", "", ns)[:10]
                if pub and pub < cutoff:
                    continue
                title = entry.findtext("atom:title", "", ns)
                link_el = entry.find("atom:link", ns)
                url = link_el.get("href", "") if link_el is not None else ""

                results.append({
                    "source": "twitter",
                    "author": username,
                    "title": "",
                    "text": title[:500],
                    "url": url,
                    "date": pub,
                    "engagement": {},
                    "language": "en",
                })
            if results:
                break
        except ET.ParseError:
            continue

    return results


def scrape_twitter(profiles: list[dict], search_terms: list[str],
                   days_back: int = 3) -> list[dict]:
    """Busca tweets via RSS do Nitter (gratuito)."""
    results = []

    for profile in profiles:
        tw_url = profile.get("platforms", {}).get("twitter")
        if not tw_url:
            continue
        username = tw_url.rstrip("/").split("/")[-1].lstrip("@")
        logger.info(f"  X RSS perfil: {profile['name']} (@{username})")
        results.extend(_try_nitter_rss(username, days_back))

    logger.info(f"  X total: {len(results)} items")
    return results


# =====================================================================
# LinkedIn (gratuito via RSS de blogs, sem scraping direto)
# =====================================================================

def scrape_linkedin(profiles: list[dict], days_back: int = 3) -> list[dict]:
    """LinkedIn não tem API gratuita. Retorna vazio."""
    logger.info("  LI: scraping gratuito indisponível. Pule esta plataforma.")
    return []


# =====================================================================
# Web / News (via Google News RSS, gratuito)
# =====================================================================

def scrape_web_news(search_terms: list[str], days_back: int = 3) -> list[dict]:
    """Busca notícias via Google News RSS."""
    results = []

    for term in search_terms[:3]:
        rss_url = (
            f"https://news.google.com/rss/search?q={urllib.parse.quote(term)}"
            f"&hl=en-US&gl=US&ceid=US:en"
        )
        logger.info(f"  Web RSS: '{term}'")
        xml_data = _fetch_url(rss_url)
        if not xml_data:
            continue

        try:
            root = ET.fromstring(xml_data)
            for item in root.iter("item"):
                title = item.findtext("title", "")
                link_el = item.find("link")
                url = link_el.text if link_el is not None else ""
                pub = item.findtext("pubDate", "")[:10]
                source = item.find("source")
                author = source.text if source is not None else ""

                results.append({
                    "source": "web",
                    "author": author,
                    "title": title,
                    "text": title[:500],
                    "url": url,
                    "date": pub,
                    "engagement": {},
                    "language": "en",
                })
        except ET.ParseError as e:
            logger.warning(f"  Web RSS '{term}' parse error: {e}")

    logger.info(f"  Web total: {len(results)} items")
    return results
