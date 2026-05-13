---
name: "MAPA — Cérebro"
description: "Mapa raiz do cérebro — fonte única de memória viva do ecossistema"
tipo: referencia
updated_at: AAAA-MM-DD
---

# Cérebro — Mapa

> Fonte única de memória viva. Todo agente importante lê este mapa ao abrir sessão. O Claude Code monta o `MEMORY.md` ponte apontando para os MAPAs âncora daqui.

## Estrutura

```
cerebro/
├── MAPA.md                         ← Este arquivo
├── README.md
│
├── negocio/
│   ├── governanca/                 Regras, decisões, lições, referências, contexto
│   ├── areas/                      Áreas operacionais (conteúdo, cursos, marketing, suporte, comunidade)
│   ├── produtos/                   Catálogo de produtos
│   ├── infra/                      Sistemas internos
│   └── projetos/                   Iniciativas com início/fim
│
├── perfil-empreendedor-solo/       Template de perfil do empreendedor (alimenta o cérebro)
│
├── pessoal/                        Vida pessoal (ACL nativa)
│
├── agentes/                        Configuração de cada agente IA
│
├── playbooks/                      Manuais executáveis transversais
│
├── acervo/                         Conteúdo produzido
│
└── seguranca/                      Permissões de acesso por agente
```

## Padrão de navegação

Toda pasta tem um `MAPA.md` no topo com:

- Índice do que tem dentro
- Convenção de nomes
- Quando abrir

## Ordem de leitura sugerida (toda sessão nova)

1. `MAPA.md` (este arquivo)
2. `negocio/governanca/regras/MAPA.md`
3. `negocio/projetos/ativos.md`
4. `agentes/MAPA.md`

## Manutenção

- Mudou estrutura? Atualize este MAPA primeiro.
- Criou pasta nova? Crie um `MAPA.md` dentro dela.
- Removeu pasta? Remova a referência aqui.
