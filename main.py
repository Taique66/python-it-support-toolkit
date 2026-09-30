import platform
import os
import shutil
import psutil
import socket
import subprocess

def consultar_disco():
    disco = shutil.disk_usage("/")
    return {
        "total_gib": disco.total / (1024 ** 3),
        "usado_gib": disco.used / (1024 ** 3),
        "livre_gib": disco.free / (1024 ** 3)
    }

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
def consultar_cpu():
    return {
        "cpus_logicas": os.cpu_count(),
        "uso_percentual": psutil.cpu_percent(interval=1)
    }


def consultar_interfaces():
    resultado = []

    for nome, enderecos in psutil.net_if_addrs().items():
        ips = []

        for endereco in enderecos:
            if endereco.family == socket.AF_INET:
                ips.append(endereco.address)

        resultado.append({
            "nome": nome,
            "ipv4": ips
        })

    return resultado
def consultar_processos(filtro):
    encontrados = []

    for processo in psutil.process_iter(["pid", "name", "memory_info"]):
        nome = processo.info["name"] or ""

        if filtro in nome.lower():
            memoria = processo.info["memory_info"]
            memoria_mib = None

            if memoria is not None:
                memoria_mib = memoria.rss / (1024 ** 2)

            encontrados.append({
                "pid": processo.info["pid"],
                "nome": nome,
                "memoria_mib": memoria_mib
            })

    return encontrados

def consultar_dns(dominio):
    try:
        ip = socket.gethostbyname(dominio)
        return {
            "dominio": dominio,
            "ipv4": ip,
            "sucesso": True,
            "erro": None
        }
    except socket.gaierror as erro:
        return {
            "dominio": dominio,
            "ipv4": None,
            "sucesso": False,
            "erro": str(erro)
        }


def testar_tcp(destino, porta):
    try:
        with socket.create_connection((destino, porta), timeout=3):
            return {
                "destino": destino,
                "porta": porta,
                "sucesso": True,
                "erro": None
            }
    except OSError as erro:
        return {
            "destino": destino,
            "porta": porta,
            "sucesso": False,
            "erro": str(erro)
        }
def testar_ping(destino):
    try:
        resultado = subprocess.run(
            ["ping", "-c", "4", "-w", "5", "--", destino],
            timeout=7
        )

        return {
            "destino": destino,
            "sucesso": resultado.returncode == 0,
            "codigo": resultado.returncode
        }

    except FileNotFoundError:
        return {
            "destino": destino,
            "sucesso": False,
            "codigo": None
        }

    except subprocess.TimeoutExpired:
        return {
            "destino": destino,
            "sucesso": False,
            "codigo": None
        }

dados_sistema = consultar_sistema()

print("Meu computador usa:", dados_sistema["sistema"])
print("Nome da máquina:", dados_sistema["nome_maquina"])
print("Versão do kernel:", dados_sistema["kernel"])

dados_memoria = consultar_memoria()

print("Memória total:", f"{dados_memoria['total_gib']:.2f} GiB")
print("Memória disponível:", f"{dados_memoria['disponivel_gib']:.2f} GiB")
print("Uso da RAM:", f"{dados_memoria['uso_percentual']:.2f}%")

if dados_memoria["uso_percentual"] > 80:
    print("ALERTA: Uso da RAM acima de 80%.")
else:
    print("Uso da RAM abaixo ou igual a 80%.")

dados_disco = consultar_disco()

print("Espaço total do disco:", f"{dados_disco['total_gib']:.2f} GiB")
print("Espaço usado do disco:", f"{dados_disco['usado_gib']:.2f} GiB")
print("Espaço livre do disco:", f"{dados_disco['livre_gib']:.2f} GiB")

if dados_disco["livre_gib"] < 10:
    print("ALERTA: menos de 10 GiB livres.")
else:
    print("Espaço livre acima ou igual a 10 GiB")

dados_cpu = consultar_cpu()

print(f"Uso da CPU: {dados_cpu['uso_percentual']:.2f}%")
print("CPUs lógicas:", dados_cpu["cpus_logicas"])

dados_interfaces = consultar_interfaces()

for interface in dados_interfaces:
    print("Interface:", interface["nome"])

    if interface["ipv4"]:
        for ip in interface["ipv4"]:
            print("  IPv4:", ip)
    else:
        print("  Sem IPv4 atribuído.")

destino = input("IP da VM [192.168.122.223]: ").strip()
if not destino:
    destino = "192.168.122.223"
    
dados_ping = testar_ping(destino)

if dados_ping["sucesso"]:
    print("Ping bem-sucedido.")
else:
    print("Falha no ping.")

dominio = input("Domínio para consulta [example.com]: ").strip()
if not dominio:
    dominio = "example.com"

dados_dns = consultar_dns(dominio)

if dados_dns["sucesso"]:
    print("Domínio:", dados_dns["dominio"])
    print("IPv4 encontrado:", dados_dns["ipv4"])
else:
    print("Falha ao resolver o domínio:", dados_dns["erro"])

print("\n=== Teste TCP da porta 22 da VM ===")

dados_tcp = testar_tcp(destino, 22)

if dados_tcp["sucesso"]:
    print("Conexão TCP aceita na porta 22.")
else:
    print("Não foi possível conectar à porta 22:", dados_tcp["erro"])