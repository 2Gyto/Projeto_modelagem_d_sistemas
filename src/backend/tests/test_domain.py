"""Testes de enums e hierarquia de exceções de domínio."""

import pytest

from app.domain.enums import (
    OrientacaoTelhado,
    StatusSimulacao,
    TipoConexao,
    TipoEntradaConsumo,
)
from app.domain.exceptions import (
    DomainError,
    EmailAlreadyRegisteredError,
    EntityNotFoundError,
    ExternalApiError,
    InvalidCredentialsError,
)


class TestEnums:
    def test_tipo_entrada_consumo_valores(self) -> None:
        # Objetivo: valores persistidos no banco batem com o domínio.
        assert TipoEntradaConsumo.KWH.value == "KWH"
        assert TipoEntradaConsumo.REAIS.value == "REAIS"

    def test_orientacao_telhado_quatro_pontos_cardeais(self) -> None:
        # Objetivo: RF03 — todas as orientações suportadas existem.
        assert len(OrientacaoTelhado) == 4

    def test_status_simulacao_fluxo_inclui_erro(self) -> None:
        # Objetivo: máquina de estados cobre falha (RF pipeline).
        assert StatusSimulacao.ERRO in StatusSimulacao

    def test_tipo_conexao_mono_bi_tri(self) -> None:
        # Objetivo: RF04 — perfis de conexão ANEEL.
        assert {e.value for e in TipoConexao} == {
            "MONOFASICA",
            "BIFASICA",
            "TRIFASICA",
        }


class TestExceptions:
    def test_external_api_error_guarda_nome_da_api(self) -> None:
        # Objetivo: handler HTTP expõe api_name no JSON 503.
        exc = ExternalApiError("NASA POWER", "timeout")
        assert exc.api_name == "NASA POWER"
        assert "timeout" in str(exc)

    def test_hierarquia_de_excecoes_de_dominio(self) -> None:
        # Objetivo: todas as falhas de negócio são DomainError capturáveis.
        assert issubclass(EntityNotFoundError, DomainError)
        assert issubclass(InvalidCredentialsError, DomainError)
        assert issubclass(EmailAlreadyRegisteredError, DomainError)
        assert issubclass(ExternalApiError, DomainError)

    def test_domain_error_e_raising_simples(self) -> None:
        # Smoke: DomainError genérico para RB customizadas.
        with pytest.raises(DomainError):
            raise DomainError("regra violada")
