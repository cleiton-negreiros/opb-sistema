---
name: "Ordem de leitura"
description: "Sequência oficial de leitura para a IA navegar o cérebro com disciplina"
tipo: regra
---

# Ordem de leitura

> A IA não precisa ler o cérebro inteiro toda sessão. Lê o mínimo pra agir com qualidade. Esta regra é o roteiro de quando abrir o quê.

## Regra-mãe

**Ler o mínimo necessário para agir com qualidade.** Nem superficialidade burra, nem mergulho arqueológico sem necessidade. O `MEMORY.md` já carrega os arquivos âncora; o resto a IA abre só quando a tarefa exigir.

## Ordem padrão (toda sessão nova)

1. `MAPA.md` (raiz) — onde a coisa está.
2. `negocio/governanca/regras/MAPA.md` — como você quer ser tratado.
3. `negocio/projetos/ativos.md` — o que está rolando agora.
4. `agentes/MAPA.md` — quem mais opera no seu cérebro.

Esses quatro são leitura obrigatória. Já são carregados automaticamente pelo `MEMORY.md` que o instalador criou.

## Quando abrir o resto

| Se a tarefa envolver... | Abra... |
|---|---|
| Regra de comportamento específica | `negocio/governanca/regras/<arquivo>.md` |
| Decisão estratégica passada | `negocio/governanca/decisoes/AAAA-MM.md` |
| Algo que já deu errado antes | `negocio/governanca/licoes/AAAA-MM.md` |
| Sistema externo (API, plataforma) | `negocio/governanca/referencias/<sistema>.md` |
| Detalhe de um produto | `negocio/produtos/<slug>/` |
| Detalhe de um sistema interno | `negocio/infra/<sistema>/` |
| Conteúdo já produzido | `acervo/` |
| Vida pessoal | `pessoal/` (só se autorizado em `seguranca/permissoes.md`) |

## Quando NÃO abrir

- Não vasculhar pastas inteiras "por garantia". O custo é alto e a chance de achar algo relevante por acidente é baixa.
- Não abrir `pessoal/` se a tarefa é de trabalho.
- Não reler `MAPA.md` no meio da sessão se já leu no início. Se ficou em dúvida, perguntar.

## Como aplicar

- Sempre que iniciar a tarefa, decidir: "preciso de mais que os 4 âncora?". Se sim, listar pra você quais arquivos vai abrir e por quê.
- Se a IA estiver perdida e abrindo arquivo demais, você pode interromper com "fecha tudo e me diz o que precisa saber".
