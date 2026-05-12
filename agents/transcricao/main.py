import os
import sys
import re
import logging
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs

sys.stdout.reconfigure(encoding='utf-8')

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    YTTA_AVAILABLE = True
except ImportError:
    YTTA_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_PATH = Path(__file__).parent.parent.parent
ACERVO_PATH = PROJECT_PATH / "acervo" / "transcricoes"

def ensure_pastas():
    ACERVO_PATH.mkdir(parents=True, exist_ok=True)
    
    index_path = ACERVO_PATH / "index.md"
    if not index_path.exists():
        index_path.write_text("""# Transcricoes de Videos

> Transcrições de vídeos do YouTube

## Como usar

```bash
python main.py "URL_DO_VIDEO"
python main.py --listar
python main.py --ler "nome-do-video"
python main.py --buscar "palavra-chave"
```

## Arquivos

- Transcrições salvas como markdown

---

_Last updated: AAAA-MM-DD_
""", encoding="utf-8")

def extrair_video_id(url: str) -> str:
    """Extrai o ID do vídeo de várias URL formats do YouTube"""
    # youtube.com/watch?v=ID
    # youtu.be/ID
    # youtube.com/embed/ID
    # youtube.com/v/ID
    
    parsed = urlparse(url)
    
    if "youtu.be" in url:
        return parsed.path[1:] if parsed.path else ""
    
    if parsed.hostname in ["www.youtube.com", "youtube.com", "m.youtube.com"]:
        if parsed.path == "/watch":
            params = parse_qs(parsed.query)
            return params.get("v", [""])[0]
        elif parsed.path.startswith("/embed/"):
            return parsed.path.split("/")[-1]
        elif parsed.path.startswith("/v/"):
            return parsed.path.split("/")[-1]
    
    return ""

def formatar_tempo(segundos: float) -> str:
    """Converte segundos para formato HH:MM:SS"""
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    seg = int(segundos % 60)
    
    if horas > 0:
        return f"{horas:02d}:{minutos:02d}:{seg:02d}"
    return f"{minutos:02d}:{seg:02d}"

def obter_titulo_video(video_id: str) -> str:
    """Tenta obter o título do vídeo (se disponível)"""
    # Não temos API para título sem API key, então usamos o ID
    return f"Video {video_id}"

def transcrever_video(url: str, idioma: str = "pt") -> dict:
    """Transcreve um vídeo do YouTube"""
    if not YTTA_AVAILABLE:
        return {"erro": "youtube-transcript-api nao instalado"}
    
    video_id = extrair_video_id(url)
    if not video_id:
        return {"erro": "URL invalida ou nao e um video do YouTube"}
    
    print(f"[Video] ID: {video_id}")
    print(f"[Idioma] {idioma}")
    
    try:
        ytta = YouTubeTranscriptApi()
        transcripts = ytta.list(video_id)
        
        # Tentar encontrar transcript no idioma preferido
        transcript_obj = None
        try:
            transcript_obj = transcripts.find_transcript([idioma, 'pt-BR', 'pt', 'en'])
        except:
            pass
        
        # Se não encontrou, pegar o primeiro disponível
        if not transcript_obj:
            for t in transcripts._transcripts:
                transcript_obj = t
                break
        
        if not transcript_obj:
            return {"erro": "Nenhuma transcript disponivel"}
        
        # Fetch da transcript
        transcript_data = transcript_obj.fetch()
        
        texto_completo = []
        for item in transcript_data:
            tempo = formatar_tempo(item.start)
            texto_completo.append(f"[{tempo}] {item.text}")
        
        return {
            "video_id": video_id,
            "url": url,
            "idioma": transcript_obj.language_code,
            "transcricao": texto_completo,
            "duracao": max(item.start + item.duration for item in transcript_data) if transcript_data else 0
        }
        
    except Exception as e:
        return {"erro": str(e)}

def salvar_transcricao(dados: dict) -> str:
    """Salva a transcrição em um arquivo markdown"""
    video_id = dados.get("video_id", "desconhecido")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Criar nome de arquivo amigável
    nome_seguro = f"{video_id}_{timestamp[:8]}"
    filepath = ACERVO_PATH / f"{nome_seguro}.md"
    
    duracao = dados.get("duracao", 0)
    minutos = int(duracao // 60)
    
    conteudo = f"""---
name: "Transcricao {video_id}"
tipo: transcricao
video_id: {video_id}
url: {dados.get("url", "")}
idioma: {dados.get("idioma", "pt")}
duracao: {minutos} minutos
data: {datetime.now().strftime("%Y-%m-%d")}
updated_at: {datetime.now().strftime("%Y-%m-%d")}
---

# Transcricao de Video

| Campo | Valor |
|-------|-------|
| **Video ID** | {video_id} |
| **URL** | {dados.get("url", "")} |
| **Idioma** | {dados.get("idioma", "pt")} |
| **Duracao** | ~{minutos} minutos |
| **Data** | {datetime.now().strftime("%Y-%m-%d %H:%M")} |

---

## Transcricao

"""
    
    for linha in dados.get("transcricao", []):
        conteudo += linha + "\n"
    
    conteudo += """

---

*Transcrito automaticamente pelo Agente Transcricao*
"""
    
    filepath.write_text(conteudo, encoding='utf-8')
    logger.info(f"Transcricao salva: {filepath.name}")
    return filepath.name

def listar_transcricoes():
    """Lista todas as transcrições salvas"""
    ensure_pastas()
    arquivos = sorted(ACERVO_PATH.glob("*.md"), reverse=True)
    
    print(f"\n[{len(arquivos)} transcricoes]\n")
    for a in arquivos:
        print(f"  - {a.stem}")
    return arquivos

def ler_transcricao(nome: str):
    """Lê uma transcrição específica"""
    ensure_pastas()
    caminho = ACERVO_PATH / f"{nome}.md"
    
    if not caminho.exists():
        # Tentar encontrar por parte do nome
        arquivos = list(ACERVO_PATH.glob(f"*{nome}*.md"))
        if arquivos:
            caminho = arquivos[0]
        else:
            print(f"Transcricao nao encontrada: {nome}")
            return
    
    print(caminho.read_text(encoding='utf-8'))

def buscar_em_transcricoes(palavra: str):
    """Busca uma palavra em todas as transcrições"""
    ensure_pastas()
    arquivos = list(ACERVO_PATH.glob("*.md"))
    
    palavra_lower = palavra.lower()
    resultados = []
    
    for a in arquivos:
        conteudo = a.read_text(encoding='utf-8').lower()
        if palavra_lower in conteudo:
            linhas = conteudo.split("\n")
            contexto = [l for l in linhas if palavra_lower in l][:3]
            resultados.append({
                "arquivo": a.stem,
                "ocorrencias": contexto
            })
    
    if resultados:
        print(f"\n[Encontrado em {len(resultados)} transcricoes]\n")
        for r in resultados:
            print(f"  {r['arquivo']}")
            for c in r['ocorrencias']:
                print(f"    > {c[:100]}...")
    else:
        print(f"Nenhuma ocorrencia de '{palavra}'")

def main():
    ensure_pastas()
    
    if not YTTA_AVAILABLE:
        print("ERRO: youtube-transcript-api nao instalado")
        print("Instale com: pip install youtube-transcript-api")
        return
    
    if len(sys.argv) < 2:
        print("""
Agente Transcricao - YouTube

USO:
  python main.py "URL_DO_VIDEO"
  python main.py --listar
  python main.py --ler "nome"
  python main.py --buscar "palavra"

EXEMPLOS:
  python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  python main.py "https://youtu.be/dQw4w9WgXcQ"
  python main.py --listar
  python main.py --buscar "IA"
""")
        return
    
    arg1 = sys.argv[1]
    
    if arg1.startswith("http"):
        # URL do vídeo
        url = arg1
        
        # Verificar idioma
        idioma = "pt"
        if len(sys.argv) > 2:
            idioma = sys.argv[2]
        
        print(f"[Transcrevendo] {url}")
        
        resultado = transcrever_video(url, idioma)
        
        if "erro" in resultado:
            print(f"ERRO: {resultado['erro']}")
            return
        
        # Salvar
        arquivo = salvar_transcricao(resultado)
        
        duracao = resultado.get("duracao", 0)
        linhas = len(resultado.get("transcricao", []))
        
        print(f"\n[SUCESSO]")
        print(f"   -> Arquivo: {arquivo}")
        print(f"   -> Duracao: ~{int(duracao//60)} minutos")
        print(f"   -> Linhas: {linhas}")
        
        return
    
    if arg1 == "--listar":
        listar_transcricoes()
        return
    
    if arg1 == "--ler" and len(sys.argv) > 2:
        ler_transcricao(sys.argv[2])
        return
    
    if arg1 == "--buscar" and len(sys.argv) > 2:
        buscar_em_transcricoes(sys.argv[2])
        return
    
    print(f"Comando desconhecido: {arg1}")

if __name__ == "__main__":
    main()