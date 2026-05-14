import subprocess
import sys

result = subprocess.run(
    ['tasklist', '/FI', 'imagename eq python.exe'],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)
if 'telegram_bot' in result.stdout.lower() or 'main.py' in result.stdout.lower():
    print("Bot esta rodando!")
else:
    print("Bot NAO encontrado nos processos")
print(result.stdout[:500])