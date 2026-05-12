import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_PATH = Path(__file__).parent.parent.parent
ACERVO_PATH = PROJECT_PATH / "acervo" / "pesquisas"

sys.stdout.reconfigure(encoding='utf-8')

@dataclass
class Perfil:
    nome: str
    plataforma: str
    url: str
    nicho: str
    relevancia: int
    nota: str = ""
    seguidores: str = ""

def ensure_pastas():
    (ACERVO_PATH / "perfis").mkdir(parents=True, exist_ok=True)
    (ACERVO_PATH / "relatorios").mkdir(parents=True, exist_ok=True)
    
    index_path = ACERVO_PATH / "index.md"
    if not index_path.exists():
        index_path.write_text("""# Pesquisas de Posicionamento

> Perfis e concorrentes analisados

## Como usar

Execute o agente com palavras-chave:
```bash
python main.py "IA para empreendedores"
python main.py "automacao trabalho"
```

## Arquivos

- `perfis/` - Perfis cadastrados por pesquisa
- `relatorios/` - Relatórios gerados

---

_Last updated: AAAA-MM-DD_
""", encoding="utf-8")

def decodificar_url_bing(url: str) -> str:
    """Decodifica URL do Bing para obter URL real"""
    if "bing.com" in url.lower() and "&u=" in url:
        try:
            from urllib.parse import unquote, parse_qs, urlparse
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            if 'u' in params:
                return params['u'][0]
        except:
            pass
    return url

def identificar_plataforma(url: str) -> str:
    url = decodificar_url_bing(url)
    url_lower = url.lower()
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "YouTube"
    elif "instagram.com" in url_lower:
        return "Instagram"
    elif "threads.net" in url_lower or "threads.com" in url_lower:
        return "Threads"
    elif "twitter.com" in url_lower or "x.com" in url_lower:
        return "Twitter/X"
    elif "linkedin.com" in url_lower:
        return "LinkedIn"
    elif "tiktok.com" in url_lower:
        return "TikTok"
    return "Website"

def calcular_relevancia(titulo: str, descricao: str, nicho: str) -> int:
    texto = (titulo + " " + descricao).lower()
    palavras = [p.strip().lower() for p in nicho.split() if len(p.strip()) > 2]
    
    pontos = sum(1 for p in palavras if p in texto)
    
    if pontos >= 4: return 5
    elif pontos >= 3: return 4
    elif pontos >= 2: return 3
    elif pontos >= 1: return 2
    return 1

def pesquisar_ddg(query: str, num_resultados: int = 15) -> List[dict]:
    """Pesquisa no DuckDuckGo via API HTML"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        url = f"https://html.duckduckgo.com/html/?q={query}"
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            resultados = []
            for result in soup.select('.result__body')[:num_resultados]:
                link = result.select_one('.result__url')
                title = result.select_one('.result__a')
                snippet = result.select_one('.result__snippet')
                
                if link and title:
                    href = link.get('href', '')
                    if href:
                        href = href.replace('//duckduckgo.com/l/?uddg=', '')
                        href = href.split('&')[0]
                    
                    resultados.append({
                        'url': href or link.get('text', ''),
                        'titulo': title.get_text(strip=True),
                        'descricao': snippet.get_text(strip=True) if snippet else ''
                    })
            
            return resultados
    except Exception as e:
        logger.warning(f"Erro DuckDuckGo: {e}")
    
    return []

def pesquisar_bing(query: str, num_resultados: int = 15) -> List[dict]:
    """Pesquisa no Bing (sem API key)"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        url = f"https://www.bing.com/search?q={query}&count={num_resultados}"
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            resultados = []
            for item in soup.select('li.b_algo')[:num_resultados]:
                link = item.select_one('a')
                snippet = item.select_one('p')
                
                if link:
                    resultados.append({
                        'url': link.get('href', ''),
                        'titulo': link.get_text(strip=True),
                        'descricao': snippet.get_text(strip=True) if snippet else ''
                    })
            
            return resultados
    except Exception as e:
        logger.warning(f"Erro Bing: {e}")
    
    return []

def pesquisar_google_via_serp(query: str, num_resultados: int = 15) -> List[dict]:
    """Fallback: pesquisa via Google sem API"""
    # Tentar múltiplas fontes
    resultados = pesquisar_ddg(query, num_resultados)
    if resultados:
        return resultados
    
    return pesquisar_bing(query, num_resultados)

def salvar_perfil(perfil: Perfil, pesquisa: str) -> str:
    ensure_pastas()
    
    # Sanitizar nome de arquivo
    nome_seguro = "".join(c for c in perfil.nome if c.isalnum() or c in "-_").strip()[:30]
    if not nome_seguro:
        nome_seguro = "perfil"
    filename = f"{pesquisa.replace(' ', '_')}_{nome_seguro}.md"
    filepath = ACERVO_PATH / "perfis" / filename
    
    conteudo = f"""---
name: "{perfil.nome}"
plataforma: {perfil.plataforma}
url: {perfil.url}
nicho: {perfil.nicho}
relevancia: {perfil.relevancia}
pesquisa: {pesquisa}
updated_at: {datetime.now().strftime("%Y-%m-%d")}
---

# {perfil.nome}

| Campo | Valor |
|-------|-------|
| **Plataforma** | {perfil.plataforma} |
| **URL** | {perfil.url} |
| **Nicho** | {perfil.nicho} |
| **Relevancia** | {"*" * perfil.relevancia} ({perfil.relevancia}/5) |

## Analise

{perfil.nota or "_Adicione sua analise aqui_"}

## Proximos passos

- [ ] Analisar conteudo
- [ ] Verificar engajamento
- [ ] Contatar para parceria

---

*Pesquisado em: {datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""
    filepath.write_text(conteudo, encoding='utf-8')
    return filename

def gerar_relatorio(pesquisa: str, perfis: List[Perfil]) -> str:
    ensure_pastas()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"relatorio_{pesquisa.replace(' ', '_')}_{timestamp}.md"
    filepath = ACERVO_PATH / "relatorios" / filename
    
    conteudo = f"""---
name: "Relatorio: {pesquisa}"
tipo: relatorio
pesquisa: {pesquisa}
total_encontrados: {len(perfis)}
updated_at: {datetime.now().strftime("%Y-%m-%d")}
---

# Relatorio de Posicionamento

> Pesquisa: **{pesquisa}**
> Data: {datetime.now().strftime("%Y-%m-%d")}

## Resumo

| Metrica | Valor |
|---------|-------|
| Total encontrados | {len(perfis)} |
| Alta relevancia | {len([p for p in perfis if p.relevancia >= 4])} |

## Perfis por Plataforma

"""
    
    por_plataforma = {}
    for p in perfis:
        por_plataforma.setdefault(p.plataforma, []).append(p)
    
    for plataforma, lista in por_plataforma.items():
        conteudo += f"### {plataforma}\n\n"
        for p in sorted(lista, key=lambda x: x.relevancia, reverse=True):
            conteudo += f"- [{p.nome}]({p.url}) {'*' * p.relevancia}\n"
        conteudo += "\n"
    
    conteudo += """## Proximos Passos

1. Analisar perfis de alta relevancia
2. Avaliar engajamento
3. Identificar parcerias

---
"""
    
    filepath.write_text(conteudo, encoding='utf-8')
    return filename

def executar_pesquisa(pesquisa: str) -> List[Perfil]:
    print(f"[Busca] Pesquisando: {pesquisa}")
    
    # Procurar perfis específicos por plataforma
    buscas = [
        f"site:youtube.com {pesquisa} influencer",
        f"site:instagram.com {pesquisa} perfil",
        f"site:threads.net {pesquisa} perfil"
    ]
    
    resultados = []
    for busca in buscas:
        r = pesquisar_google_via_serp(busca, 10)
        resultados.extend(r)
        if len(resultados) >= 15:
            break
    
    # Se não encontrou, buscar geral
    if not resultados:
        resultados = pesquisar_google_via_serp(pesquisa, 15)
    
    print(f"   -> {len(resultados)} resultados")
    
    perfis = []
    urls_seen = set()
    
    for r in resultados:
        url = r.get("url", "")
        if not url or url in urls_seen:
            continue
        urls_seen.add(url)
        
        relevancia = calcular_relevancia(r.get("titulo", ""), r.get("descricao", ""), pesquisa)
        
        # Extrair nome do URL
        nome = url.split('/')[-1].replace('@', '').replace('-', ' ').title()[:50]
        if not nome or nome.startswith('http'):
            nome = r.get("titulo", "Perfil")[:50]
        
        plataforma = identificar_plataforma(url)
        
        perfil = Perfil(
            nome=nome,
            plataforma=plataforma,
            url=url,
            nicho=pesquisa,
            relevancia=relevancia,
            nota=r.get("descricao", "")
        )
        
        salvar_perfil(perfil, pesquisa)
        perfis.append(perfil)
    
    if perfis:
        gerar_relatorio(pesquisa, perfis)
    
    return perfis

def main():
    ensure_pastas()
    
    # Verificar dependências
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("ERRO: beautifulsoup4 nao instalado")
        print("Instale com: pip install beautifulsoup4")
        return
    
    if len(sys.argv) < 2:
        print("""
Agente Posicionamento - Pesquisa de Perfis

USO:
  python main.py "palavra-chave"
  python main.py add "Nome" "URL" "nicho" [relevancia]
  python main.py --listar
  python main.py --perfis [nicho]

EXEMPLOS:
  python main.py "IA para negocios"
  python main.py "automacao produtividade"
  python main.py add "Canal Tech" "https://youtube.com/@canal" "IA" 4
""")
        return
    
    arg1 = sys.argv[1]
    
    if arg1 == "add" and len(sys.argv) >= 5:
        nome, url, nicho = sys.argv[2], sys.argv[3], sys.argv[4]
        relevancia = int(sys.argv[5]) if len(sys.argv) > 5 else 3
        
        perfil = Perfil(nome=nome, plataforma=identificar_plataforma(url),
                       url=url, nicho=nicho, relevancia=relevancia)
        salvar_perfil(perfil, nicho)
        print(f"Perfil adicionado: {nome}")
        return
    
    if arg1 == "--listar":
        relatorios = sorted((ACERVO_PATH / "relatorios").glob("*.md"), reverse=True)
        print(f"\nRelatorios ({len(relatorios)}):\n")
        for r in relatorios:
            print(f"  - {r.stem}")
        return
    
    if arg1 == "--perfis" and len(sys.argv) > 2:
        nicho = sys.argv[2]
        perfis = list((ACERVO_PATH / "perfis").glob(f"{nicho}*.md"))
        print(f"\nPerfis ({len(perfis)}):\n")
        for p in perfis:
            print(f"  - {p.stem}")
        return
    
    # Pesquisa
    pesquisa = arg1
    perfis = executar_pesquisa(pesquisa)
    
    print(f"\nConcluido!")
    print(f"   -> {len(perfis)} perfis encontrados")
    print(f"   -> Alta relevancia: {len([p for p in perfis if p.relevancia >= 4])}")

if __name__ == "__main__":
    main()