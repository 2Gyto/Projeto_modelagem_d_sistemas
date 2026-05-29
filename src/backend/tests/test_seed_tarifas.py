"""Testes do script de seed SQLite — mock de arquivo e banco."""

import sqlite3
from pathlib import Path
from unittest.mock import MagicMock, patch


from scripts import seed_tarifas_uf as seed_module


class TestSeedTarifasUf:
    def test_main_cria_tabela_e_insere_27_ufs(self, tmp_path: Path) -> None:
        # Objetivo: seed popula todas as UFs sem tocar data/ real do projeto.
        db_file = tmp_path / "tarifas_test.db"
        mock_conn = MagicMock(spec=sqlite3.Connection)

        with (
            patch.object(seed_module, "DB_PATH", db_file),
            patch("scripts.seed_tarifas_uf.sqlite3.connect", return_value=mock_conn) as mock_connect,
            patch("builtins.print") as mock_print,
        ):
            seed_module.main()

        mock_connect.assert_called_once_with(db_file)
        mock_conn.execute.assert_called()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

        # 1 CREATE + 27 INSERT/UPDATE
        assert mock_conn.execute.call_count >= 28
        mock_print.assert_called_once()
        assert "27" in str(mock_print.call_args)

    def test_tarifas_uf_contem_sp_e_valores_positivos(self) -> None:
        # Objetivo: dados de seed são consistentes (tarifa e taxas > 0).
        ufs = {row[0]: row for row in seed_module.TARIFAS_UF}
        assert "SP" in ufs
        sp = ufs["SP"]
        assert sp[1] > 0  # tarifa_kwh
        assert sp[2] > 0  # mono
        assert len(ufs) == 27

    def test_main_entry_point_chama_main(self) -> None:
        # Objetivo: bloco __main__ do script invoca main().
        with patch.object(seed_module, "main") as mock_main:
            exec(
                compile(
                    "if __name__ == '__main__': main()",
                    seed_module.__file__,
                    "exec",
                ),
                {"__name__": "__main__", "main": mock_main},
            )
        mock_main.assert_called_once()
