"""Envio de e-mail via SMTP (Gmail) — credenciais lidas do .env com logs explícitos."""

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
_REPO_ROOT = _BACKEND_DIR.parent.parent
load_dotenv(_REPO_ROOT / ".env", override=True)
load_dotenv(_BACKEND_DIR / ".env", override=True)


async def enviar_email_simulacao(
    email_destino: str,
    simulacao_id: str,
    payback_texto: str = "",
) -> None:
    """Dispara e-mail com o resultado da simulação (background task / diagnóstico no console)."""
    print(f"--- INICIANDO ENVIO DE E-MAIL PARA {email_destino} ---")

    remetente = os.getenv("SMTP_USER")
    senha = os.getenv("SMTP_PASSWORD")

    if not remetente:
        print("❌ ERRO CRÍTICO NO ENVIO DE E-MAIL: SMTP_USER não configurado no .env")
        return
    if not senha:
        print("❌ ERRO CRÍTICO NO ENVIO DE E-MAIL: SMTP_PASSWORD não configurado no .env")
        return

    print(f"Usuário SMTP carregado: {remetente}")
    print(f"Tamanho da senha lida: {len(senha)}")

    corpo = (
        f"Olá!\n\n"
        f"Sua simulação solar foi concluída com sucesso.\n"
        f"ID da simulação: {simulacao_id}\n"
    )
    if payback_texto:
        corpo += f"Payback estimado: {payback_texto}\n"
    corpo += (
        "\nAcesse seu dashboard para ver os detalhes completos.\n\n"
        "Equipe SolarCalc"
    )

    msg = EmailMessage()
    msg["Subject"] = "Resultado da sua Simulação Solar"
    msg["From"] = remetente
    msg["To"] = email_destino
    msg.set_content(corpo)

    try:
        print("Conectando ao servidor do Gmail...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        print("Tentando fazer o login...")
        server.login(remetente, senha)

        print("Enviando mensagem...")
        server.send_message(msg)

        server.quit()
        print("✅ E-MAIL ENVIADO COM SUCESSO PELA API!")

    except Exception as e:
        print(f"❌ ERRO CRÍTICO NO ENVIO DE E-MAIL: {e}")
