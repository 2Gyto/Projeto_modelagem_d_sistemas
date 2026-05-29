from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
_settings = get_settings()


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=_settings.jwt_expire_minutes
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(
        payload,
        _settings.jwt_secret,
        algorithm=_settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token,
            _settings.jwt_secret,
            algorithms=[_settings.jwt_algorithm],
        )
        sub = payload.get("sub")
        return str(sub) if sub else None
    except JWTError:
        return None
