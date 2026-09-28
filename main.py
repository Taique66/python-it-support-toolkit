import platform
import os

print("=== Python IT Support Toolkit ===")

num_cores = os.cpu_count()

if num_cores >= 8:   
     print("O sistema reconhece 8 ou mais CPUs lógicas.")
else:
     print("O sistema reconhece menos de 8 CPUs lógicas.")

print("CPUs lógicas:", num_cores)

sistema = platform.system()

print("Meu computador usa:", sistema)

nome_maquina = platform.node()
print("Nome da máquina:", nome_maquina)

versao_sistema = platform.release()
print("Versão do kernel:", versao_sistema)