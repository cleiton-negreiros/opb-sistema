# Integração: OPB Sistema & Planejamento Paz Na Conta

A análise do repositório `opb-sistema` revela que você já possui uma infraestrutura tecnológica robusta para suportar o canal **Paz Na Conta**. O sistema não é apenas um repositório de código, mas um "Cérebro" que já contém a alma do seu projeto. Abaixo, relacionamos como as funcionalidades do sistema potencializam o plano estratégico de conteúdo.

## 1. Automação da Produção de Conteúdo

O sistema possui agentes específicos que podem ser alimentados com os temas do nosso planejamento:

*   **Agente Carrossel (`agents/carrossel/`)**: Pode ser usado para gerar os carrosséis semanais propostos no cronograma (ex: "O que é a Providência Divina?" ou "3 passos para sair das dívidas").
*   **Agente Capa Vídeo (`agents/capa_video/`)**: Essencial para a fase de vídeos longos no YouTube, ajudando a criar ganchos visuais para temas como "Teologia da Prosperidade: Onde está o erro?".
*   **Agente Text Generator (`agents/text_generator/`)**: Pode transformar as reflexões teológicas em legendas engajadoras para o Instagram, mantendo o tom de voz definido no arquivo `quem-sou.md`.

## 2. Curadoria e Inteligência

O pilar **Social e Cultural** do nosso planejamento exige pesquisa constante. O sistema oferece:

*   **Agente Radagast (`agents/radagast/`)**: Sua capacidade de curadoria via RSS e YouTube pode ser configurada para monitorar outros canais de finanças e sites católicos, trazendo "matéria-prima" para novos vídeos.
*   **Agente Consumo (`agents/consumo/`)**: Ideal para processar encíclicas papais (como a *Fratelli Tutti*) ou documentos da Doutrina Social da Igreja, extraindo os pontos principais para o pilar **Espiritual**.

## 3. Gestão de Identidade e Tom de Voz

O arquivo `negocio/governanca/linha-editorial.md` do seu sistema é a base perfeita para garantir que eu, como seu assistente, e seus agentes de IA, falemos a mesma língua. Os princípios de "Paz como norte" e "Providência não é passividade" já estão codificados e devem guiar cada roteiro que produzirmos.

## 4. Expansão Multi-Perfil

A estrutura multi-perfil do sistema (`perfis/perfis.json`) indica que o **Paz Na Conta** é parte de um ecossistema maior (incluindo *Toque de Paz* e *Caminho Vida*). Isso abre margem para:
*   **Cross-content**: Relacionar finanças com música e louvor (*Toque de Paz*) ou formação espiritual (*Caminho Vida*).
*   **Reuso de Agentes**: A mesma inteligência que gera um carrossel de finanças pode ser ajustada para os outros perfis, otimizando seu tempo como solopreneur.

## Próximos Passos Sugeridos

1.  **Alimentar o Cérebro**: Usar o agente `alimentar` para inserir o Plano Estratégico que criamos hoje no sistema.
2.  **Configurar o Radagast**: Adicionar palavras-chave relacionadas a finanças católicas para começar a receber sugestões de temas.
3.  **Primeiro Roteiro**: Escolher um dos temas do cronograma (ex: "É errado ser rico?") e usar o `text_generator` para criar o primeiro rascunho, refinando-o com a visão teológica que estruturamos.
