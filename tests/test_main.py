import socket
import subprocess
import unittest
from unittest.mock import MagicMock, patch
import main
import json
import tempfile
from pathlib import Path


class TestRede(unittest.TestCase):
    @patch("main.socket.gethostbyname", return_value="93.184.216.34")
    def test_consultar_dns_sucesso(self, mock_gethostbyname):
        resultado = main.consultar_dns("example.com")

        self.assertTrue(resultado["sucesso"])
        self.assertEqual(resultado["ipv4"], "93.184.216.34")
        self.assertIsNone(resultado["erro"])
        mock_gethostbyname.assert_called_once_with("example.com")

    @patch(
        "main.socket.gethostbyname",
        side_effect=socket.gaierror("domínio não encontrado")
    )
    def test_consultar_dns_falha(self, _mock_gethostbyname):
        resultado = main.consultar_dns("teste.invalid")

        self.assertFalse(resultado["sucesso"])
        self.assertIsNone(resultado["ipv4"])
        self.assertIn("domínio não encontrado", resultado["erro"])

    @patch("main.socket.create_connection")
    def test_testar_tcp_sucesso(self, mock_create_connection):
        mock_create_connection.return_value.__enter__.return_value = MagicMock()

        resultado = main.testar_tcp("192.0.2.10", 22)

        self.assertTrue(resultado["sucesso"])
        self.assertEqual(resultado["porta"], 22)
        mock_create_connection.assert_called_once_with(
            ("192.0.2.10", 22),
            timeout=3
        )

    @patch(
        "main.socket.create_connection",
        side_effect=OSError("conexão recusada")
    )
    def test_testar_tcp_falha(self, _mock_create_connection):
        resultado = main.testar_tcp("192.0.2.10", 22)

        self.assertFalse(resultado["sucesso"])
        self.assertIn("conexão recusada", resultado["erro"])

    @patch("main.subprocess.run")
    def test_testar_ping_sucesso(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)

        resultado = main.testar_ping("example.com")

        self.assertTrue(resultado["sucesso"])
        self.assertEqual(resultado["codigo"], 0)
        self.assertIsNone(resultado["erro"])

    @patch(
        "main.subprocess.run",
        side_effect=subprocess.TimeoutExpired(cmd="ping", timeout=7)
    )
    def test_testar_ping_timeout(self, _mock_run):
        resultado = main.testar_ping("example.com")

        self.assertFalse(resultado["sucesso"])
        self.assertIsNone(resultado["codigo"])
        self.assertIn("limite de tempo", resultado["erro"])


class TestEntrada(unittest.TestCase):
    @patch("builtins.input", side_effect=["", "servidor.local"])
    @patch("builtins.print")
    def test_solicitar_destino_exige_valor(
        self, mock_print, _mock_input
    ):
        destino = main.solicitar_destino()

        self.assertEqual(destino, "servidor.local")
        mock_print.assert_called_once_with(
            "Informe um IP ou hostname para continuar."
        )

    @patch(
        "builtins.input",
        side_effect=["-c", "nome com espaço", "servidor.local"]
    )
    @patch("builtins.print")
    def test_solicitar_destino_rejeita_entrada_invalida(
        self, mock_print, _mock_input
    ):
        destino = main.solicitar_destino()

        self.assertEqual(destino, "servidor.local")
        self.assertEqual(mock_print.call_count, 2)
        
class TestRelatorio(unittest.TestCase):
    def test_salvar_relatorio(self):
        dados = {
            "sistema": {"sistema": "Linux"},
            "mensagem": "Diagnóstico concluído"
        }

        with tempfile.TemporaryDirectory() as temporaria:
            pasta = Path(temporaria) / "reports"

            caminho = main.salvar_relatorio(dados, pasta)

            self.assertTrue(caminho.exists())
            self.assertEqual(caminho.parent, pasta)

            with caminho.open(encoding="utf-8") as arquivo:
                conteudo = json.load(arquivo)

            self.assertEqual(conteudo, dados)

    def test_preservar_relatorio_anterior(self):
        with tempfile.TemporaryDirectory() as temporaria:
            primeiro = main.salvar_relatorio(
                {"execucao": 1}, temporaria
            )
            segundo = main.salvar_relatorio(
                {"execucao": 2}, temporaria
            )

            self.assertNotEqual(primeiro, segundo)

            with primeiro.open(encoding="utf-8") as arquivo:
                self.assertEqual(json.load(arquivo), {"execucao": 1})

            with segundo.open(encoding="utf-8") as arquivo:
                self.assertEqual(json.load(arquivo), {"execucao": 2})

if __name__ == "__main__":
    unittest.main()
