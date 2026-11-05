# Organizador de chamados

Aplicação Python que transforma mensagens de suporte técnico em fichas com categoria, problema, contexto e informações faltantes.

## Problema

Quem recebe solicitações de suporte precisa interpretar relatos informais, frequentemente incompletos. A aplicação organiza o texto para facilitar o registro inicial de um chamado.

- **Público:** equipes pequenas de suporte e atendimento.
- **Entrada:** texto digitado no terminal.
- **Saída:** ficha textual organizada pelo modelo.
- **Por que um LLM:** interpreta variações de linguagem que seriam difíceis de cobrir apenas com regras fixas.

A aplicação não faz diagnóstico ou correção de equipamentos, não armazena chamados e não garante que todas as informações geradas estejam corretas.

## Requisitos

Python 3.10 ou superior. Bibliotecas diretas: `requests` e `python-dotenv`, listadas em `requirements.txt`.

Ambiente usado durante o desenvolvimento: Windows, Python 3.13.0, `requests` 2.34.2 e `python-dotenv` 1.2.4. Essas são as versões observadas nos testes locais anteriores; outras versões dentro das faixas declaradas podem funcionar.

## Instalação no Windows (PowerShell)

Clone este repositório e entre na pasta `organizador-de-chamados`. Depois execute:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

No `.env`, preencha o endereço, o identificador do modelo e a chave de acesso do provedor que utilizar. **Não compartilhe nem publique esse arquivo.** O exemplo já inclui o endpoint e o nome do modelo NVIDIA; faltará sua própria chave de API.

As variáveis `INSTITUTIONAL_*` são opcionais. O serviço institucional só pode ser usado se fornecer uma API compatível com Chat Completions; essa compatibilidade ainda não foi validada. Quando configurado, o programa tenta primeiro o institucional e, se ele falhar, tenta a NVIDIA.

Configurações ajustáveis sem editar o código:

| Variável | Padrão | Intervalo |
|---|---:|---|
| `LLM_TIMEOUT` | 30 | 5–180 segundos |
| `LLM_MAX_TOKENS` | 1024 | 32–8192 |
| `LLM_TEMPERATURE` | 0.2 | 0–1 |

Para executar:

```powershell
.\.venv\Scripts\python.exe main.py
```

**Exemplo fictício de entrada:** "O computador da recepção não consegue acessar a rede. Já reiniciei o equipamento."

**Exemplo de saída esperada:** categoria de rede, problema de conectividade, tentativa de reinicialização e informações a confirmar. A redação da resposta pode variar conforme o modelo.

## Testes

Para executar os testes offline, sem gastar chamadas de API:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Esses testes usam respostas e erros **simulados**. Verificam validação, configuração, autenticação ausente/inválida, timeout, fallback, resposta inesperada, logs e parâmetros externos. Não substituem o teste real de integração.

Para conferir a integração real, configure uma chave válida e execute `main.py` com uma mensagem fictícia. O terminal identifica o provedor que respondeu.

## Privacidade e segurança

Os exemplos utilizados no projeto são fictícios. As credenciais de acesso ao modelo são mantidas em variáveis de ambiente e não são incluídas no repositório.

Os logs aparecem no terminal e indicam apenas início/fim, provedor e categoria de erro. Não armazenam prompts, respostas, chaves ou dados pessoais. O arquivo `.env` e os ambientes virtuais estão excluídos do controle de versão.

Por causa do fallback, uma mesma mensagem pode ser enviada aos dois provedores se o primeiro falhar. Evite dados pessoais e confidenciais. O enunciado do P0 menciona um único LLM; confirme com a coordenação a aceitação do fallback ou use apenas o provedor NVIDIA configurado durante a avaliação.

## Evolução e entrega

- Básico: entrada pelo terminal e chamada à API — tag `p0-basico`.
- Intermediário: organização, erros e testes — tag `p0-intermediario`.
- Avançado: configuração externa, logs e validação de ambiente limpo — tag `p0-avancado` após a conclusão.

As decisões e os resultados observados estão em [`RELATORIO_EXECUCAO.md`](RELATORIO_EXECUCAO.md).

**Vídeo de demonstração:** PENDENTE — inserir link antes da entrega final.
