"""Testes do gerador get_db — garante fechamento da sessão (sem vazamento)."""

from unittest.mock import MagicMock, patch

from app.infrastructure.db.session import get_db


class TestGetDb:
    def test_get_db_entrega_sessao_e_fecha_no_generator_close(self) -> None:
        # Objetivo: finally de get_db sempre chama Session.close().
        mock_session = MagicMock()
        with patch(
            "app.infrastructure.db.session.SessionLocal",
            return_value=mock_session,
        ):
            generator = get_db()
            session = next(generator)
            assert session is mock_session
            generator.close()

        mock_session.close.assert_called_once()

    def test_get_db_fecha_sessao_apos_yield_normal(self) -> None:
        # Objetivo: fluxo normal do FastAPI (esgotar generator) também fecha a sessão.
        mock_session = MagicMock()
        with patch(
            "app.infrastructure.db.session.SessionLocal",
            return_value=mock_session,
        ):
            generator = get_db()
            next(generator)
            try:
                next(generator)
            except StopIteration:
                pass

        mock_session.close.assert_called_once()
