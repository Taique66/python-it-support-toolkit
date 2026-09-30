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

try:
    resultado_ping = subprocess.run(
        ["ping", "-c", "4", "-w", "5", "--", destino],
        timeout=7
    )

    if resultado_ping.returncode == 0:
        print("Ping bem-sucedido.")
    else:
        print("Falha no ping.")

except FileNotFoundError:
    print("O comando ping não está instalado.")
except subprocess.TimeoutExpired:
    print("O ping ultrapassou o limite de tempo.")

dominio = "example.com"

try:
    ip_resolvido = socket.gethostbyname(dominio)
    print("Domínio:", dominio)
    print("IPv4 encontrado:", ip_resolvido)
except socket.gaierror:
    print("Falha ao resolver o domínio:", dominio)


filtro = input(
    "Nome do processo (Enter para listar todos): "
).strip().lower()

dados_processos = consultar_processos(filtro)

print("=== Processos encontrados ===")

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

print("\n=== Portas TCP locais em escuta ===")
print("A listagem pode ser parcial, conforme as permissões.")

try:
    conexoes = psutil.net_connections(kind="tcp")
    quantidade_portas = 0

    for conexao in conexoes:
        if conexao.status == psutil.CONN_LISTEN:
            print(
                "IP:", conexao.laddr.ip,
                "Porta:", conexao.laddr.port,
                "PID:", conexao.pid
            )
            quantidade_portas += 1

    print("Total de registros em escuta:", quantidade_portas)

except psutil.AccessDenied:
    print("Sem permissão para consultar as conexões TCP.")

print("\n=== Teste TCP da porta 22 da VM ===")

try:
    with socket.create_connection((destino, 22), timeout=3):
        print("Conexão TCP aceita na porta 22.")
except OSError as erro:
    print("Não foi possível conectar à porta 22:", erro)