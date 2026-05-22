# OPB Reels Script Generator - STATUS

## Status: PRODUCTION READY

## Features
- [x] 3-part script structure (Gancho + Conteudo + CTA)
- [x] Multiple durations: 30s, 60s, 90s
- [x] Multiple formats: reels, shorts, tiktok
- [x] Multiple variations (--variacoes)
- [x] Export to file (--exportar)
- [x] Visual suggestions
- [x] Text overlay suggestions
- [x] Platform-specific tips
- [x] Ollama integration (optional)
- [x] Save to output/ and acervo/ideias/
- [x] Cross-platform (PC + Termux)

## Script Structure
| Duration | Gancho | Conteudo | CTA |
|----------|--------|----------|-----|
| 30s      | 3s     | 20s      | 7s  |
| 60s      | 5s     | 45s      | 10s |
| 90s      | 7s     | 70s      | 13s |

## Usage Examples
```bash
python main.py "3 erros financeiros que catolicos cometem"
python main.py "como organizar orcamento familiar" --duracao 60
python main.py "dizimo e prosperidade" --formato shorts
python main.py "financas com proposito" --variacoes 3
python main.py "dizimo" --exportar
python main.py "fe e dinheiro" --sem-ollama
```

## Dependencies
- Python 3.7+
- requests (optional, for Ollama)

## Notes
- Works offline without Ollama
- Built-in templates for Catholic finance content
- Can be extended with more templates and visual suggestions
- Output files saved with timestamps for tracking
