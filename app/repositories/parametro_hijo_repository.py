from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.parametro_hijo import ParametroHijo


class ParametroHijoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, *, parametro_id: int, nombre: str, descripcion: str, estado: bool) -> ParametroHijo:
        hijo = ParametroHijo(parametro_id= parametro_id , nombre= nombre, descripcion = descripcion, estado= estado)
        self.db.add(hijo)
        self.db.commit()
        self.db.refresh(hijo)
        return hijo


    def obtener_id(self, id_parametro_hijo: int) -> ParametroHijo | None:
        return self.db.get(ParametroHijo, id_parametro_hijo)

    def list(self, *, skip: int = 0, limit: int = 1000) -> List[ParametroHijo]:
        return (
            self.db.query(ParametroHijo)  # type: ignore[attr-defined]
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(self, id_parametro_hijo: int, *, parametro_id: int, nombre: str | None, descripcion: str | None, estado: bool | None) -> ParametroHijo | None:
        hijo = self.obtener_id(id_parametro_hijo)
        if hijo is None:
            return None
        if parametro_id is not None:
            hijo.parametro_id = parametro_id
        if nombre is not None:
            hijo.nombre = nombre
        if descripcion is not None:
            hijo.descripcion = descripcion
        if estado is not None:
            hijo.estado = estado
        self.db.commit()
        self.db.refresh(hijo)
        return hijo
  

    def delete(self, id_parametro_hijo: int) -> bool:
        hijo = self.obtener_id(id_parametro_hijo)
        if hijo is None:
            return False
        self.db.delete(hijo)
        self.db.commit()
        return True

    def papa(self, parametro_id: int) -> List[ParametroHijo]:
        return (
        self.db.query(ParametroHijo)
        .filter(ParametroHijo.parametro_id == parametro_id)
        .all()
        )

    def cambiar_estado(self, id_parametro_hijo: int) -> bool:
        hijo = self.obtener_id(id_parametro_hijo)
        if hijo is None:
            return False
        hijo.estado = not hijo.estado
        self.db.commit()
        self.db.refresh(hijo)
        return True

    # Búsquedas auxiliares
    def find_by_nombre_exact(self, nombre: str) -> ParametroHijo | None:
        """
        Busca un ParametroHijo por nombre con comparación exacta case-insensitive.
        """
        if not isinstance(nombre, str) or not nombre:
            return None
        return (
            self.db.query(ParametroHijo)  # type: ignore[attr-defined]
            .filter(func.lower(ParametroHijo.nombre) == func.lower(nombre))
            .first()
        )
