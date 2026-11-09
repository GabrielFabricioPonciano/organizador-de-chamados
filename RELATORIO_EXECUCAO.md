# Relatório de execução — Organizador de chamados

Este relatório registra o desenvolvimento do P0. Os itens pendentes devem ser confirmados antes da entrega final.

## Evolução

- **Básico:** entrada pelo terminal, envio a uma API compatível com Chat Completions e retorno textual. Duas chamadas reais à NVIDIA foram apresentadas durante os testes. PR [#1](https://github.com/GabrielFabricioPonciano/organizador-de-chamados/pull/1) integrado; tag `p0-basico` publicada.
- **Intermediário:** separação entre entrada (`main.py`), preparação (`text_tools.py`) e consulta (`llm_client.py`), erros controlados e testes offline. 14 testes passaram no computador de desenvolvimento; houve chamada real à NVIDIA. PR [#2](https://github.com/GabrielFabricioPonciano/organizador-de-chamados/pull/2) integrado; tag `p0-intermediario` publicada. Comentários redundantes foram retirados pelo PR [#3](https://github.com/GabrielFabricioPonciano/organizador-de-chamados/pull/3).
- **Avançado:** parâmetros externos, logs técnicos e testes implementados. Foram aprovados 20 testes no ambiente original e 20 em um ambiente virtual novo. A chamada real à NVIDIA foi concluída com código de saída 0. Tag final pendente.

## Decisões

| Decisão | Alternativa | Justificativa |
|---|---|---|
| Interface de terminal | Aplicação web | Atende ao problema sem criar infraestrutura adicional. |
| `requests` para a API | Framework de agentes | O fluxo exige uma consulta textual simples. |
| NVIDIA como alternativa ao institucional | Aguardar a liberação institucional | Permite executar o P0; a aceitação acadêmica do fallback entre provedores precisa ser confirmada. |
| Testes simulados com `unittest` | Testes sempre online | Permite verificar falhas sem custo ou dependência de rede. |
| Logs de eventos e categorias | Armazenar mensagens completas | Evita registrar conteúdo potencialmente sensível. |

## Testes e resultados

| Teste | Entrada ou situação | Esperado | Obtido |
|---|---|---|---|
| Integração real — Básico | Mensagem fictícia de suporte | Ficha organizada | Resposta recebida da NVIDIA; verificado no terminal. |
| Integração real — Intermediário | Mensagem fictícia sobre impressora | Ficha organizada | Resposta recebida da NVIDIA; informações de contexto incompletas. |
| Testes offline — Intermediário | 14 cenários simulados | Todos passarem | 14/14 aprovados no computador de desenvolvimento. |
| Testes offline — Avançado | 20 cenários simulados | Todos aprovados | 20/20 no ambiente original e 20/20 no novo ambiente virtual. |
| Integração real — Avançado | Relato fictício de impressora | Ficha e logs técnicos | NVIDIA respondeu; reinicialização reconhecida; código de saída 0. |
| Ambiente limpo | Novo ambiente virtual com dependências instaladas | Testes funcionando | Python 3.13.0, requests 2.34.2, python-dotenv 1.2.4; 20/20 testes aprovados. |

## Validação local do Avançado

Data: 05/11/2026.

- Ambiente original: 20 testes offline aprovados.
- Novo ambiente virtual: instalação concluída e 20 testes aprovados.
- Python: 3.13.0.
- requests: 2.34.2.
- python-dotenv: 1.2.4.
- Consulta real: NVIDIA respondeu com uma ficha de impressora.
- Contexto da reinicialização reconhecido na resposta.
- Logs observados: início, falha institucional de configuração, sucesso NVIDIA e encerramento.
- Código de saída: 0.
- Os logs apresentados não exibiram credenciais nem o relato completo.
- Nenhum problema encontrado na instalação do ambiente virtual novo.
- Clone independente do GitHub: realizado a partir da branch develop, com novo ambiente virtual Python 3.13, instalação das dependências pelo requirements.txt e 20 testes offline aprovados. Nenhuma credencial foi copiada para o clone.

A ausência de configuração institucional acionou o fallback para NVIDIA.

## Dificuldade encontrada

Ao preparar o Intermediário, uma alteração do `README.md` já estava no *staging* e impediu a execução do script de integração. A diferença foi identificada com `git diff --cached`, revisada e registrada em um commit separado. Também foram encontrados comentários internos redundantes, removidos posteriormente sem modificar a lógica; os 14 testes continuaram passando.

**Limitação:** as respostas de um LLM podem omitir contexto e não são validadas contra um esquema rígido. O serviço institucional ainda não foi testado neste projeto.

## Uso de IA no desenvolvimento

| Ferramenta | Trabalho apoiado | Aproveitamento e revisão | Verificação |
|---|---|---|---|
| ChatGPT | Preparação do código, dos comandos de versionamento, dos testes e da documentação | Execução dos comandos pelo aluno, revisão dos diffs e retirada de comentários redundantes | Testes offline, chamadas reais à NVIDIA e pull requests integrados |

## Reflexão final

- **Principal aprendizado:** PENDENTE — escrever a partir da experiência com o projeto.
- **Competência mais desenvolvida:** PENDENTE — escolher entre C01 e C04 e justificar.
- **O que precisa melhorar:** PENDENTE — identificar uma melhoria concreta.

## Entrega

- **Repositório:** https://github.com/GabrielFabricioPonciano/organizador-de-chamados
- **PRs integrados:** #1, #2 e #3.
- **Tags publicadas:** `p0-basico`, `p0-intermediario`.
- **Tag final:** `p0-avancado` — PENDENTE.
- **Vídeo:** PENDENTE.
- **Ambiente limpo:** ambiente virtual novo criado no computador de desenvolvimento; instalação e 20 testes concluídos.
