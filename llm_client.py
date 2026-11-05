import logging
import os
from dataclasses import dataclass
from urllib.parse import urlparse

import requests

from text_tools import preparar_mensagens, tratar_resposta

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Provedor:
    nome: str
    base_url: str
    modelo: str
    chave: str
    requer_chave: bool


@dataclass(frozen=True)
class Parametros:
    timeout: int
    max_tokens: int
    temperature: float


class FalhaLLM(Exception):
    def __init__(self, categoria, mensagem):
        super().__init__(mensagem)
        self.categoria = categoria


def carregar_parametros():
    try:
        timeout = int(os.getenv("LLM_TIMEOUT", "30"))
        max_tokens = int(os.getenv("LLM_MAX_TOKENS", "1024"))
        temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    except ValueError as exc:
        raise FalhaLLM("configuracao", "Parametros do .env devem ser numeros validos.") from exc
    if not (5 <= timeout <= 180 and 32 <= max_tokens <= 8192 and 0 <= temperature <= 1):
        raise FalhaLLM("configuracao", "Revise LLM_TIMEOUT (5-180), LLM_MAX_TOKENS (32-8192) e LLM_TEMPERATURE (0-1).")
    return Parametros(timeout, max_tokens, temperature)


def configurar_provedores():
    return [
        Provedor(
            "Institucional",
            os.getenv("INSTITUTIONAL_BASE_URL", "").strip(),
            os.getenv("INSTITUTIONAL_MODEL", "").strip(),
            os.getenv("INSTITUTIONAL_API_KEY", "").strip(),
            False,
        ),
        Provedor(
            "NVIDIA",
            os.getenv("NVIDIA_BASE_URL", "").strip(),
            os.getenv("NVIDIA_MODEL", "").strip(),
            os.getenv("NVIDIA_API_KEY", "").strip(),
            True,
        ),
    ]


def _endpoint(provedor):
    url = provedor.base_url.rstrip("/")
    parsed = urlparse(url)
    local = parsed.hostname in {"localhost", "127.0.0.1"}
    if parsed.scheme != "https" and not (local and parsed.scheme == "http"):
        raise FalhaLLM("configuracao", "Endereco de API deve usar HTTPS (exceto localhost).")
    if not parsed.netloc or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise FalhaLLM("configuracao", "Endereco de API invalido.")
    return f"{url}/chat/completions"


def chamar_modelo(provedor, mensagens, parametros=None):
    parametros = carregar_parametros() if parametros is None else parametros
    if not provedor.base_url or not provedor.modelo:
        raise FalhaLLM("configuracao", "Base URL ou modelo nao informado.")
    if provedor.requer_chave and not provedor.chave:
        raise FalhaLLM("credencial_ausente", "Credencial nao informada.")

    url = _endpoint(provedor)
    headers = {"Content-Type": "application/json"}
    if provedor.chave:
        headers["Authorization"] = f"Bearer {provedor.chave}"
    corpo = {
        "model": provedor.modelo,
        "messages": mensagens,
        "max_tokens": parametros.max_tokens,
        "temperature": parametros.temperature,
        "stream": False,
    }
    if provedor.nome == "NVIDIA" and provedor.modelo == "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning":
        corpo["chat_template_kwargs"] = {"enable_thinking": False}
        corpo["top_k"] = 1
    try:
        resposta = requests.post(url, headers=headers, json=corpo, timeout=parametros.timeout, allow_redirects=False)
    except requests.Timeout as exc:
        raise FalhaLLM("timeout", "Tempo de resposta excedido.") from exc
    except requests.RequestException as exc:
        raise FalhaLLM("rede", "Falha de comunicacao com o servico.") from exc

    if 300 <= resposta.status_code < 400:
        raise FalhaLLM("configuracao", "Redirecionamento inesperado da API.")
    if resposta.status_code in (401, 403):
        raise FalhaLLM("credencial_invalida", "Acesso recusado pelo servico.")
    if resposta.status_code == 429:
        raise FalhaLLM("limite", "Limite de requisicoes atingido.")
    if resposta.status_code >= 500:
        raise FalhaLLM("indisponivel", "Servico temporariamente indisponivel.")
    if resposta.status_code >= 400:
        raise FalhaLLM("configuracao", f"Solicitacao nao aceita pelo servico (HTTP {resposta.status_code}).")
    try:
        return tratar_resposta(resposta.json())
    except (ValueError, TypeError) as exc:
        raise FalhaLLM("resposta", "Resposta vazia ou em formato inesperado.") from exc


def gerar_ficha(texto, provedores=None, parametros=None):
    mensagens = preparar_mensagens(texto)
    parametros = carregar_parametros() if parametros is None else parametros
    provedores = configurar_provedores() if provedores is None else provedores
    erros = []
    descricoes = {
        "configuracao": "configuracao ausente ou invalida",
        "credencial_ausente": "credencial ausente",
        "credencial_invalida": "acesso recusado",
        "indisponivel": "servico indisponivel",
        "rede": "falha de comunicacao",
        "timeout": "tempo limite excedido",
        "resposta": "resposta invalida",
        "limite": "limite de requisicoes",
    }
    for provedor in provedores:
        try:
            ficha = chamar_modelo(provedor, mensagens, parametros)
            log.info("llm_event=success provider=%s", provedor.nome)
            return ficha, provedor.nome
        except FalhaLLM as exc:
            log.warning("llm_event=failure provider=%s category=%s", provedor.nome, exc.categoria)
            erros.append(f"{provedor.nome}: {descricoes.get(exc.categoria, 'falha desconhecida')}")
    detalhes = "; ".join(erros) if erros else "nenhum provedor configurado"
    raise FalhaLLM("todos_falharam", f"Nao foi possivel consultar o LLM. {detalhes}. Confira o arquivo .env e a conexao.")
