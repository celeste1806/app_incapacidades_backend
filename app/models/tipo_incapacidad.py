from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


from app.models.base import Base

class TipoIncapacidad(Base):
    __tablename__ = "Tipo_incapacidad"

    id_tipo_incapacidad:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre:Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion:Mapped[str | None] = mapped_column(String(255), nullable=True)
    estado:Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)