import platform
import os

print("=== Python IT Support Toolkit ===")

num_cores = os.cpu_count()

print("CPUs lógicas:", num_cores)

sistema = platform.system()

print("Meu computador usa:", sistema)

nome_maquina = platform.node()
print("Nome da máquina:", nome_maquina)

versao_sistema = platform.release()
print("Versão do kernel:", versao_sistema)