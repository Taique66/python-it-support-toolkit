import platform
import os
import shutil

print("=== Python IT Support Toolkit ===")

disco = shutil.disk_usage("/")
total_gib = disco.total / (1024 ** 3)
livre_gib = disco.free / (1024 ** 3)
usado_gib = disco.used / (1024 ** 3)

print("Espaço total do disco:", f"{total_gib:.2f} GiB")
print("Espaço usado do disco:", f"{usado_gib:.2f} GiB")
print(f"Espaço livre do disco: {livre_gib:.2f} GiB")

if livre_gib < 10:
    print("ALERTA: menos de 10 GiB livres.")
else:
    print("Espaço livre acima ou igual a 10 GiB")


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