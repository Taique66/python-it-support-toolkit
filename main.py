import platform
import os
import shutil
import psutil
import socket
import subprocess
import json
import json

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

def consultar_portas():
    portas = []

    try:
        for conexao in psutil.net_connections(kind="tcp"):
            if conexao.status == psutil.CONN_LISTEN:
                portas.append({
                    "ip": conexao.laddr.ip,
                    "porta": conexao.laddr.port,
                    "pid": conexao.pid
                })

        return {"portas": portas, "erro": None}

    except psutil.AccessDenied:
        return {
            "portas": portas,
            "erro": "Sem permissão para consultar as conexões TCP."
        }

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

print("\n=== Portas TCP locais em escuta ===")
print("A listagem pode ser parcial, conforme as permissões.")

dados_portas = consultar_portas()

if dados_portas["erro"] is not None:
    print(dados_portas["erro"])
else:
    for porta in dados_portas["portas"]:
        print(
            "IP:", porta["ip"],
            "Porta:", porta["porta"],
            "PID:", porta["pid"]
        )

    print("Total de registros em escuta:", len(dados_portas["portas"]))

filtro = input(
    "Nome do processo (Enter para listar todos): "
).strip().lower()

dados_processos = consultar_processos(filtro)

print("\n=== Processos encontrados ===")

for processo in dados_processos:
    memoria_mib = processo["memoria_mib"]

    if memoria_mib is not None:
        print(
            processo["pid"],
            processo["nome"],
            f"RAM: {memoria_mib:.2f} MiB"
        )
    else:
        print(processo["pid"], processo["nome"], "RAM: indisponível")

if not dados_processos:
    print("Nenhum processo encontrado.")
else:
    print("Total de processos encontrados:", len(dados_processos))

print("\n=== Teste TCP da porta 22 da VM ===")

dados_tcp = testar_tcp(destino, 22)

if dados_tcp["sucesso"]:
    print("Conexão TCP aceita na porta 22.")
else:
    print("Não foi possível conectar à porta 22:", dados_tcp["erro"])

relatorio = {
    "sistema": dados_sistema,
    "memoria": dados_memoria,
    "disco": dados_disco,
    "cpu": dados_cpu,
    "interfaces": dados_interfaces,
    "ping": dados_ping,
    "dns": dados_dns,
    "processos": {
        "filtro": filtro,
        "resultados": dados_processos
    },
    "portas_tcp": dados_portas,
    "teste_tcp": dados_tcp
}

try:
    with open("report.json", "w", encoding="utf-8") as arquivo:
        json.dump(relatorio, arquivo, indent=4, ensure_ascii=False)

    print("\nRelatório salvo em report.json.")
except OSError as erro:
    print("\nNão foi possível salvar o relatório:", erro)