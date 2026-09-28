import platform

sistema = platform.system()

print("Meu computador usa:", sistema)

nome_maquina = platform.node()
print("Nome da máquina:", nome_maquina)

versao_sistema = platform.release()
print("Versão do sistema operacional:", versao_sistema)