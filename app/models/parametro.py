from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Parametro(Base):
    __tablename__ = "parametro"

    id_parametro: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


