"""Testes de validação Pydantic nos contratos HTTP."""

from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.infrastructure.http.schemas import (
    LoginRequest,
    SimulacaoCreate,
    UsuarioCreate,
)


class TestUsuarioCreate:
    def test_usuario_create_valido(self) -> None:
        # Objetivo: payload mínimo aceito no cadastro.
        model = UsuarioCreate(
            nome="João",
            email="joao@example.com",
            senha="senha12345",
        )
        assert model.email == "joao@example.com"

    def test_usuario_create_rejeita_senha_curta(self) -> None:
        # Objetivo: política mínima de 8 caracteres na senha.
        with pytest.raises(ValidationError):
            UsuarioCreate(nome="João", email="j@e.com", senha="curta")

    def test_usuario_create_rejeita_nome_curto(self) -> None:
        # Edge case: nome com menos de 2 caracteres.
        with pytest.raises(ValidationError):
            UsuarioCreate(nome="J", email="j@example.com", senha="senha12345")


class TestSimulacaoCreate:
    def test_simulacao_create_valido(self) -> None:
        # Objetivo: contrato de entrada da simulação aceita decimais positivos.
        model = SimulacaoCreate(
            consumo_kwh=Decimal("100"),
            tipo_entrada="KWH",
            area_m2=Decimal("20"),
            orientacao="NORTE",
            tipo_conexao="MONOFASICA",
        )
        assert model.area_m2 == Decimal("20")

    def test_simulacao_create_rejeita_area_zero(self) -> None:
        # Objetivo: área do telhado deve ser > 0 (RF03).
        with pytest.raises(ValidationError):
            SimulacaoCreate(
                consumo_kwh=Decimal("100"),
                tipo_entrada="KWH",
                area_m2=Decimal("0"),
                orientacao="NORTE",
                tipo_conexao="MONOFASICA",
            )

    def test_simulacao_create_rejeita_consumo_negativo(self) -> None:
        # Edge case: valores negativos não são físicos.
        with pytest.raises(ValidationError):
            SimulacaoCreate(
                consumo_kwh=Decimal("-1"),
                tipo_entrada="KWH",
                area_m2=Decimal("10"),
                orientacao="NORTE",
                tipo_conexao="MONOFASICA",
            )

    def test_simulacao_create_cep_curto(self) -> None:
        # Objetivo: CEP com menos de 8 dígitos é rejeitado na borda do schema.
        with pytest.raises(ValidationError):
            SimulacaoCreate(
                consumo_kwh=Decimal("100"),
                tipo_entrada="KWH",
                cep="123",
                area_m2=Decimal("10"),
                orientacao="NORTE",
                tipo_conexao="MONOFASICA",
            )


class TestLoginRequest:
    def test_login_request_valido(self) -> None:
        # Objetivo: login aceita e-mail e senha sem restrição de tamanho na senha.
        req = LoginRequest(email="a@b.com", senha="x")
        assert req.senha == "x"
