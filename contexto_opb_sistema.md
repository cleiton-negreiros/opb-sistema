# Contexto do Projeto OPB Sistema

O repositório `opb-sistema` é um sistema multi-agente de inteligência artificial projetado para solopreneurs, com o objetivo de automatizar e gerenciar diversas tarefas relacionadas à produção de conteúdo e gestão de negócios digitais. O sistema é modular, permitindo a criação e gerenciamento de múltiplos perfis de negócio, sendo "Paz na Conta" um desses perfis.

## Arquitetura e Componentes Principais

O sistema é construído com uma stack que inclui Python 3.8+, Ollama (para modelos de linguagem como Llama3), HTML/CSS/JS e Bootstrap 5 [1]. A arquitetura central é composta por:

1.  **API Server (`api_server.py`)**: Um servidor Flask que atua como o hub central, servindo tanto o frontend quanto a API REST. Ele gerencia a comunicação com os agentes de IA, processa requisições e fornece dados para a interface do usuário. [2]
2.  **Agentes de IA (`agents/`)**: Uma coleção de scripts Python, cada um responsável por uma funcionalidade específica. Exemplos incluem:
    *   `carrossel/`: Geração de carrosséis para redes sociais.
    *   `capa_video/`: Geração de ideias para thumbnails de vídeos do YouTube.
    *   `consumo/`: Processamento e análise de textos, PDFs e URLs.
    *   `text_generator/`: Geração de posts para Instagram.
    *   `posicionamento/`: Análise de posicionamento de mercado.
    *   `radagast/`: Curadoria de conteúdo (utiliza `yt-dlp` e RSS).
    *   `narvi/`: Edição de vídeo com FFmpeg.
    *   `telegram_bot/`: Interface para interação via Telegram.
    *   `coordinator/`: Agente coordenador para orquestrar outras tarefas.
3.  **Cérebro (`cerebro/`)**: Considerado a "fonte única de memória viva" do ecossistema. Contém a estrutura de governança do negócio, regras, decisões, lições aprendidas e o perfil do empreendedor. [3]
4.  **Perfis (`perfis/`)**: O sistema suporta múltiplos perfis de negócio, cada um com sua própria configuração e dados isolados. O perfil ativo é gerenciado por `profile_manager.py`, que carrega as configurações específicas de cada perfil, como `paz-na-conta`, `toque-de-paz` e `caminho-vida`. [4]
5.  **Frontend (`cerebro/perfil-empreendedor-solo/`)**: Uma aplicação web progressiva (PWA) mobile-first, que inclui um dashboard principal (`plataforma.html`) e um formulário de perfil (`formulario.html`).

## O Perfil "Paz na Conta"

O perfil "Paz na Conta" é um dos perfis ativos no sistema, focado em "Mentoria de Finanças Católicas". Seu público-alvo são "Católicos que desejam organizar suas finanças com base na fé". O problema que busca resolver é ajudar pessoas a "organizar suas finanças pessoais e familiares com base nos princípios da Doutrina Social da Igreja e nos ensinamentos católicos sobre administração do dinheiro" [5].

### Linha Editorial

A linha editorial do "Paz na Conta" é clara: "Finanças à luz da fé católica — organizar a vida financeira com base no Evangelho, na Doutrina Social da Igreja e no Segredo da Divina Providência" [6]. Os princípios que guiam a produção de conteúdo incluem:

*   **Nem prosperidade, nem pobreza como virtude**: Rejeita tanto a teologia da prosperidade quanto a ideia de que a pobreza material é santidade.
*   **Dinheiro serve, não governa**: Baseado na encíclica *Fratelli Tutti* e na Doutrina Social da Igreja.
*   **Organização é caminho de santidade**: Administrar bem os recursos é cooperar com a criação de Deus.
*   **Paz é o norte**: O objetivo financeiro não é a riqueza, mas a paz para servir melhor.
*   **Providência não é passividade**: Confiar em Deus não significa negligenciar a parte humana.

O sistema também armazena frases de impacto, citações de figuras como Pe. Antônio Furtado, Emmir Nogueira e Pe. Jean-Pierre de Caussade, além de citações bíblicas-chave, que servem como referências para a geração de conteúdo. [6]

## Integração com o Planejamento de Conteúdo

O `opb-sistema` já possui agentes dedicados à geração de carrosséis e ideias de capa de vídeo, o que se alinha perfeitamente com o plano estratégico de conteúdo que elaboramos para o "Paz Na Conta". A linha editorial e os princípios do projeto, já definidos no sistema, reforçam a abordagem proposta para os pilares de conteúdo (Espiritual, Prático, Social e Cultural, Devocional e Comunidade).

A existência de um `telegram_bot` sugere a possibilidade de automatizar a distribuição de conteúdo ou a interação com a comunidade, enquanto o agente `consumo` pode ser utilizado para processar e curar informações relevantes para os temas de finanças católicas.

## Status do Projeto

O projeto está em desenvolvimento ativo, com diversas funcionalidades já implementadas, incluindo o dashboard PWA, o formulário de perfil, vários agentes de IA e o API Server Flask. O backlog inclui o preenchimento do perfil do empreendedor com conteúdo real e a geração dos primeiros carrosséis e posts via plataforma [1].

---

### Referências

[1] cleiton-negreiros. *opb-sistema/AGENTS.md*. GitHub. Disponível em: https://github.com/cleiton-negreiros/opb-sistema/blob/main/AGENTS.md. Acesso em: 21 mai. 2026.
[2] cleiton-negreiros. *opb-sistema/api_server.py*. GitHub. Disponível em: https://github.com/cleiton-negreiros/opb-sistema/blob/main/api_server.py. Acesso em: 21 mai. 2026.
[3] cleiton-negreiros. *opb-sistema/MAPA.md*. GitHub. Disponível em: https://github.com/cleiton-negreiros/opb-sistema/blob/main/MAPA.md. Acesso em: 21 mai. 2026.
[4] cleiton-negreiros. *opb-sistema/perfis/perfis.json*. GitHub. Disponível em: https://github.com/cleiton-negreiros/opb-sistema/blob/main/perfis/perfis.json. Acesso em: 21 mai. 2026.
[5] cleiton-negreiros. *opb-sistema/perfis/paz-na-conta/perfil/PERFIL.md*. GitHub. Disponível em: https://github.com/cleiton-negreiros/opb-sistema/blob/main/perfis/paz-na-conta/perfil/PERFIL.md. Acesso em: 21 mai. 2026.
[6] cleiton-negreiros. *opb-sistema/negocio/governanca/linha-editorial.md*. GitHub. Disponível em: https://github.com/cleiton-negreiros/opb-sistema/blob/main/negocio/governanca/linha-editorial.md. Acesso em: 21 mai. 2026.
