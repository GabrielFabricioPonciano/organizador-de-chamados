# Organizador de Chamados

Aplicação em Python que utiliza um modelo de linguagem (LLM) para organizar mensagens de suporte técnico em fichas com categoria, problema, contexto e informações faltantes.

## Sobre o projeto

No atendimento de suporte, é comum receber mensagens incompletas ou pouco organizadas. Isso dificulta a identificação do problema e o registro do chamado.

O Organizador de Chamados recebe uma mensagem digitada no terminal e utiliza um LLM para estruturar essas informações.

- **Público:** equipes de suporte e atendimento.
- **Entrada:** mensagem de texto.
- **Saída:** ficha organizada com as informações do chamado.
- **Uso do LLM:** interpretar relatos escritos de diferentes maneiras, sem depender apenas de palavras-chave.

A aplicação não realiza diagnósticos, não corrige equipamentos e não armazena chamados.

## Estrutura do projeto

| Arquivo | Função |
|---|---|
| `main.py` | Executa a aplicação e recebe a mensagem. |
| `llm_client.py` | Realiza a comunicação com o modelo. |
| `text_tools.py` | Valida e organiza as informações. |
| `tests/` | Contém os testes automatizados. |
| `.env.example` | Exemplo das configurações necessárias. |
| `requirements.txt` | Lista as dependências do projeto. |
| `RELATORIO_EXECUCAO.md` | Documenta o desenvolvimento e os testes. |

## Requisitos

- Python 3.10 ou superior.
- Bibliotecas `requests` e `python-dotenv`.
- Chave de API válida para executar consultas reais.

O projeto foi desenvolvido e testado no Windows com Python 3.13.0.

## Instalação

Abra o PowerShell e execute:

```powershell
git clone https://github.com/GabrielFabricioPonciano/organizador-de-chamados.git
cd organizador-de-chamados

py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

Copy-Item .env.example .env
notepad .env
```

No arquivo `.env`, configure sua chave de API. O `.env.example` já apresenta as configurações necessárias para utilizar a NVIDIA.

**Não publique o arquivo `.env`, pois ele contém informações de acesso.**

## Modelo utilizado

A NVIDIA foi o provedor utilizado nas execuções reais do projeto e apresentou os resultados esperados.

O projeto também permite configurar um serviço institucional compatível com a API Chat Completions. Quando configurado, o programa tenta utilizá-lo primeiro e pode recorrer à NVIDIA em caso de falha.

Embora o serviço institucional esteja disponível atualmente, optei por continuar utilizando a NVIDIA, pois foi o provedor validado durante o desenvolvimento. A integração institucional não foi testada neste projeto.

As principais configurações podem ser ajustadas no `.env`:

| Configuração | Padrão |
|---|---|
| `LLM_TIMEOUT` | 30 segundos |
| `LLM_MAX_TOKENS` | 1024 |
| `LLM_TEMPERATURE` | 0.2 |

## Como executar

Com o ambiente configurado, execute:

```powershell
.\.venv\Scripts\python.exe main.py
```

Exemplo de mensagem:

> A impressora do escritório não está imprimindo. Já reiniciei o equipamento, mas o problema continua.

A aplicação deverá gerar uma ficha semelhante a esta:

**Categoria:** Impressora

**Problema:** Equipamento não está imprimindo.

**Contexto:** O usuário já tentou reiniciar a impressora.

**Informações faltantes:** Modelo da impressora, mensagens de erro e tipo de conexão.

Esse é um exemplo ilustrativo. A resposta pode variar conforme o modelo.

## Testes

Os testes automatizados podem ser executados sem utilizar uma chave de API:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Eles verificam situações como:

- Entrada válida e entrada vazia.
- Credenciais ausentes ou inválidas.
- Falhas de comunicação e timeout.
- Respostas inesperadas da API.
- Configurações externas e funcionamento dos logs.

Durante o desenvolvimento, foram aprovados **14 testes no Intermediário e 20 no Avançado**.

A versão Avançada também foi validada em um ambiente virtual novo e em um clone independente do GitHub, com os 20 testes aprovados.

Além dos testes simulados, foram realizadas chamadas reais à NVIDIA para verificar a geração das fichas.

## Segurança e limitações

As credenciais ficam em variáveis de ambiente e não são incluídas no repositório.

Os logs registram eventos e categorias de erros, sem armazenar as mensagens completas ou as chaves de API.

Como as mensagens podem ser enviadas a um provedor externo, não utilize dados pessoais ou informações confidenciais nos testes.

O modelo pode interpretar alguma informação incorretamente ou deixar detalhes de fora. Por isso, as fichas devem ser conferidas antes de serem utilizadas.

## Evolução do projeto

O desenvolvimento foi dividido em três níveis:

- **Básico — `p0-basico`:** aplicação inicial e integração com o LLM.
- **Intermediário — `p0-intermediario`:** organização do código, tratamento de erros e testes.
- **Avançado — `p0-avancado`:** configurações externas, logs e validação em ambiente independente.

O histórico de commits e pull requests está disponível neste repositório.

A tag `p0-entrega-final` identifica a versão com a documentação finalizada.

## Relatório e vídeo

O desenvolvimento, as decisões técnicas, os resultados dos testes e as reflexões estão documentados no [Relatório de Execução](RELATORIO_EXECUCAO.md).

**Vídeo de demonstração:** https://youtu.be/teuFhgPCauc

## Autor

Gabriel Fabrício Ponciano

Projeto desenvolvido para o P0 do curso SOFTEX TrendsIA.
