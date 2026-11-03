"""P0 Basico: entrada textual -> LLM -> resultado; NVIDIA como reserva."""
import os

import requests
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = (
    "Voce organiza relatos de suporte tecnico em portugues brasileiro. "
    "Retorne somente os campos: Categoria, Problema, Contexto e Informacoes faltantes. "
    "Use apenas fatos presentes na mensagem. Se nao souber, escreva 'Nao informado'. "
    "Nao invente diagnosticos nem instrucoes de conserto."
)


def consultar(base_url, modelo, chave, mensagem):
    headers = {"Content-Type": "application/json"}
    if chave:
        headers["Authorization"] = f"Bearer {chave}"
    payload = {
        "model": modelo,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": mensagem},
        ],
        "max_tokens": 1024,
        "stream": False,
    }
    # Nano Omni usa raciocinio por padrao; para fichas curtas, usar modo instrucao.
    if modelo == "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning":
        payload["chat_template_kwargs"] = {"enable_thinking": False}
        payload["top_k"] = 1
    resposta = requests.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers=headers,
        json=payload,
        timeout=30,
        allow_redirects=False,
    )
    if resposta.status_code >= 300:
        # Nao imprimir cabecalhos, payload ou corpo de erro do provedor.
        raise ValueError(f"HTTP {resposta.status_code}")
    dados = resposta.json()
    texto = dados["choices"][0]["message"]["content"]
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("Resposta vazia ou inesperada")
    return texto.strip()


def main():
    mensagem = input("Cole a mensagem de suporte: ").strip()
    if not mensagem:
        print("Digite uma mensagem antes de continuar.")
        return

    provedores = [
        (
            "Institucional",
            os.getenv("INSTITUTIONAL_BASE_URL", "").strip(),
            os.getenv("INSTITUTIONAL_MODEL", "").strip(),
            os.getenv("INSTITUTIONAL_API_KEY", "").strip(),
        ),
        (
            "NVIDIA",
            os.getenv("NVIDIA_BASE_URL", "").strip(),
            os.getenv("NVIDIA_MODEL", "").strip(),
            os.getenv("NVIDIA_API_KEY", "").strip(),
        ),
    ]
    for nome, url, modelo, chave in provedores:
        if not url or not modelo or (nome == "NVIDIA" and not chave):
            continue
        try:
            resultado = consultar(url, modelo, chave, mensagem)
            print(f"\nProvedor utilizado: {nome}\n\n{resultado}")
            return
        except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
            # Nao imprimir erros internos que podem conter dados sensiveis.
            print(f"Nao foi possivel obter resposta do {nome}. Tentando alternativa...")
    print("Nenhum LLM respondeu. Confira .env, credenciais e conectividade.")


if __name__ == "__main__":
    main()
