# Python IT Support Toolkit

Ferramenta de terminal em Python para diagnóstico de sistema e rede em Linux. Coleta informações do computador, executa testes de conectividade e exporta os resultados para JSON com data e hora.

Projeto desenvolvido para praticar automação de suporte de TI, infraestrutura e fundamentos de segurança defensiva, com testes no próprio computador e em um homelab.

## Funcionalidades

- Sistema operacional, hostname e kernel.
- Uso de CPU e quantidade de CPUs lógicas.
- Memória RAM total, disponível e percentual de uso.
- Espaço total, usado e livre da partição raiz (`/`).
- Alertas para RAM acima de 80% e espaço livre abaixo de 10 GiB.
- Interfaces de rede e endereços IPv4.
- Teste de conectividade com quatro pacotes de ping.
- Resolução de domínio para um endereço IPv4.
- Busca de processos por parte do nome, com PID e memória RSS em MiB.
- Listagem de portas TCP locais em escuta.
- Teste de conexão TCP na porta 22 do destino informado.
- Relatório `report.json` com os resultados e o horário de geração.

## Tecnologias

Python, psutil, Linux, Git e JSON. Módulos da biblioteca padrão utilizados: `platform`, `os`, `shutil`, `socket`, `subprocess`, `json` e `datetime`.

## Ambiente testado

- CachyOS Linux.
- Python 3.14.7.
- psutil 7.2.2.
- Ubuntu Server em uma VM KVM/QEMU para os testes de conectividade.

## Instalação

É necessário ter Git, Python 3 com suporte a ambientes virtuais, pip e o comando `ping` disponível no Linux. Os comandos abaixo usam Bash ou Zsh.

```bash
git clone https://github.com/Taique66/python-it-support-toolkit.git
cd python-it-support-toolkit
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

No Fish, substitua a ativação por:

```fish
source .venv/bin/activate.fish
```

A dependência externa está registrada em `requirements.txt`. Os demais módulos acompanham o Python.

## Como usar

Com o ambiente virtual ativo, execute na pasta do projeto:

```bash
python main.py
```

O programa solicita três entradas:

| Entrada | Comportamento |
| --- | --- |
| IP da VM | Enter utiliza `192.168.122.223`, endereço do homelab usado no desenvolvimento. Informe o endereço do seu destino para outro ambiente. |
| Domínio | Enter consulta `example.com`. Também é possível informar um domínio, como `google.com`. |
| Nome do processo | Filtra por parte do nome, sem diferenciar maiúsculas e minúsculas. Enter lista todos os processos acessíveis. |

O ping e o teste TCP usam o mesmo destino. Para obter sucesso no teste da porta 22, o destino precisa estar acessível e aceitar conexões nessa porta.

## Relatório JSON

Ao final, o programa grava `report.json` no diretório de onde foi executado. Cada execução substitui o relatório anterior.

O arquivo reúne:

- `gerado_em`: data e hora de montagem do relatório, com fuso horário;
- `sistema`, `memoria`, `disco` e `cpu`: informações do computador;
- `interfaces`: interfaces e seus endereços IPv4;
- `ping` e `dns`: resultados dos testes de rede;
- `processos`: filtro utilizado e processos encontrados;
- `portas_tcp`: registros locais em escuta e eventual erro de permissão;
- `teste_tcp`: resultado da conexão na porta 22.

O relatório reutiliza os dados coletados durante a execução. As medições acontecem em momentos diferentes; o horário de geração não representa uma coleta simultânea.

Em JSON, `true` e `false` representam resultados booleanos, e `null` representa ausência de valor. Uma falha de conectividade também é um resultado de diagnóstico e pode ser registrada no arquivo.

O arquivo gerado está no `.gitignore`, pois contém dados do ambiente e muda a cada execução.

## Organização

| Arquivo | Responsabilidade |
| --- | --- |
| `main.py` | Funções de consulta e teste, interação no terminal e exportação do relatório. |
| `requirements.txt` | Dependência externa com versão fixada. |
| `.gitignore` | Exclusão do ambiente virtual, cache e relatório gerado do controle de versão. |
| `README.md` | Apresentação e instruções de uso. |

As funções retornam listas ou dicionários que o programa utiliza para apresentar os resultados e compor o relatório. O comando externo de ping também exibe sua própria saída no terminal.

## Validações realizadas

Verificações manuais durante o desenvolvimento:

- Coleta de sistema, RAM, disco, CPU e interfaces.
- Ping com resposta da VM e conexão aceita na porta 22.
- Resolução DNS de `google.com`.
- Consulta de `teste.invalid` com falha tratada e continuidade da execução.
- Busca por `code` com processos encontrados.
- Busca por um nome inexistente com mensagem de ausência de resultados.
- Listagem de portas TCP locais em escuta.
- Gravação de relatório JSON, inclusive em execução com falha de DNS.
- Inclusão de data e hora no relatório.
- Verificação das dependências no ambiente virtual com `python -m pip check`.

Essas verificações são manuais e não constituem uma suíte de testes automatizados. A instalação em um ambiente novo ainda não foi validada.

## Limitações

- A implementação atual foi testada no Linux. Os argumentos do ping e o caminho de disco `/` não foram adaptados para Windows.
- A listagem de conexões pode ser parcial conforme as permissões; o PID pode aparecer como `null` no relatório.
- A consulta de interfaces mostra IPv4; a listagem de portas também pode conter endereços IPv6.
- A consulta DNS retorna um IPv4 e não possui um tempo limite explícito definido pelo programa.
- O teste TCP verifica apenas se a conexão na porta 22 é aceita. Não autentica nem verifica o funcionamento completo do SSH.
- O relatório de ping guarda destino, sucesso e código de retorno; não estrutura latência ou perda de pacotes em campos próprios.
- O tratamento de erros é básico. Por exemplo, mudanças ou restrições de acesso aos processos durante a consulta ainda precisam de tratamento mais abrangente.
- O projeto lista processos, mas não gerencia nem consulta o estado de serviços pelo systemd.

## Autor

Guilherme dos Santos Barros

- [GitHub](https://github.com/Taique66)
- [LinkedIn](https://www.linkedin.com/in/guilherme-dos-santos-barros-a551a0282/)
