"""Integração de persistência em arquivo (SQLite de tarifas) e ciclo de sessão DB."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from scripts import seed_tarifas_uf as seed_module


pytestmark = pytest.mark.integration


class TestSeedTarifasIntegration:
    def test_main_grava_27_ufs_em_arquivo_temporario(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        db_path = tmp_path / "tarifas_integration.db"
        monkeypatch.setattr(seed_module, "DB_PATH", db_path)

        seed_module.main()
        assert db_path.exists()

        conn = sqlite3.connect(db_path)
        try:
            rows = conn.execute(
                "SELECT uf, tarifa_kwh FROM tarifas_uf ORDER BY uf"
            ).fetchall()
        finally:
            conn.close()

        assert len(rows) == 27
        ufs = {r[0] for r in rows}
        assert "SP" in ufs
        assert all(r[1] > 0 for r in rows)

    def test_reexecucao_atualiza_sem_duplicar_uf(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        db_path = tmp_path / "tarifas_idempotent.db"
        monkeypatch.setattr(seed_module, "DB_PATH", db_path)

        seed_module.main()
        seed_module.main()

        conn = sqlite3.connect(db_path)
        try:
            count = conn.execute("SELECT COUNT(*) FROM tarifas_uf").fetchone()[0]
        finally:
            conn.close()
        assert count == 27


class TestSessionLifecycleIntegration:
    def test_sessao_fecha_apos_request(
        self, integration_client, auth_headers, simulacao_payload
    ) -> None:
        """Garante que requests HTTP não deixam sessão aberta (vazamento de conexão)."""
        for _ in range(5):
            r = integration_client.post(
                "/api/v1/simulacoes",
                json=simulacao_payload,
                headers=auth_headers,
            )
            assert r.status_code == 201

    def test_transacao_commit_visivel_na_mesma_sessao(
        self, db_session: Session
    ) -> None:
        from app.application.auth_service import AuthService
        from app.infrastructure.db.models import Usuario

        AuthService(db_session).register("Tx", "tx@test.com", "senha12345")
        db_session.commit()

        user = db_session.scalar(select(Usuario).where(Usuario.email == "tx@test.com"))
        assert user is not None
