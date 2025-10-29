from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import secrets
import hashlib

from app.models.base import Base


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    token_hash = Column(String(255), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relación con usuario
    user = relationship("Usuario", back_populates="password_reset_tokens")

    @staticmethod
    def generate_token() -> str:
        """Genera un token seguro para reset de contraseña"""
        return secrets.token_urlsafe(32)

    @staticmethod
    def hash_token(token: str) -> str:
        """Hashea el token para almacenamiento seguro"""
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def create_token(user_id: int, expires_in_hours: int = 24) -> tuple[str, "PasswordResetToken"]:
        """Crea un nuevo token de reset de contraseña"""
        token = PasswordResetToken.generate_token()
        token_hash = PasswordResetToken.hash_token(token)
        expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
        
        reset_token = PasswordResetToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at
        )
        
        return token, reset_token

    def is_valid(self) -> bool:
        """Verifica si el token es válido (no usado y no expirado)"""
        return not self.used and self.expires_at > datetime.utcnow()

    def mark_as_used(self):
        """Marca el token como usado"""
        self.used = True
