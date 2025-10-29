from typing import List
from sqlalchemy.orm import Session

from app.models.tipo_incapacidad import TipoIncapacidad


class TipoIncapacidadRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    # Create
    def create(self, *, nombre: str, descripcion: str | None, estado: bool) -> TipoIncapacidad:
        entity = TipoIncapacidad(nombre=nombre, descripcion=descripcion, estado=estado)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    # Read
    def get(self, id_tipo_incapacidad: int) -> TipoIncapacidad | None:
        return self.db.get(TipoIncapacidad, id_tipo_incapacidad)

    def obtener_id(self, id_tipo_incapacidad: int) -> TipoIncapacidad | None:
        return self.get(id_tipo_incapacidad)

    def list(self, *, skip: int = 0, limit: int = 100) -> List[TipoIncapacidad]:
        return (
            self.db.query(TipoIncapacidad)  # type: ignore[attr-defined]
            .offset(skip)
            .limit(limit)
            .all()
        )

    

    # Update
    def update(self, id_tipo_incapacidad: int, *, nombre: str | None, descripcion: str | None, estado: bool | None) -> TipoIncapacidad | None:
        entity = self.get(id_tipo_incapacidad)
        if entity is None:
            return None
        if nombre is not None:
            entity.nombre = nombre
        if descripcion is not None:
            entity.descripcion = descripcion
        if estado is not None:
            entity.estado = estado
        self.db.commit()
        self.db.refresh(entity)
        return entity

    # Delete
    def delete(self, id_tipo_incapacidad: int) -> bool:
        entity = self.get(id_tipo_incapacidad)
        if entity is None:
            return False
        self.db.delete(entity)
        self.db.commit()
        return True


