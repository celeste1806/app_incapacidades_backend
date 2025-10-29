from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


# Usar bcrypt_sha256 para evitar la limitación de 72 bytes de bcrypt puro.
# Mantener compatibilidad para hashes existentes con esquema "bcrypt".
password_context = CryptContext(
    schemes=["bcrypt_sha256", "bcrypt"],
    deprecated="auto",
)

# Configuración de tokens
ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = 7


def hash_password(plain_password: str) -> str:
    # bcrypt_sha256 aplica SHA-256 previo a bcrypt, permitiendo contraseñas >72 bytes
    return password_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Nunca propagar mensajes técnicos de passlib/bcrypt; retornar False si falla
    try:
        return password_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def create_access_token(*, subject: str, claims: dict[str, Any] | None = None, expires_delta: Optional[timedelta] = None) -> str:
    to_encode: dict[str, Any] = {"sub": subject, "type": "access"}
    if claims:
        to_encode.update(claims)
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(*, subject: str, expires_delta: Optional[timedelta] = None) -> str:
    to_encode: dict[str, Any] = {"sub": subject, "type": "refresh"}
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise ValueError("Token inválido")


def validate_refresh_token(token: str) -> dict[str, Any]:
    """Valida que el token sea un refresh token válido"""
    payload = decode_token(token)
    if payload.get("type") != "refresh":
        raise ValueError("Token no es un refresh token válido")
    return payload


def create_tokens_from_refresh_token(refresh_token: str) -> str:
    """Crea un nuevo access token a partir de un refresh token válido"""
    payload = validate_refresh_token(refresh_token)
    user_id = payload.get("sub")
    if not user_id:
        raise ValueError("Token inválido")
    
    # Crear nuevo access token
    return create_access_token(subject=user_id)


