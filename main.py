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


filtro = input("Digite o nome do processo: ").strip().lower()

print("=== Processos encontrados ===")
quantidade = 0

for processo in psutil.process_iter(["pid", "name", "memory_info"]):
    nome = processo.info["name"] or ""

    if filtro in nome.lower():
        memoria = processo.info["memory_info"]

        if memoria is not None:
            memoria_mib = memoria.rss / (1024 ** 2)
            print(processo.info["pid"], nome, f"RAM: {memoria_mib:.2f} MiB")
        else:
            print(processo.info["pid"], nome, "RAM: indisponível")

        quantidade += 1

if quantidade == 0:
    print("Nenhum processo encontrado.")
else:
    print("Total de processos encontrados:", quantidade)

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