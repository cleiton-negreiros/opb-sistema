#!/usr/bin/env python3
"""Gera snapshot HTML com dados embutidos para deploy sem API."""
import json
from pathlib import Path

BASE = Path(r"C:\Users\cleit\Desktop\opb-sistema")
OUT = BASE / "snapshot.html"
PROFILE_DIR = BASE / "cerebro" / "perfil-empreendedor-solo"
ACERVO = BASE / "acervo"

def ler(path):
    try: return path.read_text(encoding='utf-8')
    except: return ""

def secoes(content):
    s, k = {}, None
    for line in content.split('\n'):
        if line.startswith('## '):
            k = line[3:].strip().lower()
            s[k] = ''
        elif k and line.strip():
            s[k] = (s.get(k, '') + line + '\n').strip()
    return s

def perfil_json():
    d = {}
    for arquivo, chave in [
        ("PERFIL.md", "basico"), ("HABILIDADES.md", "habilidades"),
        ("HISTORIAS.md", "historias"), ("COSMOVISAO.md", "cosmovisao"),
        ("PUBLICO-ALVO.md", "publico"), ("POSICIONAMENTO.md", "posicionamento"),
        ("NARRATIVA.md", "narrativa"),
    ]:
        c = ler(PROFILE_DIR / arquivo)
        if c: d[chave] = secoes(c)
    return json.dumps(d, ensure_ascii=False)

def resultados():
    items = []
    for pasta, tag in [("carrossel","carrossel"), ("conhecimento","consumo"), ("capas","capa-video")]:
        p = ACERVO / pasta
        if not p.exists(): continue
        for f in sorted(p.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True):
            if f.name == "index.md": continue
            c = ler(f)
            items.append({"id":abs(hash(str(f))), "texto":c[:3000], "tag":tag, "data":f.stem[-15:].replace("_"," ")})
    return json.dumps(items[:50], ensure_ascii=False)

def ideias():
    items = []
    p = ACERVO / "ideias"
    if p.exists():
        for f in sorted(p.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True):
            if f.name == "index.md": continue
            items.append({"titulo":ler(f).strip().split('\n')[0].replace('#','').strip(), "data":f.stem[:16].replace("_"," ")})
    return json.dumps(items[:15], ensure_ascii=False)

def carrosseis():
    items = []
    p = ACERVO / "carrossel"
    if p.exists():
        for f in sorted(p.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True):
            if f.name == "index.md": continue
            items.append({"nome":f.stem[:40], "data":f.stem[-15:].replace("_"," "), "conteudo":ler(f)[:200]})
    return json.dumps(items[:20], ensure_ascii=False)

def inline_css():
    css_p = PROFILE_DIR / "styles"
    if not css_p.exists(): return ""
    parts = []
    for f in sorted(css_p.glob("*.css")):
        parts.append(f.read_text(encoding='utf-8'))
    return "\n".join(parts)

# Coleta dados
PERFIL = perfil_json()
RESULTADOS = resultados()
IDEIAS = ideias()
CARROSSEIS = carrosseis()
CSS = inline_css()

_html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OPB Snapshot — Paz na Conta</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#f5f5f7;--card:#fff;--text:#1d1d1f;--text2:#86868b;--border:#e5e5ea;--accent:#8b5cf6;--success:#34c759;--warning:#ff9f0a;--info:#5ac8fa;}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.5}}
.banner{{background:linear-gradient(135deg,#ff9f0a,#e67e22);color:#000;padding:10px;text-align:center;font-size:14px;font-weight:600;position:sticky;top:0;z-index:100}}
.banner a{{color:#000}}
.container{{max-width:800px;margin:0 auto;padding:16px}}
h1{{font-size:24px;margin-bottom:4px}}
h2{{font-size:18px;margin:24px 0 12px;padding-bottom:8px;border-bottom:2px solid var(--accent)}}
h3{{font-size:15px;margin:16px 0 8px;color:var(--text2)}}
.card{{background:var(--card);border-radius:12px;padding:16px;margin-bottom:12px;box-shadow:0 1px 3px rgba(0,0,0,.08)}}
.card-title{{font-weight:600;font-size:14px;color:var(--text2);margin-bottom:8px}}
.card-val{{font-size:16px;line-height:1.6}}
.stat-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:20px}}
.stat-card{{background:var(--card);border-radius:12px;padding:16px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.08)}}
.stat-num{{font-size:32px;font-weight:700}}
.stat-label{{font-size:12px;color:var(--text2);margin-top:4px}}
.result-item{{padding:12px;background:var(--bg);border-radius:8px;margin-bottom:8px;border-left:3px solid var(--accent)}}
.result-data{{font-size:11px;color:var(--text2);margin-bottom:4px}}
.result-texto{{font-size:14px;white-space:pre-wrap;max-height:100px;overflow:hidden}}
.result-tag{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;margin-top:4px}}
.tag-carrossel{{background:#e8f5e9;color:#2e7d32}}
.tag-consumo{{background:#e3f2fd;color:#1565c0}}
.tag-capa-video{{background:#fff3e0;color:#e65100}}
.ideia-item{{padding:10px 0;border-bottom:1px solid var(--border);font-size:14px}}
.ideia-data{{font-size:11px;color:var(--text2)}}
.expand-btn{{background:none;border:none;color:var(--accent);cursor:pointer;font-size:13px;padding:4px 0}}
.expand-btn:hover{{text-decoration:underline}}
@media(prefers-color-scheme:dark){{
:root{{--bg:#1c1c1e;--card:#2c2c2e;--text:#f5f5f7;--text2:#98989d;--border:#38383a}}
.result-item{{background:#1c1c1e}}
}}
</style>
</head>
<body>
<div class="banner">📸 <strong>Snapshot</strong> — Paz na Conta · OPB Studio · 22/05/2026</div>
<div class="container">

<h1>Paz na Conta</h1>
<p style="color:var(--text2);margin-bottom:20px">Snapshot dos dados salvos em 22/05/2026 · <a href="#" style="color:var(--accent)" onclick="document.getElementById('raw').style.display=document.getElementById('raw').style.display==='none'?'block':'none'">ver JSON</a></p>

<div class="stat-grid">
<div class="stat-card"><div class="stat-num">{len(json.loads(RESULTADOS))}</div><div class="stat-label">Resultados</div></div>
<div class="stat-card"><div class="stat-num">{len(json.loads(CARROSSEIS))}</div><div class="stat-label">Carrosséis</div></div>
<div class="stat-card"><div class="stat-num">{len(json.loads(IDEIAS))}</div><div class="stat-label">Ideias</div></div>
</div>

<script id="snapshot-data" type="application/json">{{
"perfil":{PERFIL},
"resultados":{RESULTADOS},
"ideias":{IDEIAS},
"carrosseis":{CARROSSEIS}
}}</script>

<h2>📋 Perfil</h2>
<div id="perfil-view"></div>

<h2>📂 Resultados Salvos</h2>
<div id="resultados-view"></div>

<h2>💡 Ideias Capturadas</h2>
<div id="ideias-view"></div>

<h2>🎠 Carrosséis</h2>
<div id="carrosseis-view"></div>

<div id="raw" style="display:none;margin-top:20px">
<h3>Dados Brutos (JSON)</h3>
<pre style="background:var(--card);border-radius:8px;padding:12px;overflow:auto;font-size:12px;max-height:400px" id="raw-json"></pre>
</div>

<p style="text-align:center;color:var(--text2);font-size:13px;margin:40px 0 20px">
OPB Studio · Snapshot gerado em 22/05/2026 · <a href="https://github.com/cleitoni/opb-sistema" style="color:var(--accent)">GitHub</a>
</p>

</div>

<script>
const data = JSON.parse(document.getElementById('snapshot-data').textContent);

function h(){{return document.getElementById(arguments[0])}}

function escapeHtml(s){{var d=document.createElement('div');d.appendChild(document.createTextNode(s));return d.innerHTML}}

// Perfil
function renderPerfil(){{
var p=data.perfil
var out=''
if(p.basico){{
var b=p.basico
out+='<div class="card"><div class="card-title">Dados Basicos</div><div class="card-val">'
out+= '<strong>'+escapeHtml(b.nome||'')+'</strong>'
if(b.nicho) out+='<br><span style="color:var(--text2)">'+escapeHtml(b.nicho)+'</span>'
if(b['tagline']) out+='<br>'+escapeHtml(b['tagline'])
if(b['publico alvo']||b['público-alvo']) out+='<br><br><strong>Publico:</strong> '+escapeHtml(b['publico alvo']||b['público-alvo'])
if(b.problema) out+='<br><br><strong>Problema:</strong> '+escapeHtml(b.problema)
out+='</div></div>'
}}
if(p.habilidades){{
var hh=p.habilidades
if(hh.habilidades) out+='<div class="card"><div class="card-title">Habilidades</div><div class="card-val">'+escapeHtml(hh.habilidades)+'</div></div>'
if(hh.resumo) out+='<div class="card"><div class="card-title">Resumo</div><div class="card-val">'+escapeHtml(hh.resumo)+'</div></div>'
}}
if(p.historias){{
var hs=p.historias
if(hs['história profissional']||hs['historia profissional']||hs.historia) out+='<div class="card"><div class="card-title">Historias</div><div class="card-val">'+escapeHtml(hs['história profissional']||hs['historia profissional']||hs.historia||'')+'</div></div>'
if(hs.experiências||hs.experiencias) out+='<div class="card"><div class="card-title">Experiencias</div><div class="card-val">'+escapeHtml(hs.experiências||hs.experiencias||'')+'</div></div>'
}}
if(p.cosmovisao&&p.cosmovisao.valores) out+='<div class="card"><div class="card-title">Cosmovisao</div><div class="card-val">'+escapeHtml(p.cosmovisao.valores)+'</div></div>'
if(p.posicionamento&&p.diferencial) out+='<div class="card"><div class="card-title">Diferencial</div><div class="card-val">'+escapeHtml(p.diferencial)+'</div></div>'
if(p.posicionamento&&p['proposta de valor']) out+='<div class="card"><div class="card-title">Proposta de Valor</div><div class="card-val">'+escapeHtml(p['proposta de valor'])+'</div></div>'
h('perfil-view').innerHTML=out||'<div class="card">Nenhum dado de perfil encontrado</div>'
}}

// Resultados
function renderResultados(){{
var items=data.resultados
if(!items.length){{h('resultados-view').innerHTML='<div class="card">Nenhum resultado salvo</div>';return}}
var out=''
for(var i=0;i<items.length;i++){{
var r=items[i]
out+='<div class="result-item">'
out+='<div class="result-data">'+escapeHtml(r.data||'')+' <span class="result-tag tag-'+r.tag+'">'+escapeHtml(r.tag)+'</span></div>'
out+='<div class="result-texto" id="rt-'+i+'">'+escapeHtml(r.texto.substring(0,200))+(r.texto.length>200?'...':'')+'</div>'
if(r.texto.length>200) out+='<button class="expand-btn" onclick="expandResult('+i+')">Mostrar mais</button>'
out+='</div>'
}}
h('resultados-view').innerHTML=out
}}
function expandResult(i){{
var el=h('rt-'+i)
var txt=data.resultados[i].texto
if(el.style.maxHeight==='none'){{el.style.maxHeight='100px';el.textContent=txt.substring(0,200)+'...'}}
else{{el.style.maxHeight='none';el.textContent=txt}}
}}

// Ideias
function renderIdeias(){{
var items=data.ideias
if(!items.length){{h('ideias-view').innerHTML='<div class="card">Nenhuma ideia capturada</div>';return}}
var out=''
for(var i=0;i<items.length;i++){{
out+='<div class="ideia-item">'+escapeHtml(items[i].titulo)+'<div class="ideia-data">'+escapeHtml(items[i].data||'')+'</div></div>'
}}
h('ideias-view').innerHTML=out
}}

// Carrosseis
function renderCarrosseis(){{
var items=data.carrosseis
if(!items.length){{h('carrosseis-view').innerHTML='<div class="card">Nenhum carrossel gerado</div>';return}}
var out=''
for(var i=0;i<items.length;i++){{
var c=items[i]
out+='<div class="result-item">'
out+='<div class="result-data">'+escapeHtml(c.data||'')+'</div>'
out+='<div class="result-texto">'+escapeHtml(c.conteudo||c.nome||'')+'</div>'
out+='</div>'
}}
h('carrosseis-view').innerHTML=out
}}

// Raw JSON
document.getElementById('raw-json').textContent=JSON.stringify(data,null,2)

renderPerfil()
renderResultados()
renderIdeias()
renderCarrosseis()
</script>
</body>
</html>'''

OUT.write_text(_html, encoding='utf-8')
print("[OK] Snapshot: " + str(OUT))
print("    Tamanho: " + str(len(_html)) + " bytes")
print("    Abra no navegador ou deploy Vercel/Netlify/GitHub Pages")
