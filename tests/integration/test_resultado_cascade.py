"""Integração de persistência em cascata (resultado + projeções anuais)."""

from __future__ import annotations

from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.application.auth_service import AuthService
from app.application.simulacao_service import SimulacaoService
from app.domain.enums import StatusSimulacao
from app.infrastructure.db.models import ProjecaoAnual, Resultado, Simulacao
from app.infrastructure.http.schemas import SimulacaoCreate


pytestmark = pytest.mark.integration


class TestResultadoCascadeIntegration:
    def test_resultado_e_projecoes_persistem_com_fk(
        self, db_session: Session
    ) -> None:
        user = AuthService(db_session).register(
            "Calc", "calc@test.com", "senha12345"
        )
        sim = SimulacaoService(db_session).criar_rascunho(
            user,
            SimulacaoCreate(
                consumo_kwh=Decimal("300"),
                valor_reais=None,
                tipo_entrada="KWH",
                cep="01310100",
                cidade="SP",
                area_m2=Decimal("40"),
                orientacao="NORTE",
                tipo_conexao="MONOFASICA",
            ),
        )
        sim.status = StatusSimulacao.CONCLUIDA
        resultado = Resultado(
            simulacao_id=sim.id,
            geracao_kwh=Decimal("4500"),
            economia_mensal=Decimal("320"),
            payback_anos=Decimal("5.5"),
            payback_meses=Decimal("66"),
            custo_total=Decimal("25000"),
        )
        db_session.add(resultado)
        db_session.flush()

        for ano in range(1, 4):
            db_session.add(
                ProjecaoAnual(
                    resultado_id=resultado.id,
                    ano=ano,
                    custo_concessionaria=Decimal("1200"),
                    custo_fotovoltaico=Decimal("800"),
                    saldo=Decimal("400"),
                )
            )
        db_session.commit()

        loaded = db_session.scalar(
            select(Simulacao)
            .where(Simulacao.id == sim.id)
            .options(
                selectinload(Simulacao.resultado).selectinload(
                    Resultado.projecoes
                )
            )
        )
        assert loaded is not None
        assert loaded.resultado is not None
        assert len(loaded.resultado.projecoes) == 3
        assert loaded.resultado.payback_anos == Decimal("5.5")
