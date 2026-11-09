import logging
import os
import unittest
from unittest.mock import patch, Mock

from llm_client import FalhaLLM, Parametros, Provedor, carregar_parametros, gerar_ficha


class TesteConfiguracao(unittest.TestCase):
    @patch.dict(os.environ, {"LLM_TIMEOUT": "12", "LLM_MAX_TOKENS": "256", "LLM_TEMPERATURE": "0.4"})
    def test_parametros_externos(self):
        self.assertEqual(carregar_parametros(), Parametros(12, 256, 0.4))

    @patch.dict(os.environ, {"LLM_TIMEOUT": "abc"})
    def test_parametro_invalido(self):
        with self.assertRaises(FalhaLLM) as erro:
            carregar_parametros()
        self.assertEqual(erro.exception.categoria, "configuracao")

    @patch.dict(os.environ, {"LLM_MAX_TOKENS": "0"})
    def test_faixa_invalida(self):
        with self.assertRaises(FalhaLLM):
            carregar_parametros()


class TesteSeguranca(unittest.TestCase):
    @patch("llm_client.requests.post")
    def test_log_nao_expoe_entrada_credencial_ou_resposta(self, post):
        provedor = Provedor("NVIDIA", "https://integrate.api.nvidia.com/v1", "modelo", "chave_SUPER_SECRETA", True)
        post.return_value.status_code = 200
        post.return_value.json.return_value = {"choices": [{"message": {"content": "RESPOSTA_PRIVADA_789"}}]}
        with self.assertLogs("llm_client", level="INFO") as captured:
            resposta, nome = gerar_ficha("MENSAGEM_PRIVADA_123", [provedor], Parametros(10, 256, 0.2))
        self.assertEqual(nome, "NVIDIA")
        self.assertEqual(resposta, "RESPOSTA_PRIVADA_789")
        registro = " ".join(captured.output)
        self.assertNotIn("MENSAGEM_PRIVADA_123", registro)
        self.assertNotIn("RESPOSTA_PRIVADA_789", registro)
        self.assertNotIn("chave_SUPER_SECRETA", registro)

    @patch("llm_client.requests.post")
    def test_fallback_quando_resposta_vazia(self, post):
        inst = Provedor("Institucional", "https://exemplo.edu.br/v1", "modelo", "", False)
        nvidia = Provedor("NVIDIA", "https://integrate.api.nvidia.com/v1", "modelo", "chave", True)
        vazio = Mock(status_code=200)
        vazio.json.return_value = {"choices": [{"message": {"content": " "}}]}
        valido = Mock(status_code=200)
        valido.json.return_value = {"choices": [{"message": {"content": "Ficha correta"}}]}
        post.side_effect = [vazio, valido]
        with self.assertLogs("llm_client", level="WARNING"):
            ficha, nome = gerar_ficha("Entrada ficticia", [inst, nvidia], Parametros(10, 256, 0.2))
        self.assertEqual((ficha, nome), ("Ficha correta", "NVIDIA"))
        self.assertEqual(post.call_count, 2)

    @patch("llm_client.requests.post")
    def test_http_nao_divulga_corpo_de_erro(self, post):
        provedor = Provedor("NVIDIA", "https://integrate.api.nvidia.com/v1", "modelo", "token_privado", True)
        post.return_value.status_code = 403
        post.return_value.text = "token_privado - nao mostrar"
        with self.assertLogs("llm_client", level="WARNING") as captured:
            with self.assertRaises(FalhaLLM) as erro:
                gerar_ficha("Mensagem pessoal ficticia", [provedor], Parametros(10, 256, 0.2))
        self.assertNotIn("token_privado", str(erro.exception) + str(captured.output))
        self.assertNotIn("Mensagem pessoal ficticia", str(erro.exception) + str(captured.output))


if __name__ == "__main__":
    unittest.main()
