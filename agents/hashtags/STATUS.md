# OPB Hashtag Generator - STATUS

## Status: PRODUCTION READY

## Features
- [x] 3-tier hashtag generation (Popular, Medium, Niche)
- [x] Topic-based generation
- [x] Pillar-based generation
- [x] Multiple variations (--blocos)
- [x] Export to file (--exportar)
- [x] Built-in database (200+ hashtags)
- [x] Ollama integration (optional)
- [x] Save to output/ and acervo/ideias/
- [x] Cross-platform (PC + Termux)
- [x] Copy-paste ready output

## Database
- 4 pillars: espiritual, pratico, testemunho, dsi
- Finance subcategories: dizimo, orcamento, dividas, investimento, caridade
- Catholic subcategories: fe, igreja, evangelho, maria, santos

## Usage Examples
```bash
python main.py "dizimo e organizacao financeira"
python main.py --pilar espiritual
python main.py --pilar pratico --blocos 3
python main.py "dizimo" --exportar
python main.py "fe e financas" --sem-ollama
```

## Dependencies
- Python 3.7+
- requests (optional, for Ollama)

## Notes
- Works offline without Ollama
- Database can be expanded by editing hashtags_db.json
- Output files saved with timestamps for tracking
