import subprocess
import time
import sys

# Mata o servidor antigo se estiver rodando
result = subprocess.run(
    ['taskkill', '/F', '/FI', 'windowtitle eq OPB API Server'],
    capture_output=True, text=True
)
time.sleep(2)

# Inicia servidor novo
proc = subprocess.Popen(
    [sys.executable, r"C:\Users\cleit\Desktop\opb-sistema\api_server.py"],
    cwd=r"C:\Users\cleit\Desktop\opb-sistema",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    encoding='utf-8',
    errors='replace'
)
print(f"Servidor iniciado com PID: {proc.pid}")
time.sleep(3)

# Verifica se está rodando
if proc.poll() is None:
    print("✅ Servidor rodando!")
else:
    out, err = proc.communicate()
    print("❌ Servidor morreu!")
    print("STDOUT:", out[:500])
    print("STDERR:", err[:500] if err else "(vazio)")