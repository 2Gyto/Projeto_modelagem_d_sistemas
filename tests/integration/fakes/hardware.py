"""Fakes de hardware para testes sem instrumentos físicos (pyvisa / pyserial).

O domínio SolarCalc ainda não integra bancada; estes fakes permitem validar
padrões de comunicação serial e SCPI quando o módulo for implementado.
"""

from __future__ import annotations

import threading
from collections import deque
from typing import Any


class FakeSerial:
    """Substituto de serial.Serial com buffer thread-safe."""

    def __init__(
        self,
        port: str = "COM1",
        baudrate: int = 9600,
        timeout: float = 1.0,
        *,
        responses: list[bytes] | None = None,
    ) -> None:
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._open = False
        self._lock = threading.Lock()
        self._rx: deque[bytes] = deque(responses or [])
        self.written: list[bytes] = []

    def open(self) -> None:
        self._open = True

    def close(self) -> None:
        self._open = False

    def __enter__(self) -> FakeSerial:
        self.open()
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def write(self, data: bytes) -> int:
        with self._lock:
            if not self._open:
                raise OSError("Port not open")
            self.written.append(data)
            return len(data)

    def readline(self) -> bytes:
        with self._lock:
            if not self._open:
                raise OSError("Port not open")
            if not self._rx:
                return b"\n"
            return self._rx.popleft()

    def flush(self) -> None:
        pass


class FakeVisaInstrument:
    """Substituto mínimo de pyvisa.resources.MessageBasedResource."""

    def __init__(self, *, idn: str = "FAKE,MODEL,SN,1.0") -> None:
        self._idn = idn
        self._lock = threading.Lock()
        self.queries: list[str] = []
        self._scpi_map: dict[str, str] = {
            "*IDN?": idn,
            "*RST": "",
            ":MEAS?": "1.0",
        }

    def write(self, command: str) -> None:
        with self._lock:
            self.queries.append(command.strip())

    def query(self, command: str) -> str:
        with self._lock:
            self.queries.append(command.strip())
            return self._scpi_map.get(command.strip(), "0")

    def close(self) -> None:
        pass
