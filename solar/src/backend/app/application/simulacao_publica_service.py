"""Fluxo público de simulação — captura lead, calcula e persiste."""

import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.calculadora_solar import (
    TARIFA_PADRAO_REAIS_KWH,
    calcular_paineis_por_gasto,
)
from app.domain.enums import StatusSimulacao, TipoEntradaConsumo
from app.domain.exceptions import EntityNotFoundError
from app.infrastructure.db.models import (
    DadosConsumo,
    Localizacao,
    Resultado,
    Simulacao,
    Usuario,
)
from app.infrastructure.http.schemas import (
    SimulacaoPublicaCreate,
    SimulacaoPublicaResponse,
)

import os
import smtplib
from email.mime.text import MIMEText


class SimulacaoPublicaService:
    def __init__(self, db: Session) -> None:
        self._db = db

    def executar(self, dados: SimulacaoPublicaCreate) -> SimulacaoPublicaResponse:
        usuario = self._upsert_lead(dados.nome, dados.email)

        sim = Simulacao(usuario_id=usuario.id, status=StatusSimulacao.CALCULANDO)
        self._db.add(sim)
        self._db.flush()

        self._db.add(
            DadosConsumo(
                simulacao_id=sim.id,
                valor_reais=dados.valor_reais,
                tipo_entrada=TipoEntradaConsumo.REAIS,
            )
        )
        self._db.add(Localizacao(simulacao_id=sim.id, cep=dados.cep))

        calc = calcular_paineis_por_gasto(dados.valor_reais)

        self._db.add(
            Resultado(
                simulacao_id=sim.id,
                geracao_kwh=calc.geracao_total_kwh_mes,
                economia_mensal=calc.economia_mensal_reais,
                quantidade_paineis=calc.quantidade_paineis,
                potencia_sistema_kwp=calc.potencia_sistema_kwp,
            )
        )

        sim.status = StatusSimulacao.CONCLUIDA
        self._db.commit()
        self._db.refresh(sim)

        # ---> INÍCIO DO MOTOR DE E-MAIL <---
        try:
            remetente = os.environ.get("SMTP_USER")
            senha = os.environ.get("SMTP_PASSWORD")
            
            if remetente and senha:
                corpo = (
                    f"Olá, {usuario.nome}!\n\n"
                    f"Os cálculos do seu telhado solar foram concluídos com sucesso.\n"
                    f"Acesse o link abaixo para visualizar seu dashboard e a projeção de economia para os próximos 25 anos:\n\n"
                    f"https://https://85f9ee2a172de1.lhr.life//dashboard?id={sim.id}\n\n"
                    f"Um abraço,\n"
                    f"Equipe Zila Technologies"
                )
                
                msg = MIMEText(corpo, 'plain', 'utf-8')
                msg['Subject'] = 'Resultado da sua simulação - SolarCalc'
                msg['From'] = remetente
                msg['To'] = usuario.email

                # Conecta ao Gmail e dispara
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(remetente, senha)
                    server.send_message(msg)
                    print(f"SUCESSO: E-mail enviado para {usuario.email}")
            else:
                print("AVISO: Credenciais de e-mail não encontradas no .env")
        except Exception as e:
            print(f"ERRO AO ENVIAR E-MAIL: {e}")
        # ---> FIM DO MOTOR DE E-MAIL <---   

        return SimulacaoPublicaResponse(
            simulacao_id=sim.id,
            nome=usuario.nome,
            email=usuario.email,
            cep=dados.cep,
            valor_reais=dados.valor_reais,
            consumo_kwh_mes=calc.consumo_kwh_mes,
            quantidade_paineis=calc.quantidade_paineis,
            potencia_sistema_kwp=calc.potencia_sistema_kwp,
            geracao_total_kwh_mes=calc.geracao_total_kwh_mes,
            economia_mensal_reais=calc.economia_mensal_reais,
        )

    def obter(self, simulacao_id: uuid.UUID) -> SimulacaoPublicaResponse:
        sim = self._db.get(Simulacao, simulacao_id)
        if not sim or not sim.resultado or not sim.dados_consumo or not sim.localizacao:
            raise EntityNotFoundError("Simulação não encontrada.")

        valor = sim.dados_consumo.valor_reais or Decimal("0")
        consumo_kwh = (valor / TARIFA_PADRAO_REAIS_KWH).quantize(Decimal("0.01"))

        return SimulacaoPublicaResponse(
            simulacao_id=sim.id,
            nome=sim.usuario.nome,
            email=sim.usuario.email,
            cep=sim.localizacao.cep or "",
            valor_reais=valor,
            consumo_kwh_mes=consumo_kwh,
            quantidade_paineis=sim.resultado.quantidade_paineis or 0,
            potencia_sistema_kwp=sim.resultado.potencia_sistema_kwp or Decimal("0"),
            geracao_total_kwh_mes=sim.resultado.geracao_kwh or Decimal("0"),
            economia_mensal_reais=sim.resultado.economia_mensal or Decimal("0"),
        )

    def _upsert_lead(self, nome: str, email: str) -> Usuario:
        email_norm = email.lower().strip()
        existing = self._db.scalar(select(Usuario).where(Usuario.email == email_norm))
        if existing:
            if existing.nome != nome:
                existing.nome = nome
                self._db.flush()
            return existing
        novo = Usuario(nome=nome, email=email_norm, senha_hash=None)
        self._db.add(novo)
        self._db.flush()
        return novo
