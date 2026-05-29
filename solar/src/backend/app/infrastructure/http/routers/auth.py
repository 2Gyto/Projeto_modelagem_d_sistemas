from fastapi import APIRouter, Depends, HTTPException, status

from app.application.auth_service import AuthService
from app.domain.exceptions import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
)
from app.infrastructure.db.models import Usuario
from app.infrastructure.http.dependencies import get_auth_service, get_current_user
from app.infrastructure.http.schemas import (
    LoginRequest,
    TokenResponse,
    UsuarioCreate,
    UsuarioResponse,
)

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    body: UsuarioCreate,
    auth: AuthService = Depends(get_auth_service),
) -> Usuario:
    try:
        return auth.register(body.nome, body.email, body.senha)
    except EmailAlreadyRegisteredError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.post("/login", response_model=TokenResponse)
def login(
    body: LoginRequest,
    auth: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    try:
        _, token = auth.login(body.email, body.senha)
        return TokenResponse(access_token=token)
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.get("/me", response_model=UsuarioResponse)
def me(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    return current_user
