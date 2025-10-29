from __future__ import annotations

import logging
import os
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext

from app.models.password_reset_token import PasswordResetToken
from app.repositories.usuario_repository import UsuarioRepository
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class PasswordResetService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.usuario_repo = UsuarioRepository(db)
        self.notification_service = NotificationService(db)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def request_password_reset(self, correo_electronico: str) -> bool:
        """
        Solicita un reset de contraseña para el usuario con el correo dado.
        Siempre retorna True por seguridad (no revela si el correo existe).
        """
        try:
            # Buscar usuario por correo
            usuario = self.usuario_repo.get_by_email(correo_electronico)
            
            if not usuario or not usuario.estado:
                # Por seguridad, no revelamos si el correo existe o no
                logger.info(f"Intento de reset de contraseña para correo no encontrado: {correo_electronico}")
                return True
            
            # Invalidar tokens anteriores del usuario
            self._invalidate_user_tokens(usuario.id_usuario)
            
            # Crear nuevo token
            token, reset_token = PasswordResetToken.create_token(
                user_id=usuario.id_usuario,
                expires_in_hours=24  # Token válido por 24 horas
            )
            
            # Guardar token en la base de datos
            self.db.add(reset_token)
            self.db.commit()
            
            # Enviar correo con el token
            success = self._send_password_reset_email(usuario, token)
            
            if success:
                logger.info(f"Correo de reset de contraseña enviado a {correo_electronico}")
            else:
                logger.error(f"Error al enviar correo de reset a {correo_electronico}")
            
            return True  # Siempre retornar True por seguridad
            
        except Exception as e:
            logger.error(f"Error en request_password_reset para {correo_electronico}: {str(e)}")
            return True  # Por seguridad, siempre retornar True

    def reset_password(self, token: str, new_password: str) -> bool:
        """
        Restablece la contraseña usando el token proporcionado.
        """
        try:
            # Hashear el token para buscar en la base de datos
            token_hash = PasswordResetToken.hash_token(token)
            
            # Buscar el token en la base de datos
            reset_token = self.db.query(PasswordResetToken).filter(
                PasswordResetToken.token_hash == token_hash
            ).first()
            
            if not reset_token:
                logger.warning(f"Token de reset no encontrado: {token[:10]}...")
                return False
            
            # Verificar si el token es válido
            if not reset_token.is_valid():
                logger.warning(f"Token de reset inválido o expirado: {token[:10]}...")
                return False
            
            # Obtener el usuario
            usuario = self.usuario_repo.get(reset_token.user_id)
            if not usuario or not usuario.estado:
                logger.error(f"Usuario no encontrado o inactivo para token: {token[:10]}...")
                return False
            
            # Hashear la nueva contraseña
            hashed_password = self.pwd_context.hash(new_password)
            
            # Actualizar la contraseña del usuario
            usuario.password = hashed_password
            self.db.commit()
            
            # Marcar el token como usado
            reset_token.mark_as_used()
            self.db.commit()
            
            # Enviar correo de confirmación
            self._send_password_reset_confirmation_email(usuario)
            
            logger.info(f"Contraseña restablecida exitosamente para usuario {usuario.id_usuario}")
            return True
            
        except Exception as e:
            logger.error(f"Error en reset_password: {str(e)}")
            self.db.rollback()
            return False

    def _invalidate_user_tokens(self, user_id: int):
        """Invalida todos los tokens de reset del usuario"""
        try:
            self.db.query(PasswordResetToken).filter(
                PasswordResetToken.user_id == user_id,
                PasswordResetToken.used == False
            ).update({"used": True})
            self.db.commit()
        except Exception as e:
            logger.error(f"Error invalidando tokens del usuario {user_id}: {str(e)}")
            self.db.rollback()

    def _send_password_reset_email(self, usuario, token: str) -> bool:
        """Envía correo con enlace para reset de contraseña"""
        try:
            # URL del backend para reset de contraseña (página temporal)
            backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
            reset_url = f"{backend_url}/api/auth/reset-password-page?token={token}"
            
            asunto = "🔐 Restablecer Contraseña - Sistema de Incapacidades"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
                    .content {{ background-color: #f8f9fa; padding: 20px; border-radius: 0 0 5px 5px; }}
                    .button {{ display: inline-block; background-color: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                    .warning {{ background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 15px 0; border-radius: 5px; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔐 Restablecer Contraseña</h1>
                    </div>
                    <div class="content">
                        <p>Estimado/a <strong>{usuario.nombre_completo}</strong>,</p>
                        
                        <p>Hemos recibido una solicitud para restablecer la contraseña de su cuenta en el Sistema de Incapacidades.</p>
                        
                        <p>Para crear una nueva contraseña, haga clic en el siguiente enlace:</p>
                        
                        <div style="text-align: center;">
                            <a href="{reset_url}" class="button">Restablecer Contraseña</a>
                        </div>
                        
                        <div class="warning">
                            <h3>⚠️ Información Importante:</h3>
                            <ul>
                                <li>Este enlace es válido por <strong>24 horas</strong></li>
                                <li>Solo puede ser usado <strong>una vez</strong></li>
                                <li>Si no solicitó este cambio, ignore este correo</li>
                            </ul>
                        </div>
                        
                        <p>Si el botón no funciona, copie y pegue este enlace en su navegador:</p>
                        <p style="word-break: break-all; background-color: #e9ecef; padding: 10px; border-radius: 3px;">
                            {reset_url}
                        </p>
                        
                        <p>Si tiene alguna pregunta, contacte al departamento de recursos humanos.</p>
                        
                        <p>Atentamente,<br>
                        <strong>Equipo de Recursos Humanos</strong></p>
                    </div>
                    <div class="footer">
                        <p>Este es un mensaje automático. Por favor no responda a este correo.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_content = f"""
            RESTABLECER CONTRASEÑA
            
            Estimado/a {usuario.nombre_completo},
            
            Hemos recibido una solicitud para restablecer la contraseña de su cuenta en el Sistema de Incapacidades.
            
            Para crear una nueva contraseña, visite el siguiente enlace:
            {reset_url}
            
            INFORMACIÓN IMPORTANTE:
            - Este enlace es válido por 24 horas
            - Solo puede ser usado una vez
            - Si no solicitó este cambio, ignore este correo
            
            Si tiene alguna pregunta, contacte al departamento de recursos humanos.
            
            Atentamente,
            Equipo de Recursos Humanos
            """
            
            return self.notification_service._send_email(
                to_email=usuario.correo_electronico,
                subject=asunto,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Error enviando correo de reset a {usuario.correo_electronico}: {str(e)}")
            return False

    def _send_password_reset_confirmation_email(self, usuario):
        """Envía correo de confirmación cuando se restablece la contraseña"""
        try:
            asunto = "✅ Contraseña Restablecida - Sistema de Incapacidades"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #28a745; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
                    .content {{ background-color: #f8f9fa; padding: 20px; border-radius: 0 0 5px 5px; }}
                    .success {{ background-color: #d4edda; border: 1px solid #c3e6cb; padding: 15px; margin: 15px 0; border-radius: 5px; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>✅ Contraseña Restablecida</h1>
                    </div>
                    <div class="content">
                        <p>Estimado/a <strong>{usuario.nombre_completo}</strong>,</p>
                        
                        <div class="success">
                            <h3>🎉 ¡Contraseña Restablecida Exitosamente!</h3>
                            <p>Su contraseña ha sido restablecida correctamente.</p>
                        </div>
                        
                        <p>Ahora puede iniciar sesión en el sistema con su nueva contraseña.</p>
                        
                        <p>Si no realizó este cambio, contacte inmediatamente al departamento de recursos humanos.</p>
                        
                        <p>Atentamente,<br>
                        <strong>Equipo de Recursos Humanos</strong></p>
                    </div>
                    <div class="footer">
                        <p>Este es un mensaje automático. Por favor no responda a este correo.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_content = f"""
            CONTRASEÑA RESTABLECIDA
            
            Estimado/a {usuario.nombre_completo},
            
            Su contraseña ha sido restablecida correctamente.
            
            Ahora puede iniciar sesión en el sistema con su nueva contraseña.
            
            Si no realizó este cambio, contacte inmediatamente al departamento de recursos humanos.
            
            Atentamente,
            Equipo de Recursos Humanos
            """
            
            return self.notification_service._send_email(
                to_email=usuario.correo_electronico,
                subject=asunto,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Error enviando correo de confirmación a {usuario.correo_electronico}: {str(e)}")
            return False
