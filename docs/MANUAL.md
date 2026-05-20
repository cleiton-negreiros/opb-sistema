# Manual do Usuário — Paz na Conta

> **Versão:** 2.3 | **Última atualização:** 2026-05-20
> **Suporte:** @paznaconta (Instagram) | @NegreirosBot (Telegram)

---

## Sumário
1. [Introdução](#1-introdução)
2. [Primeiros Passos](#2-primeiros-passos)
3. [Criando sua Conta](#3-criando-sua-conta)
4. [Onboarding](#4-onboarding)
5. [Dashboard](#5-dashboard)
6. [Agentes de IA](#6-agentes-de-ia)
7. [Cérebro](#7-cérebro)
8. [Quadro de Avisos](#8-quadro-de-avisos)
9. [Perfil](#9-perfil)
10. [Configurações](#10-configurações)
11. [PWA Mobile](#11-pwa-mobile)
12. [Telegram Bot](#12-telegram-bot)
13. [FAQ](#13-faq)
14. [Suporte](#14-suporte)

---

## 1. Introdução

### O que é o Paz na Conta?
O Paz na Conta é um sistema de agentes de IA que ajuda católicos a organizarem suas finanças com propósito e fé. A plataforma combina:

- **Agentes de IA locais** (rodam no seu computador, sem APIs pagas)
- **Dashboard web** (interface moderna e responsiva)
- **Telegram Bot** (comandos rápidos pelo celular)
- **PWA Mobile** (app instalável no celular)

### Para quem é?
- Católicos que querem organizar finanças com base no Evangelho
- Empreendedores que precisam de conteúdo para Instagram
- Mentores que querem escalar seu atendimento
- Qualquer pessoa que quer paz financeira com propósito

### Requisitos
- **PC:** Windows 10/11 ou macOS 12+, Python 3.10+, 4GB RAM
- **Celular:** Android 8+ (Termux) ou iOS 16+ (a-Shell)
- **Internet:** Apenas para download inicial e sync via Git

---

## 2. Primeiros Passos

### Instalação Rápida (PC)

**Windows:**
1. Instale Python em https://python.org/downloads (marque "Add to PATH")
2. Baixe o projeto: `git clone https://github.com/cleiton-negreiros/opb-sistema.git`
3. Entre na pasta: `cd opb-sistema`
4. Instale dependências: `pip install -r requirements.txt`
5. Inicie: `iniciar-dia.bat`
6. Acesse: http://localhost:5000

**macOS:**
1. Instale Python: `brew install python`
2. Baixe o projeto: `git clone https://github.com/cleiton-negreiros/opb-sistema.git`
3. Entre na pasta: `cd opb-sistema`
4. Instale dependências: `pip3 install -r requirements.txt`
5. Inicie: `python3 api_server.py &`
6. Acesse: http://localhost:5000

### Instalação no Celular (Android)
1. Instale Termux do F-Droid: https://f-droid.org/packages/com.termux/
2. Abra Termux e execute:
   ```bash
   pkg update -y && pkg install python git clang -y
   termux-setup-storage
   cd ~/storage/downloads
   git clone https://github.com/cleiton-negreiros/opb-sistema.git
   cd opb-sistema
   pip install flask flask-cors python-telegram-bot requests jinja2 markdown
   bash termux.sh
   ```
3. Acesse: http://localhost:5000

### Instalar como App (PWA)
- **Android (Chrome):** Menu (⋮) → "Adicionar à tela inicial"
- **iOS (Safari):** Compartilhar → "Adicionar à Tela de Início"
- **PC (Chrome/Edge):** Ícone de instalação na barra de endereço

---

## 3. Criando sua Conta

### Registro
1. Acesse http://localhost:5000/auth.html
2. Clique na aba **"Criar Conta"**
3. Preencha:
   - **Nome Completo:** Seu nome
   - **Usuário:** 3-30 caracteres (letras, números, underscore)
   - **Email:** Email válido
   - **Senha:** Mínimo 6 caracteres
   - **Confirmar Senha:** Repita a senha
4. Clique em **"Criar Conta"**
5. Se tudo estiver correto, você será redirecionado para o login

### Login
1. Acesse http://localhost:5000/auth.html
2. Na aba **"Entrar"**, digite:
   - **Email ou Usuário**
   - **Senha**
3. Clique em **"Entrar"**
4. Se for seu primeiro acesso, você será direcionado ao Onboarding

### Esqueci minha Senha
1. Na tela de login, clique em **"Esqueceu a senha?"**
2. Digite seu email
3. Clique em **"Enviar Instruções"**
4. *Nota: Recuperação por email requer configuração adicional*

### Logout
1. Vá para **Configurações** (engrenagem no menu)
2. Role até a seção **"Conta"**
3. Clique em **"Sair"**

---

## 4. Onboarding

O onboarding configura sua experiência personalizada em 3 passos:

### Passo 1: Quem é você?
- **Objetivo principal:** Escolha entre Organizar Finanças, Sair das Dívidas, Começar a Investir ou Crescer Negócio
- **Faixa de renda:** Selecione sua faixa salarial

### Passo 2: Conteúdo de interesse
Selecione os temas que mais te interessam (pode escolher vários):
- 💰 Orçamento
- ⛪ Dízimo
- 🔓 Dívidas
- 👨‍👩‍👧‍👦 Família
- 🏢 Negócios
- 📱 Conteúdo

### Passo 3: Configurações
- **Token do Telegram:** Opcional, para conectar com o bot
- **URL da API:** Deixe padrão se estiver rodando localmente
- **Notificações:** Ative ou desative alertas

Após completar, você terá acesso completo à plataforma.

---

## 5. Dashboard

O dashboard é sua central de controle. Ele mostra:

### KPI Cards
- **Agentes Ativos:** Quantos agentes estão funcionando
- **Ideias Salvas:** Total de ideias capturadas
- **Carrosséis Gerados:** Posts criados
- **Conhecimento Salvo:** Artigos processados

### Heatmap de Atividade
Visualização estilo GitHub dos últimos 90 dias de atividade.

### Streak Semanal
Sequência de dias consecutivos usando a plataforma.

### Ações Rápidas
Botões para acessar rapidamente:
- Transcrever vídeo
- Gerar carrossel
- Alimentar cérebro
- Gerar post

### Agentes
Cards clicáveis para cada agente disponível. Clique para executar.

### Atividade Recente
Timeline das últimas ações realizadas.

---

## 6. Agentes de IA

### Transcrição
**O que faz:** Transcreve vídeos do YouTube automaticamente.

**Como usar:**
1. Vá para **Transcrição** no menu
2. Cole a URL do YouTube
3. Selecione o idioma (português, inglês, etc.)
4. Clique em **"Transcrever"**
5. Aguarde o processamento (pode levar alguns minutos)

**Dica:** URLs curtas funcionam melhor. Evite playlists.

---

### Capa de Vídeo
**O que faz:** Gera ideias de thumbnails para vídeos do YouTube.

**Como usar:**
1. Vá para **Capa Vídeo**
2. Digite o tema do vídeo
3. Escolha a quantidade (3-10)
4. Clique em **"Gerar"**

**Exemplo:** Tema: "Como sair das dívidas com fé" → 5 ideias de capa

---

### Carrossel
**O que faz:** Gera carrosséis para Instagram com conteúdo educativo.

**Como usar:**
1. Vá para **Carrossel**
2. Digite o tema ou cole um texto longo
3. Escolha o tipo (educacional, motivacional, tutorial)
4. Defina o número de slides (5-10)
5. Clique em **"Gerar"**

**Editor:** Após gerar, você pode:
- Visualizar o carrossel
- Editar o conteúdo
- Salvar alterações
- Deletar

**Arquivo:** Veja todos os carrosséis gerados na aba "Arquivo"

---

### Consumo de Conteúdo
**O que faz:** Processa artigos, livros e conteúdos para o cérebro.

**Como usar:**
1. Vá para **Consumo**
2. Cole o conteúdo a ser processado
3. Escolha o tipo de análise (completo, resumo, insights)
4. Clique em **"Processar"**
5. O conteúdo será analisado e salvo no cérebro

**Alimentar Cérebro:** Após processar, clique em "Alimentar Cérebro" para integrar ao conhecimento.

---

### Gerador de Texto
**O que faz:** Cria posts para Instagram.

**Como usar:**
1. Vá para **Text Generator**
2. Defina o objetivo do post
3. Escolha o tipo (educacional, motivacional, venda)
4. Clique em **"Gerar"**

**Templates rápidos:** Use os botões de template para gerar posts rápidos sobre temas comuns.

---

### Posicionamento
**O que faz:** Analisa seu posicionamento e concorrentes.

**Como usar:**
1. Vá para **Posicionamento**
2. Digite seu nicho
3. Liste concorrentes (um por linha)
4. Clique em **"Analisar"**

**Resultado:** Você receberá análise de:
- Verdade do nicho
- Inimigo comum
- Frase de posicionamento
- Checklist de ação

---

### Narvi (Editor de Vídeo)
**O que faz:** Edita vídeos automaticamente (requer FFmpeg).

**Como usar:**
1. Vá para **Narvi**
2. Selecione o arquivo de vídeo
3. Escolha o tipo de corte
4. Defina o formato de saída
5. Clique em **"Processar"**

**Nota:** Requer FFmpeg instalado no sistema.

---

### Radagast (Curadoria)
**O que faz:** Curadoria automática de conteúdo via RSS e YouTube.

**Como usar:**
1. Vá para **Radagast**
2. Clique em **"Executar"**
3. Aguarde a curadoria

**Configuração:** Edite `agents/radagast/config/keywords.json` para definir termos de busca.

---

## 7. Cérebro

O Cérebro é a base de conhecimento do sistema.

### Árvore de Arquivos
Visualize todos os arquivos do cérebro em estrutura de pastas.

### Integridade
Verifica se os arquivos essenciais existem e estão corretos.

### MAPAs
Lista todos os arquivos MAPA.md (mapas de conhecimento) com descrição.

### Como funciona
- Cada agente tem seu próprio MAPA.md
- Os MAPAs contêm conhecimento processado
- O cérebro cresce conforme você usa os agentes
- Arquivos são em Markdown (.md) para fácil edição

---

## 8. Quadro de Avisos

Sistema de tarefas para delegar trabalho aos agentes.

### Adicionar Tarefa
1. Vá para **Quadro de Avisos**
2. Preencha:
   - **Descrição:** O que precisa ser feito
   - **Agente:** Qual agente vai executar
   - **Prioridade:** Alta, Média ou Baixa
3. Clique em **"Adicionar"**

### Lista de Tarefas
- **Pendentes:** Tarefas aguardando execução
- **Concluídas:** Tarefas finalizadas

### Ações
- ✅ **Concluir:** Marca tarefa como feita
- 🗑️ **Excluir:** Remove a tarefa

### Dica
Use o quadro de avisos para planejar seu conteúdo da semana. Adicione tarefas para cada agente e execute uma por uma.

---

## 9. Perfil

Configure sua identidade e posicionamento.

### Abas do Perfil

**Dados Pessoais:**
- Nome, email, descrição
- Links sociais (Instagram, YouTube, etc.)

**Habilidades:**
- Habilidades técnicas
- Habilidades interpessoais
- Áreas de expertise

**Histórias:**
- Histórias pessoais para conteúdo
- Testemunhos
- Experiências de vida

**Cosmovisão:**
- Valores fundamentais
- Crenças sobre dinheiro
- Princípios católicos

**Público-Alvo:**
- Quem você serve
- Dores e desejos
- Faixa etária e perfil

**Posicionamento:**
- Sua verdade única
- Inimigo comum
- Frase de posicionamento

**Narrativa:**
- Sua história de origem
- Jornada do herói
- Mensagem central

### Identidade Visual
- Cores primária e secundária
- Fonte preferida
- Estilo visual

### Salvar
Clique em **"Salvar"** em cada aba para persistir as alterações.

---

## 10. Configurações

### Geral
- **URL da API:** Endereço do servidor (padrão: http://localhost:5000)
- **Caminho do Projeto:** Pasta do projeto no sistema
- **Token do Telegram:** Token do bot no Telegram

### Ferramentas
- **Iniciar Telegram Bot:** Inicia o bot
- **Verificar Dependências:** Checa se todos os pacotes estão instalados
- **Exportar Log:** Baixa log do sistema

### Conta
- **Seu email e plano**
- **Botão Sair:** Faz logout

### Sobre
- Versão do sistema
- Build date
- Número de agentes

---

## 11. PWA Mobile

O sistema funciona como app no celular.

### Instalar
1. Acesse http://localhost:5000/dashboard.html no celular
2. Chrome (Android): Menu → "Adicionar à tela inicial"
3. Safari (iOS): Compartilhar → "Adicionar à Tela de Início"
4. O app aparece na home como app nativo

### Funcionalidades Mobile
- Status dos serviços (API + Bot)
- Executar agentes (Radagast, Carrossel, Texto, Consumo)
- Quadro de avisos (adicionar/concluir tarefas)
- Links rápidos para plataforma e health check
- Painel de output para resultados

### Sync PC-Celular
1. No PC: `git add -A && git commit -m "sync" && git push`
2. No celular (Termux): `git pull`
3. Os dados são sincronizados via Git

---

## 12. Telegram Bot

O bot @NegreirosBot permite interagir com os agentes pelo Telegram.

### Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `/start` | Inicia o bot e mostra menu |
| `/ajuda` | Lista todos os comandos |
| `/ideia <texto>` | Captura uma ideia |
| `/transcrever <url>` | Transcreve vídeo do YouTube |
| `/carrossel <tema>` | Gera carrossel para Instagram |
| `/texto <objetivo>` | Gera post para Instagram |
| `/consumo <texto>` | Processa conteúdo |
| `/capa <tema>` | Gera ideias de capa de vídeo |
| `/posicionamento <nicho>` | Análise de posicionamento |
| `/tarefas` | Lista tarefas pendentes |
| `/tarefa <descricao>` | Adiciona tarefa |
| `/concluir <id>` | Conclui tarefa |
| `/status` | Status dos serviços |

### Configurar Token
1. No Telegram, fale com @BotFather
2. Crie um novo bot
3. Copie o token
4. No sistema: Configurações → Token do Telegram → Salvar

---

## 13. FAQ

### O sistema funciona sem internet?
Sim! Os agentes rodam localmente com Ollama. Internet é necessária apenas para:
- Download inicial do projeto
- Sync via Git
- Transcrição de vídeos do YouTube

### Posso usar em mais de um dispositivo?
Sim! Use Git para sincronizar entre PC e celular.

### Os dados ficam seguros?
Sim! Tudo roda localmente no seu computador. Nenhum dado é enviado para servidores externos.

### Preciso pagar alguma API?
Não! O sistema usa Ollama (IA local gratuita) e fontes gratuitas (yt-dlp, RSS).

### Como faço backup?
Basta copiar a pasta `opb-sistema` inteira ou usar Git.

### O sistema funciona no celular?
Sim! Via Termux (Android) ou a-Shell (iOS). A experiência é otimizada para mobile.

### Posso personalizar os agentes?
Sim! Cada agente tem arquivos de configuração em sua pasta. Edite os arquivos `.md` e `.json`.

### Como atualizar o sistema?
```bash
git pull
pip install -r requirements.txt
```

### O que acontece se eu perder minha senha?
O sistema armazena senhas com hash seguro. Atualmente, a recuperação requer acesso direto ao banco de dados SQLite.

### Posso usar com outros modelos de IA?
Sim! O sistema suporta Ollama e pode ser configurado para outros providers via `utils/llm_provider.py`.

---

## 14. Suporte

### Canais
- **Instagram:** @paznaconta
- **Telegram:** @NegreirosBot (comando /ajuda)
- **Email:** contato@paznaconta.com
- **GitHub:** https://github.com/cleiton-negreiros/opb-sistema

### Reportar Bugs
1. Vá para https://github.com/cleiton-negreiros/opb-sistema/issues
2. Clique em "New Issue"
3. Descreva o problema com:
   - Sistema operacional
   - Versão do Python
   - Passos para reproduzir
   - Mensagem de erro

### Contribuir
1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m "feat: descrição"`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

---

*Paz na Conta — Finanças com fé. Sem culpa. Sem prosperidade falsa.* ✝️
