from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.models.base import Base


class IncapacidadArchivo(Base):
    __tablename__ = "incapacidad_archivo"

    id_incapacidad_archivo: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    incapacidad_id: Mapped[int] = mapped_column(Integer, ForeignKey("incapacidad.id_incapacidad"))
    archivo_id: Mapped[int] = mapped_column(Integer, ForeignKey("archivo.id_archivo"))
    url_documento: Mapped[str] = mapped_column(String(500), nullable=False)
    fecha_subida: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())