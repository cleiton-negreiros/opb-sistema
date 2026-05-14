import subprocess
import sys

# Mata TODOS os processos python relacionados
result = subprocess.run(
    ['taskkill', '/F', '/IM', 'python.exe'],
    capture_output=True, text=True
)
print("Processos mortos:", result.stdout[:200] if result.stdout else "Nenhum encontrado")
print("Pronto para reiniciar")