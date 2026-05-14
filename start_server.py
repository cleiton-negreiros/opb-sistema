import subprocess
import sys
import time

print("Iniciando servidor Flask...")

proc = subprocess.Popen(
    [sys.executable, r"C:\Users\cleit\Desktop\opb-sistema\api_server.py"],
    cwd=r"C:\Users\cleit\Desktop\opb-sistema",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    encoding='utf-8',
    errors='replace'
)

# Le primeira saida
time.sleep(3)
if proc.poll() is None:
    print("Servidor rodando (PID:", proc.pid, ")")
else:
    out, err = proc.communicate()
    print("SERVIDOR MORREU!")
    print("STDOUT:", repr(out[:1000]))
    print("STDERR:", repr(err[:1000]) if err else "(vazio)")