from sqlalchemy import Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func

from app.models.base import Base

class Administrador(Base):
    __tablename__ = "administrador"

    id_administrador: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    correo_electronico: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str] = mapped_column(String(150), nullable=False)
    numero_radicado: Mapped[str] = mapped_column(String(150), nullable=False)
    fecha_radicado: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    paga: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())