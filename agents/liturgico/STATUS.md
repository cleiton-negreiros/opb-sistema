# ⛪ Agente Litúrgico - STATUS.md

## Status: ✅ Concluído

Agente funcional e pronto para uso em PC e Termux.

## Features Implementadas

### Comandos Principais
- ✅ `python main.py hoje` - Tema litúrgico de hoje
- ✅ `python main.py semana` - Temas para a semana
- ✅ `python main.py mes` - Temas para o mês
- ✅ `python main.py tempo` - Tempo litúrgico atual com datas móveis
- ✅ `python main.py datas` - Próximas datas litúrgicas importantes
- ✅ `python main.py sugerir` - Sugestões de conteúdo litúrgico-financeiro
- ✅ `python main.py sugerir "tema"` - Sugestões sobre tema específico
- ✅ `python main.py santo "nome"` - Conteúdo sobre santo específico
- ✅ `python main.py ollama` - Geração de conteúdo com Ollama (opcional)
- ✅ `python main.py ajuda` - Ajuda completa

### Funcionalidades Técnicas
- ✅ Cálculo da Páscoa (algoritmo Gregoriano Anônimo)
- ✅ Cálculo de datas móveis (Cinzas, Ramos, Ascensão, Pentecostes, Corpus Christi)
- ✅ Cálculo do 1º Domingo do Advento
- ✅ Determinação automática do tempo litúrgico
- ✅ Banco de dados de santos (14 santos relevantes para finanças/trabalho)
- ✅ Banco de festas e solenidades fixas
- ✅ Temas financeiros por tempo litúrgico
- ✅ Doutrina Social da Igreja (8 temas)
- ✅ Temas por mês litúrgico
- ✅ Salvamento automático em `acervo/ideias/`
- ✅ Output em formato markdown
- ✅ Compatível com PC e Termux
- ✅ Sem dependências externas obrigatórias

### Calendário
- ✅ Temporais litúrgicos 2026-2027 com datas
- ✅ 14 festas e solenidades fixas
- ✅ 14 santos com biografia e temas financeiros
- ✅ 8 temas da Doutrina Social da Igreja
- ✅ Temas financeiros por mês

## Dependências
- Python 3.6+
- python-dotenv (opcional)
- Ollama (opcional, para IA)

## TODO - Melhorias Futuras

### Curto Prazo
- [ ] Adicionar mais santos ao calendário
- [ ] Incluir leituras do dia (API ou banco local)
- [ ] Suporte a calendário de santos locais (Brasil)
- [ ] Exportar calendário para PDF

### Médio Prazo
- [ ] Integração com Google Calendar
- [ ] Notificações automáticas de datas importantes
- [ ] Template de posts para cada tempo litúrgico
- [ ] Banco de citações bíblicas sobre finanças
- [ ] Suporte a múltiplos idiomas (PT/EN/ES)

### Longo Prazo
- [ ] Interface web simples
- [ ] App mobile (Termux friendly)
- [ ] Integração com APIs de Bíblia
- [ ] Machine learning para sugestões personalizadas
- [ ] Calendário interativo com visualização gráfica

## Histórico

| Data | Versão | Mudança |
|------|--------|---------|
| 21/05/2026 | 1.0 | Criação inicial do agente |
