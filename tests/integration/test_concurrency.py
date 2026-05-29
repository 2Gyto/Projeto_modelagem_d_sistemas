"""Testes de concorrência — requisições paralelas e fakes thread-safe."""

from __future__ import annotations

import concurrent.futures

import pytest
from fastapi.testclient import TestClient

from tests.integration.fakes.hardware import (  # noqa: PLC0415
    FakeSerial,
    FakeVisaInstrument,
)


pytestmark = pytest.mark.integration


class TestHttpConcurrency:
    def test_registros_paralelos_nao_corrompem_banco(
        self, integration_client: TestClient
    ) -> None:
        """Múltiplos POSTs simultâneos devem persistir usuários distintos."""

        def _register(i: int) -> int:
            r = integration_client.post(
                "/api/v1/auth/register",
                json={
                    "nome": f"User {i}",
                    "email": f"parallel{i}@example.com",
                    "senha": "senha12345",
                },
            )
            return r.status_code

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            codes = list(pool.map(_register, range(8)))

        assert all(c == 201 for c in codes)

    def test_simulacoes_paralelas_do_mesmo_usuario(
        self,
        integration_client: TestClient,
        auth_headers: dict[str, str],
        simulacao_payload: dict,
    ) -> None:
        def _create(_: int) -> int:
            r = integration_client.post(
                "/api/v1/simulacoes",
                json=simulacao_payload,
                headers=auth_headers,
            )
            return r.status_code

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
            codes = list(pool.map(_create, range(5)))

        assert all(c == 201 for c in codes)

        lista = integration_client.get(
            "/api/v1/simulacoes", headers=auth_headers
        )
        assert len(lista.json()) >= 5


class TestHardwareFakesThreadSafety:
    def test_fake_serial_concorrente(self) -> None:
        serial = FakeSerial(responses=[b"OK\n", b"OK\n", b"OK\n"])
        serial.open()

        def _write_read() -> None:
            serial.write(b"*IDN?\n")
            serial.readline()

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(lambda _: _write_read(), range(12)))

        serial.close()
        assert len(serial.written) == 12

    def test_fake_visa_scpi_sequencial(self) -> None:
        inst = FakeVisaInstrument()
        assert inst.query("*IDN?") == "FAKE,MODEL,SN,1.0"
        inst.write("*RST")
        assert inst.query(":MEAS?") == "1.0"
        assert "*RST" in inst.queries
        inst.close()
