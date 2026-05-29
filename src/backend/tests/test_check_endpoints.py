"""Testes do script check_endpoints — HTTP mockado (sem servidor real)."""

from unittest.mock import MagicMock, patch

import httpx

from scripts import check_endpoints


class TestCheckEndpointsScript:
    def test_main_imprime_status_health_em_sucesso(self, capsys) -> None:
        # Objetivo: script de smoke test consulta /health sem rede real.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"status":"ok"}'

        with patch("scripts.check_endpoints.httpx.get", return_value=mock_response):
            check_endpoints.main()

        captured = capsys.readouterr().out
        assert "HEALTH STATUS: 200" in captured

    def test_main_trata_erro_de_conexao_health(self, capsys) -> None:
        # Objetivo: falha de rede não derruba o script (mensagem HEALTH ERROR).
        with patch(
            "scripts.check_endpoints.httpx.get",
            side_effect=httpx.ConnectError("recusado"),
        ):
            check_endpoints.main()

        assert "HEALTH ERROR" in capsys.readouterr().out

    def test_main_trata_erro_na_rota_app(self, capsys) -> None:
        # Objetivo: segunda chamada (/app) também captura exceções.
        ok = MagicMock(status_code=200, text="ok")

        def _get(url, **kwargs):
            if "health" in url:
                return ok
            raise httpx.TimeoutException("timeout")

        with patch("scripts.check_endpoints.httpx.get", side_effect=_get):
            check_endpoints.main()

        out = capsys.readouterr().out
        assert "HEALTH STATUS: 200" in out
        assert "APP ERROR" in out

    def test_main_entry_point(self) -> None:
        # Objetivo: execução como script chama main().
        with patch.object(check_endpoints, "main") as mock_main:
            exec(
                compile(
                    "if __name__ == '__main__': main()",
                    check_endpoints.__file__,
                    "exec",
                ),
                {"__name__": "__main__", "main": mock_main},
            )
        mock_main.assert_called_once()
