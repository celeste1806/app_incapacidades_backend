from sqlalchemy import Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.models.base import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_completo: Mapped[str] = mapped_column(String(150), nullable=False)
    numero_identificacion:Mapped[str] = mapped_column(String(150), nullable=False)
    tipo_identificacion_id:Mapped[int] = mapped_column(Integer, ForeignKey("parametro_hijo.id_parametrohijo"))
    tipo_empleador_id:Mapped[int] = mapped_column(Integer, ForeignKey("parametro_hijo.id_parametrohijo"))
    cargo_interno_id:Mapped[int] = mapped_column(Integer, ForeignKey("parametro_hijo.id_parametrohijo"))
    correo_electronico:Mapped[str] = mapped_column(String(150), nullable=False)
    telefono:Mapped[str] = mapped_column(String(30), nullable=True)
    password:Mapped[str] = mapped_column(String(150), nullable=False)
    rol_id:Mapped[int] = mapped_column(Integer, ForeignKey("parametro_hijo.id_parametrohijo"))
    estado:Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Relaciones
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user")
    