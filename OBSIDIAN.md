# Obsidian Integration — OPB Sistema

Como usar o Obsidian no PC e celular para escrever ideias sincronizadas.

## 📡 Como a Sincronia Funciona

```
PC (Obsidian) ←→ GitHub ←→ Celular (Obsidian)
```

Tudo que voce escreve no Obsidian (ideias, notas, anotacoes) vai para o GitHub via `git push`. No celular, o Termux puxa do GitHub. As pastas sincronizadas sao:

| Pasta | O que guardar |
|-------|---------------|
| `inbox/` | Captura rapida de ideias (abre primeiro) |
| `acervo/ideias/` | Ideias detalhadas e organizadas |
| `acervo/transcricoes/` | Transcricoes de video/audio |
| `_templates/` | Modelos para novas notas |
| `negocio/` | Documentos do negocio |
| `perfis/` | Perfis de conteudo |

---

## 💻 PC — Configuracao

### 1. Abrir o projeto como Vault
```
iniciar-obsidian.bat
```
Isso ja faz: `git pull` + abre Obsidian.

### 2. Escrever ideias
- Abra `inbox/inbox.md` para captura rapida
- Use `Ctrl+N` para nova nota (escolha template `idea.md`)
- As notas salvam em `acervo/ideias/`

### 3. Sincronizar (escolha um metodo)

**Manual** — `sync.bat` (menu: enviar/receber)

**Automatico** — `sync-watch.bat` (a cada 2min, em segundo plano)

**Iniciar + Sync** — `iniciar-obsidian.bat` (pull + abre Obsidian)

### Atalhos 1-Clique

| Arquivo | Faz |
|---------|-----|
| `iniciar-obsidian.bat` | Pull + abre Obsidian |
| `sync-watch.bat` | Auto-sync a cada 2min |
| `sync.bat` | Sync manual (envia/recebe) |
| `abrir-obsidian.bat` | So abre Obsidian |

---

## 📱 Celular (Android) — Configuracao

### 1. Instalar apps
- **Obsidian** — Google Play Store
- **Termux** — F-Droid (https://f-droid.org/packages/com.termux/) ou GitHub

### 2. Rodar setup automatico
```
pkg install -y curl
curl -sL https://raw.githubusercontent.com/cleiton-negreiros/opb-sistema/main/setup-mobile.sh | bash
```
Ou copie o `setup-mobile.sh` para o celular e rode:
```
bash setup-mobile.sh
```

### 3. Abrir vault no Obsidian
- Abra o Obsidian
- "Open folder as vault"
- Navegue ate: `Internal Storage/Obsidian/opb-sistema`
- Selecione a pasta

### 4. Sincronizar
No Termux:
```
opb-sync        # atalho: puxa + envia
```

Na primeira vez vai pedir o token do GitHub. Gere em:
https://github.com/settings/tokens (marque `repo`)

### Widget Rapido (opcional)
Crie um widget do Termux na tela inicial com:
```
bash ~/.opb-bin/sync-safe
```

---

---

## 📝 Pipeline de Conteudo Diario

Escreva 1 texto por dia no celular e o sistema gera 4 formatos automaticamente.

### Fluxo Completo

```
Celular (Obsidian)                          PC (Pipeline)
─────────────────────────                   ─────────────────────────
                                            ┌─ 🎠 Carrossel Instagram
1. Cria email com template ── sync ──► Git ── 📱 Reels 60s
2. Preenche: tema, versiculo,               ├─ 🎬 Video 10min YouTube
   reflexao, aplicacao pratica              └─ 📝 Post Instagram
3. Git add + commit + push
```

### 1. Escrever o Email Diario (no celular)

Use `Ctrl+N` → escolha template **`email-diario`**:

```markdown
---
tema: Confianca na Providencia
versiculo: Mt 6, 26.33
pilar: espiritual
---

# Confianca na Providencia

## Versiculo do Dia
> Olhai as aves do ceu...

## Reflexao
[Seu texto aqui]

## Aplicacao Pratica
[O que fazer na pratica]

## Oracao
[Oracao final]
```

### 2. Sincronizar

No Termux:
```
opb-sync
```

No PC (auto):
```
sync-watch.bat
```

### 3. Rodar o Pipeline

No **PC**:
```
pipeline-conteudo.bat
```
Isso pega o arquivo mais recente de `inbox/` ou `acervo/ideias/` e gera:

| Formato | Onde salva | Para que |
|---------|-----------|----------|
| 🎠 Carrossel | `acervo/carrossel/` | Post Instagram (carrossel) |
| 📱 Reels | `acervo/ideias/` | Reels 60s |
| 🎬 Video 10min | `acervo/video/` | YouTube semanal |
| 📝 Post | `perfis/paz-na-conta/output/text_posts/` | Legenda Instagram |

No **Termux** (celular):
```
bash pipeline-conteudo.sh
```

### Pelo Navegador (PC + Celular)

Na plataforma web, acesse a pagina Pipeline e clique "Processar Email do Dia":
```
POST /api/pipeline/diario
```

Ou diretamente pelo navegador: acesse a plataforma → secao Pipeline.

---

## ⚙️ Templates Disponiveis

Os templates sao usados via `Ctrl+N` no Obsidian:

| Template | Uso |
|----------|-----|
| `_templates/idea.md` | Nova ideia estruturada |
| `_templates/daily.md` | Nota diaria |
| `_templates/email-diario.md` | **Email diario para pipeline** |

---

## 🔧 Solucao de Problemas

**"Conflito no git"** — Tanto PC quanto celular editaram o mesmo arquivo.
```
git merge origin/master
git add .
git commit -m "merge: resolucao manual"
git push
```

**"Token expirou"** — No Termux:
```
rm ~/.opb-git-credentials
opb-sync
```

**Obsidian nao ve a pasta** — No Termux, verifique se o clone foi em `~/storage/shared/Obsidian/opb-sistema` (area acessivel ao Obsidian).

---

_Last updated: 2026-06-10_
