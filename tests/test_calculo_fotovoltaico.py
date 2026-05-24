"""Testes do motor de cálculo (sem APIs externas)."""

import sys
import unittest
from decimal import Decimal
from pathlib import Path

_BACKEND = Path(__file__).resolve().parents[1] / "src" / "backend"
sys.path.insert(0, str(_BACKEND))

from app.application.calculo_fotovoltaico import CalculoFotovoltaicoService, EntradaCalculo
from app.config import Settings
from app.domain.enums import OrientacaoTelhado, TipoConexao
from app.infrastructure.db.tarifa_sqlite import TarifaUf


def _tarifa_sp() -> TarifaUf:
    return TarifaUf(
        uf="SP",
        tarifa_kwh=Decimal("0.6123"),
        taxa_disponibilidade_mono=Decimal("30"),
        taxa_disponibilidade_bi=Decimal("50"),
        taxa_disponibilidade_tri=Decimal("100"),
        atualizado_em="2026-05-24",
        fonte="teste",
    )


class TestCalculoFotovoltaico(unittest.TestCase):
    def setUp(self) -> None:
        self.svc = CalculoFotovoltaicoService(Settings())

    def test_geracao_e_payback_positivos(self) -> None:
        entrada = EntradaCalculo(
            consumo_kwh_mes=Decimal("400"),
            area_m2=Decimal("30"),
            orientacao=OrientacaoTelhado.NORTE,
            tipo_conexao=TipoConexao.MONOFASICA,
            hsp_medio_dia=Decimal("4.5"),
            tarifa=_tarifa_sp(),
        )
        r = self.svc.calcular(entrada)
        self.assertGreater(r.qtd_paineis, 0)
        self.assertGreater(r.geracao_kwh_mes, 0)
        self.assertGreater(r.investimento, 0)
        self.assertGreater(r.economia_mensal, 0)
        self.assertEqual(len(r.projecoes), 26)
        self.assertEqual(r.projecoes[0].ano, 0)

    def test_area_insuficiente(self) -> None:
        entrada = EntradaCalculo(
            consumo_kwh_mes=Decimal("100"),
            area_m2=Decimal("1"),
            orientacao=OrientacaoTelhado.SUL,
            tipo_conexao=TipoConexao.TRIFASICA,
            hsp_medio_dia=Decimal("3"),
            tarifa=_tarifa_sp(),
        )
        with self.assertRaises(ValueError):
            self.svc.calcular(entrada)


if __name__ == "__main__":
    unittest.main()
