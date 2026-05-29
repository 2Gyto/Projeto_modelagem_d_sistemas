import json
import logging
from decimal import Decimal, InvalidOperation

from app.config import get_settings
from app.domain.exceptions import DomainError, ExternalApiError
from app.infrastructure.external.base_client import BaseHttpClient
from app.infrastructure.external.dtos import DadosMercadoGemini

logger = logging.getLogger(__name__)
_settings = get_settings()

_PROMPT_TEMPLATE = """Você é um consultor de energia solar no Brasil.
Para o estado {uf}, retorne APENAS um JSON válido (sem markdown) com:
{{
  "tarifa_kwh": <número decimal — tarifa média atual da concessionária local em R$/kWh>,
  "marcas_recomendadas": [<exatamente 3 strings com marcas confiáveis de painéis solares>],
  "observacao": "<frase curta sobre a tarifa ou mercado local>"
}}
Use valores realistas para o Brasil em 2025/2026."""


class GeminiApiClient(BaseHttpClient):
    def __init__(self) -> None:
        super().__init__("Gemini API", _settings.gemini_api_base_url)

    async def consultar_tarifa_e_marcas(self, estado_uf: str) -> DadosMercadoGemini:
        if not _settings.gemini_api_key:
            raise DomainError(
                "Chave da Gemini API não configurada (GEMINI_API_KEY)."
            )

        prompt = _PROMPT_TEMPLATE.format(uf=estado_uf.upper())
        path = (
            f"/v1beta/models/{_settings.gemini_model}:generateContent"
            f"?key={_settings.gemini_api_key}"
        )
        body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.2,
            },
        }

        response = await self.post(path, json=body)
        return self._parse_response(response.json())

    def _parse_response(self, payload: dict) -> DadosMercadoGemini:
        try:
            texto = payload["candidates"][0]["content"]["parts"][0]["text"]
            dados = json.loads(texto)
        except (KeyError, IndexError, json.JSONDecodeError) as exc:
            logger.warning("Resposta Gemini inválida: %s", payload)
            raise ExternalApiError(
                "Gemini API",
                "Não foi possível interpretar a resposta da IA.",
            ) from exc

        try:
            tarifa = Decimal(str(dados["tarifa_kwh"]))
            marcas = [str(m) for m in dados["marcas_recomendadas"]][:3]
            if len(marcas) < 3:
                raise ValueError("menos de 3 marcas")
            if tarifa <= 0:
                raise ValueError("tarifa inválida")
        except (KeyError, InvalidOperation, TypeError, ValueError) as exc:
            raise ExternalApiError(
                "Gemini API",
                "Estrutura JSON esperada não retornada pelo modelo.",
            ) from exc

        observacao = dados.get("observacao")
        return DadosMercadoGemini(
            tarifa_kwh=tarifa.quantize(Decimal("0.0001")),
            marcas_recomendadas=marcas,
            observacao=str(observacao) if observacao else None,
        )
