import platform
import os
import shutil
import psutil
import socket
import subprocess

def consultar_sistema():
    return {
        "sistema": platform.system(),
        "nome_maquina": platform.node(),
        "kernel": platform.release()
    }
print("=== Python IT Support Toolkit ===")

def consultar_memoria():
    memoria = psutil.virtual_memory()
    return {
        "total_gib": memoria.total / (1024 ** 3),
        "disponivel_gib": memoria.available / (1024 ** 3),
        "uso_percentual": memoria.percent
    }

dados_sistema = consultar_sistema()

print("Meu computador usa:", dados_sistema["sistema"])
print("Nome da máquina:", dados_sistema["nome_maquina"])
print("Versão do kernel:", dados_sistema["kernel"])

dados_memoria = consultar_memoria()
ram_total_gib = dados_memoria["total_gib"]
ram_disponivel_gib = dados_memoria["disponivel_gib"]
uso_ram = dados_memoria["uso_percentual"]

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
uso_cpu = psutil.cpu_percent(interval=1)
print(f"Uso da CPU: {uso_cpu:.2f}%")

if num_cores >= 8:   
     print("O sistema reconhece 8 ou mais CPUs lógicas.")
else:
     print("O sistema reconhece menos de 8 CPUs lógicas.")

print("CPUs lógicas:", num_cores)

interfaces = psutil.net_if_addrs()

for nome in interfaces:
    print("Interface:", nome)

    for endereco in interfaces[nome]:
        if endereco.family == socket.AF_INET:
            print("  IPv4:", endereco.address)

resultado_ping = subprocess.run(
    ["ping", "-c", "4", "192.168.122.223"]
)

print("Código de saída:", resultado_ping.returncode)

if resultado_ping.returncode == 0:
    print("Ping bem-sucedido.")
else:
    print("Falha no ping.")
