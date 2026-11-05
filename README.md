# Organizador de chamados

Aplicacao em Python para organizar mensagens informais de suporte tecnico utilizando um modelo de linguagem.

## Problema

Relatos de suporte frequentemente chegam com informacoes incompletas, linguagem informal e descricoes pouco organizadas.

## Objetivo

Transformar esses relatos em fichas de atendimento com informacoes claras e padronizadas.

## Escopo

- Entrada de texto pelo terminal
- Interpretacao por modelo de linguagem
- Organizacao das informacoes
- Apresentacao de uma ficha de atendimento

A aplicacao nao realiza diagnosticos automaticos nem executa correcoes nos equipamentos.

## Desenvolvimento

O projeto sera desenvolvido progressivamente, com validacao de cada etapa antes da integracao na branch principal.

## Privacidade e segurança

Os exemplos utilizados no projeto são fictícios. As credenciais de acesso ao modelo são mantidas em variáveis de ambiente e não são incluídas no repositório.

## Instalacao e execucao

Requer Python 3.10 ou superior.

No PowerShell, execute na pasta do projeto:

    py -3 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    Copy-Item .env.example .env
    notepad .env
    .\.venv\Scripts\python.exe main.py

Preencha o arquivo .env com os dados do provedor escolhido.
Nao publique credenciais reais.

## Exemplo de utilizacao

Entrada: A impressora da recepcao nao imprime documentos.

Saida esperada: categoria, problema, contexto e informacoes faltantes.
A resposta real pode variar conforme o modelo.

## Testes

Execute:

    .\.venv\Scripts\python.exe -m unittest discover -s tests -v

Os testes automatizados simulam respostas e falhas da API.
Incluem credencial ausente, credencial invalida, timeout e indisponibilidade.
Nao realizam chamadas reais ao LLM.

A integracao real e verificada executando main.py com acesso valido.

## Limitacoes

A aplicacao nao realiza diagnosticos nem corrige equipamentos.
A qualidade das respostas depende do modelo utilizado.
A API institucional precisa ser compativel com Chat Completions.
Quando configurado, o institucional e consultado primeiro.
Caso falhe, a NVIDIA e utilizada como alternativa.
O mesmo texto pode ser enviado aos dois servicos.

## Video

Link da demonstracao final: pendente.
