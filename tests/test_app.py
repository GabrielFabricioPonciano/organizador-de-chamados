"""Testes offline: nao chamam a rede."""
import unittest
from unittest.mock import Mock, patch

from llm_client import FalhaLLM, Provedor, chamar_modelo, gerar_ficha
from text_tools import preparar_mensagens, tratar_resposta, validar_entrada


class TesteTexto(unittest.TestCase):
    def test_entrada_vazia(self):
        with self.assertRaises(ValueError):
            validar_entrada("  ")

    def test_preparacao(self):
        mensagens = preparar_mensagens("  Solicitacao incompleta  ")
        self.assertEqual(mensagens[1]["content"], "Solicitacao incompleta")
        self.assertEqual(mensagens[0]["role"], "system")

    def test_resposta_invalida(self):
        with self.assertRaises(ValueError):
            tratar_resposta({"choices": []})

    def test_resposta_truncada(self):
        dados = {"choices": [{"message": {"content": "Ficha incompleta"}, "finish_reason": "length"}]}
        with self.assertRaises(ValueError):
            tratar_resposta(dados)

    def test_resposta_valida(self):
        self.assertEqual(tratar_resposta({"choices": [{"message": {"content": " Ficha "}}]}), "Ficha")


class TesteAPI(unittest.TestCase):
    def setUp(self):
        self.inst = Provedor("Institucional", "https://instituicao.exemplo/v1", "modelo", "token", True)
        self.nvidia = Provedor("NVIDIA", "https://integrate.api.nvidia.com/v1", "modelo", "token", True)
        self.msg = [{"role": "user", "content": "Teste"}]

    def test_credencial_ausente_simulada(self):
        provedor = Provedor("NVIDIA", self.nvidia.base_url, "modelo", "", True)
        with self.assertRaises(FalhaLLM) as erro:
            chamar_modelo(provedor, self.msg)
        self.assertEqual(erro.exception.categoria, "credencial_ausente")

    @patch("llm_client.requests.post")
    def test_sem_configuracao_nao_envia_requisicao(self, post):
        sem_config = Provedor("Institucional", "", "", "", False)
        with self.assertRaises(FalhaLLM) as erro:
            gerar_ficha("Mensagem ficticia", [sem_config])
        post.assert_not_called()
        self.assertIn(".env", str(erro.exception))

    @patch("llm_client.requests.post")
    def test_credencial_invalida_simulada(self, post):
        post.return_value.status_code = 401
        with self.assertRaises(FalhaLLM) as erro:
            chamar_modelo(self.inst, self.msg)
        self.assertEqual(erro.exception.categoria, "credencial_invalida")

    @patch("llm_client.requests.post", side_effect=__import__("requests").Timeout)
    def test_timeout_simulado(self, post):
        with self.assertRaises(FalhaLLM) as erro:
            chamar_modelo(self.inst, self.msg)
        self.assertEqual(erro.exception.categoria, "timeout")

    @patch("llm_client.requests.post")
    def test_redirecionamento_bloqueado(self, post):
        post.return_value.status_code = 302
        with self.assertRaises(FalhaLLM) as erro:
            chamar_modelo(self.inst, self.msg)
        self.assertEqual(erro.exception.categoria, "configuracao")
        self.assertFalse(post.call_args.kwargs["allow_redirects"])

    @patch("llm_client.requests.post")
    def test_modo_instrucao_nvidia_e_payload_institucional(self, post):
        post.return_value.status_code = 200
        post.return_value.json.return_value = {"choices": [{"message": {"content": "Ficha"}}]}
        nano = Provedor("NVIDIA", self.nvidia.base_url, "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning", "token", True)
        chamar_modelo(nano, self.msg)
        self.assertEqual(post.call_args.kwargs["json"]["chat_template_kwargs"], {"enable_thinking": False})
        self.assertEqual(post.call_args.kwargs["json"]["top_k"], 1)
        chamar_modelo(self.inst, self.msg)
        self.assertNotIn("chat_template_kwargs", post.call_args.kwargs["json"])

    @patch("llm_client.requests.post")
    def test_fallback_simulado(self, post):
        ruim = Mock(status_code=503)
        bom = Mock(status_code=200)
        bom.json.return_value = {"choices": [{"message": {"content": "Ficha valida"}}]}
        post.side_effect = [ruim, bom]
        resposta, nome = gerar_ficha("A impressora parou", [self.inst, self.nvidia])
        self.assertEqual((resposta, nome), ("Ficha valida", "NVIDIA"))
        self.assertEqual(post.call_count, 2)

    @patch("llm_client.requests.post")
    def test_sem_fallback_quando_institucional_funciona(self, post):
        post.return_value.status_code = 200
        post.return_value.json.return_value = {"choices": [{"message": {"content": "Institucional OK"}}]}
        _, nome = gerar_ficha("A impressora parou", [self.inst, self.nvidia])
        self.assertEqual(nome, "Institucional")
        self.assertEqual(post.call_count, 1)

    @patch("llm_client.requests.post")
    def test_sem_expor_segredo(self, post):
        post.return_value.status_code = 401
        with self.assertRaises(FalhaLLM) as erro:
            gerar_ficha("Texto ficticio", [self.inst])
        self.assertNotIn("token", str(erro.exception))
        self.assertNotIn("Texto ficticio", str(erro.exception))


if __name__ == "__main__":
    unittest.main()
