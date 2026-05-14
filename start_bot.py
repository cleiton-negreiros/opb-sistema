import subprocess
import sys
import time

bot_path = r"C:\Users\cleit\Desktop\opb-sistema\agents\telegram_bot\main.py"

proc = subprocess.Popen(
    [sys.executable, bot_path],
    cwd=r"C:\Users\cleit\Desktop\opb-sistema",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    encoding='utf-8',
    errors='replace'
)
print(f"Bot iniciado com PID: {proc.pid}")
time.sleep(5)
if proc.poll() is None:
    print("Bot ainda rodando!")
else:
    out, err = proc.communicate()
    print("STDOUT:", out[:500])
    print("STDERR:", err[:500] if err else "(vazio)")