import platform
import os
import shutil
import psutil

print("=== Python IT Support Toolkit ===")

memoria = psutil.virtual_memory()
ram_total_gib = memoria.total / (1024 ** 3)
ram_disponivel_gib = memoria.available / (1024 ** 3)
uso_ram = 85

print("Memória total:", f"{ram_total_gib:.2f} GiB")
print("Memória disponível:", f"{ram_disponivel_gib:.2f} GiB")
print(f"Uso da RAM: {uso_ram:.2f}%")
if uso_ram > 80:
    print("ALERTA: Uso da RAM acima de 80%.")
else:
    print("Uso da RAM abaixo ou igual a 80%.")


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