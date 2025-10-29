from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


from app.models.base import Base

class Relacion(Base):
    __tablename__ = "relacion"

    # Clave primaria compuesta
    tipo_incapacidad_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Tipo_incapacidad.id_tipo_incapacidad"),
        primary_key=True,
    )
    archivo_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("archivo.id_archivo"),
        primary_key=True,
    )