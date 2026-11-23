# Relatório de execução — Organizador de Chamados

## 1. Evolução do projeto

O projeto foi desenvolvido em três etapas:

- **Básico:** aplicação Python de terminal que recebe relatos de suporte e usa um LLM para organizá-los em fichas. A consulta à NVIDIA funcionou. Tag `p0-basico`.
- **Intermediário:** separação das responsabilidades do código, tratamento de erros e testes offline. Foram aprovados 14 testes. Tag `p0-intermediario`.
- **Avançado:** configurações externas, logs e testes adicionais. Foram aprovados 20 testes, inclusive em um ambiente virtual novo e em um clone independente do GitHub. Tag `p0-avancado`.

A evolução foi registrada em commits e pull requests no GitHub.

## 2. Decisões técnicas

| Decisão | Alternativa | Motivo |
|---|---|---|
| Manter a NVIDIA como provedor utilizado nos testes reais | Usar o serviço institucional | A NVIDIA já havia sido utilizada e validada durante o desenvolvimento. Mesmo com o serviço institucional atualmente disponível, preferi manter o provedor testado. |
| Criar testes simulados com `unittest` | Depender apenas de chamadas reais à API | Permitiu verificar falhas sem depender da internet ou consumir chamadas. |
| Registrar eventos e categorias de erro nos logs | Registrar mensagens e respostas completas | Reduziu a exposição de informações que poderiam ser sensíveis. |
| Colocar parâmetros no `.env` | Deixar valores fixos no código | Permitiu ajustar as configurações sem editar os arquivos Python. |

## 3. Testes e resultados

| Teste | Resultado observado |
|---|---|
| Entrada válida | A NVIDIA gerou uma ficha organizada para um relato fictício. |
| Entrada vazia | O envio foi impedido com uma mensagem de orientação. |
| Credencial ausente ou inválida | Tratamento confirmado nos testes simulados. |
| Falha de comunicação | Tratamento confirmado nos testes simulados. |
| Testes do Intermediário | 14/14 aprovados. |
| Testes do Avançado | 20/20 aprovados. |
| Ambiente virtual novo | Dependências instaladas e 20 testes aprovados. |
| Clone independente do GitHub | Instalação realizada e 20 testes aprovados. |

A consulta real do Avançado utilizou um relato fictício sobre uma impressora. O modelo organizou a mensagem e reconheceu que o equipamento já havia sido reiniciado.

Ambiente de validação: Python 3.13.0, `requests` 2.34.2 e `python-dotenv` 1.2.4.

## 4. Dificuldades e limitações

No Intermediário, uma alteração do `README.md` já preparada no Git impediu temporariamente a integração. Identifiquei a diferença com `git diff --cached`, revisei as mudanças e resolvi o problema.

O LLM pode omitir informações ou produzir respostas imprecisas. Por isso, as fichas geradas precisam ser conferidas. O serviço institucional está disponível atualmente, mas sua integração não foi validada neste projeto; os testes reais documentados utilizaram a NVIDIA.

## 5. Uso de IA no desenvolvimento

Utilizei o ChatGPT como apoio na preparação do código, dos testes, dos comandos Git e da documentação. Executei os comandos e conferi os resultados por meio de testes locais, chamadas reais à API e revisão das alterações e dos pull requests.

## 6. Reflexão final

O principal aprendizado foi que integrar um LLM é apenas uma parte do trabalho. Também é necessário organizar o código, tratar falhas e verificar se o projeto funciona em outro ambiente.

A competência mais desenvolvida foi a **C04**, principalmente pela instalação e validação em um clone independente do GitHub.

Como melhoria futura, seria importante avaliar a qualidade das fichas com mais mensagens variadas, sobretudo as incompletas ou ambíguas.

## 7. Entrega

- **Repositório:** https://github.com/GabrielFabricioPonciano/organizador-de-chamados
- **Tags dos níveis:** `p0-basico`, `p0-intermediario` e `p0-avancado`
- **Versão com a documentação final:** `p0-entrega-final`
- **Vídeo de demonstração:** https://youtu.be/teuFhgPCauc
