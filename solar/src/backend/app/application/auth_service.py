import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.security import create_access_token, hash_password, verify_password
from app.domain.exceptions import (
    EmailAlreadyRegisteredError,
    EntityNotFoundError,
    InvalidCredentialsError,
)
from app.infrastructure.db.models import Usuario


class AuthService:
    def __init__(self, db: Session) -> None:
        self._db = db

    def register(self, nome: str, email: str, senha: str) -> Usuario:
        exists = self._db.scalar(select(Usuario).where(Usuario.email == email))
        if exists:
            raise EmailAlreadyRegisteredError("E-mail já cadastrado.")

        user = Usuario(
            nome=nome,
            email=email.lower().strip(),
            senha_hash=hash_password(senha),
        )
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def login(self, email: str, senha: str) -> tuple[Usuario, str]:
        user = self._db.scalar(
            select(Usuario).where(Usuario.email == email.lower().strip())
        )
        if not user or not verify_password(senha, user.senha_hash):
            raise InvalidCredentialsError("E-mail ou senha inválidos.")

        token = create_access_token(str(user.id))
        return user, token

    def get_user(self, user_id: uuid.UUID) -> Usuario:
        user = self._db.get(Usuario, user_id)
        if not user:
            raise EntityNotFoundError("Usuário não encontrado.")
        return user
