import os
from typing import Final

from dotenv import load_dotenv


load_dotenv()


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL no está definido en el archivo .env"
        )
    return database_url


# Exponer constante útil para otros módulos
DATABASE_URL: Final[str] = get_database_url()


def get_env(name: str, default: str = "") -> str:
    value = os.getenv(name, default)
    return value.strip() if isinstance(value, str) else default


# Configuración de seguridad/JWT
SECRET_KEY: Final[str] = get_env("SECRET_KEY", "change-this-secret-key")
ALGORITHM: Final[str] = get_env("ALGORITHM", "HS256")
# 1 día = 1440 minutos
ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = int(get_env("ACCESS_TOKEN_EXPIRE_MINUTES", "1440") or 1440)

