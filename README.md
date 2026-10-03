# Python IT Support Toolkit

Toolkit de terminal em Python para diagnóstico de sistema e rede em Linux, criado para praticar atividades de **Suporte de TI, Infraestrutura e NOC**.

A aplicação coleta informações do computador, executa testes básicos de conectividade e exporta os resultados para um relatório JSON com data e hora.

**Status: v1 concluída.**

## Competências demonstradas

- Diagnóstico de Linux.
- Troubleshooting básico de sistema e rede.
- TCP/IP, DNS, ping e testes de conectividade.
- Portas TCP e validação da porta 22/SSH.
- Processos e consumo de memória.
- Automação com Python.
- Estruturação de dados e relatórios em JSON.
- Tratamento básico de erros.
- Git e documentação técnica.
- Testes automatizados com `unittest` e mocks.

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
- Relatórios JSON na pasta `reports/`, com data e hora no nome e preservação das execuções anteriores.

## Tecnologias

Python, psutil, Linux, Git e JSON.

Módulos da biblioteca padrão utilizados: `platform`, `os`, `shutil`, `socket`, `subprocess`, `json`, `datetime`, `pathlib` e `unittest`.

## Ambiente testado

- CachyOS Linux.
- Python 3.14.7.
- psutil 7.2.2.
- Ubuntu Server em uma VM KVM/QEMU para os testes de conectividade.

## Instalação

É necessário ter Git, Python 3 com suporte a ambientes virtuais, pip e o comando `ping` disponível no Linux.

Os comandos abaixo usam Bash ou Zsh:

```bash
git clone https://github.com/guilhermesantosbarros/python-it-support-toolkit.git
cd python-it-support-toolkit
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

No Fish:

```fish
source .venv/bin/activate.fish
```

A dependência externa está registrada em `requirements.txt`. Os demais módulos acompanham o Python.

## Como usar

Com o ambiente virtual ativo:

```bash
python main.py
```

O programa solicita:

| Entrada | Comportamento |
| --- | --- |
| IP ou hostname de destino | Campo obrigatório utilizado no ping e no teste TCP da porta 22. Rejeita entradas com espaços ou iniciadas por `-`. |
| Domínio | Enter consulta `example.com`. Também é possível informar outro domínio. |
| Nome do processo | Filtra por parte do nome, sem diferenciar maiúsculas e minúsculas. Enter lista todos os processos acessíveis. |

O destino não fica mais preso ao endereço IP do homelab usado durante o desenvolvimento, permitindo testar outras máquinas e ambientes.

## Relatório JSON

Ao final, o programa cria a pasta `reports/` no diretório de onde foi executado e salva um JSON com data, hora e microssegundos no nome, como `report_20261003_131144_278533.json`. Cada execução preserva os relatórios anteriores. A função `salvar_relatorio()` concentra a gravação e devolve o caminho do arquivo criado.

O arquivo reúne:

- `gerado_em`: data e hora de montagem do relatório, com fuso horário;
- `sistema`, `memoria`, `disco` e `cpu`: informações do computador;
- `interfaces`: interfaces e seus endereços IPv4;
- `ping` e `dns`: resultados dos testes de rede;
- `processos`: filtro utilizado e processos encontrados;
- `portas_tcp`: registros locais em escuta e eventual erro de permissão;
- `teste_tcp`: resultado da conexão na porta 22.

O relatório reutiliza os dados coletados durante a execução. As medições acontecem em momentos diferentes; o horário de geração não representa uma coleta simultânea.

A pasta `reports/` e o arquivo legado `report.json` estão no `.gitignore`, pois podem conter dados do ambiente.

## Testes automatizados

A pasta `tests/` contém 10 testes para as funções de rede, a entrada do destino e a gravação dos relatórios. Os testes de rede usam mocks; os de gravação usam pastas temporárias. Não dependem de acesso real à internet.

Execute:

```bash
python -m unittest discover -s tests -v
```

Atualmente são verificados cenários de:

- resolução DNS com sucesso e falha;
- conexão TCP com sucesso e falha;
- ping com sucesso e timeout;
- rejeição de destino vazio, com espaços ou iniciado por `-`;
- criação da pasta e gravação correta do JSON;
- preservação dos relatórios anteriores.

## Organização

| Arquivo | Responsabilidade |
| --- | --- |
| `main.py` | Funções de consulta e teste, interação no terminal e exportação do relatório. |
| `tests/test_main.py` | Testes automatizados de rede, entrada do destino e salvamento dos relatórios. |
| `requirements.txt` | Dependência externa com versão fixada. |
| `.gitignore` | Exclusão do ambiente virtual, cache, relatório e arquivos temporários. |
| `README.md` | Apresentação e instruções de uso. |

## Validações realizadas

Além da suíte automatizada, foram realizadas verificações manuais durante o desenvolvimento:

- Coleta de sistema, RAM, disco, CPU e interfaces.
- Ping com resposta da VM e conexão aceita na porta 22.
- Resolução DNS de `google.com`.
- Consulta de `teste.invalid` com falha tratada e continuidade da execução.
- Busca por `code` com processos encontrados.
- Busca por um nome inexistente com mensagem de ausência de resultados.
- Listagem de portas TCP locais em escuta.
- Gravação de relatório JSON, inclusive em execução com falha de DNS.
- Inclusão de data e hora no relatório.
- Gravação de relatórios com nomes distintos na pasta `reports/`.
- Execução local dos 10 testes com resultado `OK`.
- Verificação das dependências no ambiente virtual com `python -m pip check`.

## Limitações

- A implementação atual foi testada no Linux. Os argumentos do ping e o caminho de disco `/` não foram adaptados para Windows.
- A listagem de conexões pode ser parcial conforme as permissões; o PID pode aparecer como `null` no relatório.
- A consulta de interfaces mostra IPv4; a listagem de portas também pode conter endereços IPv6.
- A consulta DNS retorna um IPv4 e não possui um tempo limite explícito definido pelo programa.
- O teste TCP verifica apenas se a conexão na porta 22 é aceita. Não autentica nem verifica o funcionamento completo do SSH.
- O relatório de ping guarda destino, sucesso e código de retorno; não estrutura latência ou perda de pacotes em campos próprios.
- O tratamento de erros é básico e ainda pode ser ampliado em versões futuras.
- Os testes automatizados atuais cobrem rede, entrada e relatórios; a coleta completa de métricas do sistema ainda depende de validações manuais.

## Próximos passos possíveis

A v1 está concluída. Evoluções futuras podem incluir:

- parâmetros de linha de comando;
- suporte a Windows;
- consulta de serviços `systemd`;
- estruturação de latência e perda de pacotes;
- exportação adicional em CSV;
- integração com ferramentas de monitoramento.

## Autor

Guilherme dos Santos Barros

- [GitHub](https://github.com/guilhermesantosbarros)
- [LinkedIn](https://www.linkedin.com/in/guilherme-dos-santos-barros-a551a0282/)
