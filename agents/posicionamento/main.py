import os
import json
import logging
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_PATH = Path(__file__).parent.parent.parent
ACERVO_PATH = PROJECT_PATH / "acervo" / "pesquisas"

@dataclass
class Perfil:
    nome: str
    plataforma: str
    url: str
    nicho: str
    relevancia: int  # 1-5
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
python main.py "automação trabalho"
```

## Arquivos

- `perfis/` - Perfis cadastrados por pesquisa
- `relatorios/` - Relatórios gerados

---

_Last updated: AAAA-MM-DD_
""", encoding="utf-8")

def pesquisar_google(query: str, num_resultados: int = 10) -> List[dict]:
    """Pesquisa no Google (usandobing ou similar)"""
    try:
        url = "https://ddg-api.herokuapp.com/search"
        params = {"q": query, "num": num_resultados}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            results = response.json()
            return [
                {"titulo": r.get("title", ""), "url": r.get("url", ""), "descricao": r.get("snippet", "")}
                for r in results
            ]
    except Exception as e:
        logger.warning(f"Google API falhou: {e}")
    
    return []

def identificar_plataforma(url: str) -> str:
    url_lower = url.lower()
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "YouTube"
    elif "instagram.com" in url_lower:
        return "Instagram"
    elif "threads.net" in url_lower or "threads.com" in url_lower:
        return "Threads"
    elif "twitter.com" in url_lower:
        return "Twitter/X"
    elif "linkedin.com" in url_lower:
        return "LinkedIn"
    elif "tiktok.com" in url_lower:
        return "TikTok"
    return "Website"

def calcular_relevancia(titulo: str, descricao: str, nicho: str) -> int:
    """Calcula pontuação de relevância (1-5)"""
    texto = (titulo + " " + descricao).lower()
    palavras_nicho = [p.strip().lower() for p in nicho.split() if len(p.strip()) > 2]
    
    pontos = 0
    for palavra in palavras_nicho:
        if palavra in texto:
            pontos += 1
    
    if pontos >= 4:
        return 5
    elif pontos >= 3:
        return 4
    elif pontos >= 2:
        return 3
    elif pontos >= 1:
        return 2
    return 1

def salvar_perfil(perfil: Perfil, pesquisa: str) -> str:
    ensure_pastas()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_seguro = perfil.nome.replace(" ", "-")[:30]
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
| **Relevância** | {"⭐" * perfil.relevancia} |
| **Seguidores** | {perfil.seguidores or "Não verificado"} |

## Análise

{perfil.nota or "_Adicione sua análise aqui_"}

## Próximos passos

- [ ] Analisar conteúdo
- [ ] Verificar engajamento
- [ ] Contatar para parceria
- [ ] Monitorar

---

*Pesquisado em: {datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""
    filepath.write_text(conteudo, encoding="utf-8")
    logger.info(f"Perfil salvo: {filename}")
    return filename

def gerar_relatorio(pesquisa: str, perfis: List[Perfil]) -> str:
    ensure_pastas()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"relatorio_{pesquisa.replace(' ', '_')}_{timestamp}.md"
    filepath = ACERVO_PATH / "relatorios" / filename
    
    conteudo = f"""---
name: "Relatório: {pesquisa}"
tipo: relatorio
pesquisa: {pesquisa}
total_encontrados: {len(perfis)}
updated_at: {datetime.now().strftime("%Y-%m-%d")}
---

# Relatório de Posicionamento

> Pesquisa: **{pesquisa}**
> Data: {datetime.now().strftime("%Y-%m-%d")}

## Resumo

| Métrica | Valor |
|---------|-------|
| Total encontrados | {len(perfis)} |
| Alta relevância (4-5⭐) | {len([p for p in perfis if p.relevancia >= 4])} |
| Média relevância (3⭐) | {len([p for p in perfis if p.relevancia == 3])} |

## Perfis por Plataforma

"""
    
    por_plataforma = {}
    for p in perfis:
        if p.plataforma not in por_plataforma:
            por_plataforma[p.plataforma] = []
        por_plataforma[p.plataforma].append(p)
    
    for plataforma, lista in por_plataforma.items():
        conteudo += f"### {plataforma}\n\n"
        for p in sorted(lista, key=lambda x: x.relevancia, reverse=True):
            estrelas = "⭐" * p.relevancia
            conteudo += f"- [{p.nome}]({p.url}) {estrelas}\n"
        conteudo += "\n"
    
    conteudo += """## Próximos Passos

1. Analisar os perfis de alta relevância
2. Avaliar engajamento e qualidade do conteúdo
3. Identificar oportunidades de parceria
4. Mapear estratégias de conteúdo similares

---

*Relatório gerado automaticamente pelo Agente Posicionamento*
"""
    
    filepath.write_text(conteudo, encoding="utf-8")
    logger.info(f"Relatório salvo: {filename}")
    return filename

def executar_pesquisa(pesquisa: str) -> List[Perfil]:
    """Executa pesquisa para uma palavra-chave"""
    print(f"🔍 Pesquisando: {pesquisa}")
    
    resultados = pesquisar_google(pesquisa)
    print(f"   → {len(resultados)} resultados encontrados")
    
    perfis = []
    for r in resultados:
        url = r.get("url", "")
        if not url:
            continue
        
        plataforma = identificar_plataforma(url)
        relevancia = calcular_relevancia(
            r.get("titulo", ""), 
            r.get("descricao", ""), 
            pesquisa
        )
        
        perfil = Perfil(
            nome=r.get("titulo", "Sem nome")[:50],
            plataforma=plataforma,
            url=url,
            nicho=pesquisa,
            relevancia=relevancia,
            nota=r.get("descricao", "")[:200]
        )
        perfis.append(perfil)
        
        salvar_perfil(perfil, pesquisa)
    
    if perfis:
        gerar_relatorio(pesquisa, perfis)
    
    return perfis

def main():
    ensure_pastas()
    
    import sys
    
    if len(sys.argv) < 2:
        print("""
🧠 Agente Posicionamento - Pesquisa de Perfis

Uso:
    python main.py "palavra-chave 1"
    python main.py "IA para empreendedores" "automação"
    python main.py --listar
    python main.py --relatorio "nome-da-pesquisa"

Exemplos:
    python main.py "inteligência artificial negócios"
    python main.py "produtividade entrepreneur"
    python main.py "automação trabalho remoto"
""")
        return
    
    if sys.argv[1] == "--listar":
        ensure_pastas()
        relatorios = list((ACERVO_PATH / "relatorios").glob("*.md"))
        print(f"\n📊 Relatórios ({len(relatorios)}):\n")
        for r in sorted(relatorios, reverse=True):
            print(f"  • {r.stem}")
        return
    
    if sys.argv[1] == "--relatorio" and len(sys.argv) > 2:
        nome = sys.argv[2]
        caminho = ACERVO_PATH / "relatorios" / f"relatorio_{nome}.md"
        if caminho.exists():
            print(caminho.read_text(encoding="utf-8"))
        else:
            print(f"Relatório não encontrado: {nome}")
        return
    
    pesquisas = sys.argv[1:]
    for p in pesquisas:
        perfis = executar_pesquisa(p)
        print(f"\n✅ Pesquisa '{p}' concluída!")
        print(f"   📊 {len(perfis)} perfis encontrados")
        alta_relevancia = len([x for x in perfis if x.relevancia >= 4])
        print(f"   ⭐ {alta_relevancia} de alta relevância")

if __name__ == "__main__":
    main()