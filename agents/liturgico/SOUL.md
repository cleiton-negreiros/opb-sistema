# ⛪ Agente Litúrgico - SOUL.md

## Identidade

**Nome:** Litúrgico

**Propósito:** Gerar sugestões de conteúdo alinhadas ao calendário litúrgico católico, combinando datas e temas litúrgicos com educação financeira para o projeto "Paz na Conta".

## Como Funciona

O agente Litúrgico:

1. **Calcula datas litúrgicas** programaticamente usando o algoritmo de Easter (Páscoa) gregoriano
2. **Determina o tempo litúrgico** atual (Advento, Natal, Quaresma, Páscoa, Tempo Comum)
3. **Consulta o calendário** com santos, festas e solenidades relevantes
4. **Combina temas litúrgicos** com finanças pessoais (dízimo, orçamento, caridade, etc.)
5. **Gera sugestões de conteúdo** em formato markdown
6. **Salva no acervo** para consulta posterior (`acervo/ideias/`)
7. **Integra com Ollama** para geração de conteúdo com IA (opcional)

## Uso

```bash
# Tema para hoje
python main.py hoje

# Temas da semana
python main.py semana

# Temas do mês
python main.py mes

# Tempo litúrgico atual
python main.py tempo

# Próximas datas importantes
python main.py datas

# Sugestões de conteúdo
python main.py sugerir
python main.py sugerir "dízimo"

# Conteúdo sobre um santo
python main.py santo "José"
python main.py santo "Mateus"

# Gerar com Ollama
python main.py ollama
python main.py ollama "Crie um post sobre dízimo na Quaresma"

# Ajuda
python main.py ajuda
```

## Temas Financeiros Católicos

O agente combina liturgia com estes temas:

- Dízimo e generosidade cristã
- Orçamento familiar à luz do Evangelho
- Caridade e justiça social
- Desapego material e liberdade financeira
- Trabalho como vocação
- Investimento ético e responsável
- Superando dívidas com fé e disciplina
- Poupança com propósito
- Administração como mordomia cristã
- Doutrina Social da Igreja aplicada às finanças

## Santos Relevantes

O agente possui dados sobre santos ligados a finanças/trabalho:

- **São José** - Provedor, trabalhador, patrono das famílias
- **São Mateus** - Patrono dos profissionais de finanças
- **São Bento** - Equilíbrio entre trabalho e oração
- **São Vicente de Paulo** - Caridade organizada
- **São Francisco de Assis** - Desapego e simplicidade
- **São Tomás de Aquino** - Teologia econômica
- **Santa Clara** - Pobreza voluntária
- **Santo Antônio** - Generosidade com os pobres

## Integração com Outros Agentes

### Agente Carrossel
```bash
# Gerar tema litúrgico
python main.py hoje > tema.txt

# Usar no agente carrossel
python ../carrossel/main.py --tema "$(cat tema.txt)"
```

### Agente Text Generator
```bash
# Obter tema
python main.py sugerir "dízimo" > ideias.txt

# Gerar texto completo
python ../text_generator/main.py --input ideias.txt
```

### Agente Content Planner
```bash
# Temas do mês
python main.py mes > calendario_mes.txt

# Planejar conteúdo
python ../content_planner/main.py --calendario calendario_mes.txt
```

### Pipeline Completo
```bash
# 1. Obter tema do dia
python main.py hoje

# 2. Gerar ideias
python main.py sugerir

# 3. Gerar conteúdo com Ollama
python main.py ollama

# 4. Salva automaticamente em acervo/ideias/
```

## Estrutura de Arquivos

```
agents/liturgico/
├── main.py              # Script principal
├── calendario.json      # Calendário litúrgico 2026-2027
├── SOUL.md              # Este arquivo
├── STATUS.md            # Status do agente
├── requirements.txt     # Dependências
└── acervo/
    └── ideias/          # Ideias geradas salvas aqui
```

## Compatibilidade

- **PC (Windows/Linux/Mac):** Python 3.6+
- **Termux (Android):** Python 3, sem dependências externas obrigatórias
- **Ollama:** Opcional, para geração de conteúdo com IA

## Notas

- Não requer conexão com internet (exceto Ollama)
- Cálculo de Páscoa usa algoritmo gregoriano anônimo
- Calendário segue o rito romano da Igreja Católica
- Temas financeiros alinhados com Doutrina Social da Igreja
