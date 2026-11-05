import logging

from dotenv import load_dotenv

from llm_client import FalhaLLM, gerar_ficha
from text_tools import validar_entrada


def capturar_entrada():
    return input("Cole a mensagem de suporte: ")


def apresentar_resultado(ficha, provedor):
    print(f"\nProvedor utilizado: {provedor}\n\n{ficha}")


def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    logging.info("app_event=start")
    try:
        texto = validar_entrada(capturar_entrada())
        ficha, provedor = gerar_ficha(texto)
        apresentar_resultado(ficha, provedor)
    except ValueError as exc:
        print(f"Entrada invalida: {exc}")
    except FalhaLLM as exc:
        print(f"Nao foi possivel concluir: {exc}")
    except (EOFError, KeyboardInterrupt):
        print("\nOperacao cancelada.")
    finally:
        logging.info("app_event=end")


if __name__ == "__main__":
    main()
