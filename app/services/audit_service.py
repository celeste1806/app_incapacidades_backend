from __future__ import annotations

import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
from enum import Enum


class AuditAction(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    REVIEW = "REVIEW"
    STATUS_CHANGE = "STATUS_CHANGE"


class AuditService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.logger = logging.getLogger(__name__)

    def log_incapacity_action(self, 
                            action: AuditAction,
                            incapacidad_id: int,
                            user_id: int,
                            details: Optional[Dict[str, Any]] = None) -> bool:
        """
        Registra una acción de auditoría en una incapacidad.
        """
        try:
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "action": action.value,
                "entity_type": "incapacidad",
                "entity_id": incapacidad_id,
                "user_id": user_id,
                "details": details or {}
            }
            
            # Por ahora, solo loggeamos la auditoría
            # En un entorno real, guardarías en una tabla de auditoría
            self.logger.info(f"AUDIT: {audit_entry}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error al registrar auditoría: {str(e)}")
            return False

    def log_file_upload(self, 
                       file_id: int,
                       user_id: int,
                       filename: str,
                       file_size: int) -> bool:
        """
        Registra la subida de un archivo.
        """
        try:
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "action": AuditAction.CREATE.value,
                "entity_type": "archivo",
                "entity_id": file_id,
                "user_id": user_id,
                "details": {
                    "filename": filename,
                    "file_size": file_size,
                    "file_type": "PDF"
                }
            }
            
            self.logger.info(f"AUDIT FILE UPLOAD: {audit_entry}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al registrar auditoría de archivo: {str(e)}")
            return False

    def log_administrative_change(self,
                                incapacidad_id: int,
                                admin_id: int,
                                changes: Dict[str, Any]) -> bool:
        """
        Registra cambios administrativos en una incapacidad.
        """
        try:
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "action": AuditAction.UPDATE.value,
                "entity_type": "incapacidad_administrativa",
                "entity_id": incapacidad_id,
                "user_id": admin_id,
                "details": {
                    "changes": changes,
                    "admin_action": True
                }
            }
            
            self.logger.info(f"AUDIT ADMIN CHANGE: {audit_entry}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al registrar auditoría administrativa: {str(e)}")
            return False

    def log_status_change(self,
                         incapacidad_id: int,
                         user_id: int,
                         old_status: int,
                         new_status: int,
                         reason: Optional[str] = None) -> bool:
        """
        Registra cambios de estado en una incapacidad.
        """
        try:
            status_names = {1: "Enviado", 2: "Revisado", 3: "Aprobado", 4: "Rechazado"}
            
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "action": AuditAction.STATUS_CHANGE.value,
                "entity_type": "incapacidad",
                "entity_id": incapacidad_id,
                "user_id": user_id,
                "details": {
                    "old_status": old_status,
                    "new_status": new_status,
                    "old_status_name": status_names.get(old_status, f"Estado {old_status}"),
                    "new_status_name": status_names.get(new_status, f"Estado {new_status}"),
                    "reason": reason
                }
            }
            
            self.logger.info(f"AUDIT STATUS CHANGE: {audit_entry}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al registrar auditoría de estado: {str(e)}")
            return False

    def get_audit_history(self, 
                         entity_type: str,
                         entity_id: int,
                         skip: int = 0,
                         limit: int = 100) -> List[Dict[str, Any]]:
        """
        Obtiene historial de auditoría para una entidad específica.
        """
        try:
            # Por ahora, retornamos una lista vacía
            # En un entorno real, consultarías la tabla de auditoría
            return []
            
        except Exception as e:
            self.logger.error(f"Error al obtener historial de auditoría: {str(e)}")
            return []

    def get_user_audit_history(self, 
                              user_id: int,
                              skip: int = 0,
                              limit: int = 100) -> List[Dict[str, Any]]:
        """
        Obtiene historial de auditoría para un usuario específico.
        """
        try:
            # Por ahora, retornamos una lista vacía
            return []
            
        except Exception as e:
            self.logger.error(f"Error al obtener historial de usuario: {str(e)}")
            return []

    def log_notification_sent(self,
                            notification_type: str,
                            recipient_id: int,
                            sender_id: int,
                            entity_id: Optional[int] = None) -> bool:
        """
        Registra el envío de una notificación.
        """
        try:
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "action": "NOTIFICATION_SENT",
                "entity_type": "notificacion",
                "entity_id": entity_id,
                "user_id": sender_id,
                "details": {
                    "notification_type": notification_type,
                    "recipient_id": recipient_id,
                    "sender_id": sender_id
                }
            }
            
            self.logger.info(f"AUDIT NOTIFICATION: {audit_entry}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al registrar auditoría de notificación: {str(e)}")
            return False
