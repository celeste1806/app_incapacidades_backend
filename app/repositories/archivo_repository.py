from typing import List
from sqlalchemy.orm import Session

from app.models.archivo import Archivo
from app.models.relacion import Relacion


class ArchivoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    # Create
    def create(self, payload) -> Archivo:
        entity = Archivo(
            nombre=payload.nombre, 
            descripcion=payload.descripcion, 
            estado=payload.estado
        )
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    # Read
    def get(self, id_archivo: int) -> Archivo | None:
        return self.db.get(Archivo, id_archivo)

    def obtener_id(self, id_archivo: int) -> Archivo | None:
        return self.get(id_archivo)

    def list(self, *, skip: int = 0, limit: int = 100) -> List[Archivo]:
        return (
            self.db.query(Archivo)  # type: ignore[attr-defined]
            .offset(skip)
            .limit(limit)
            .all()
        )

    def list_by_tipo_incapacidad(self, tipo_incapacidad_id: int) -> List[Archivo]:
        return (
            self.db.query(Archivo)  # type: ignore[attr-defined]
            .join(Relacion, Relacion.archivo_id == Archivo.id_archivo)
            .filter(Relacion.tipo_incapacidad_id == tipo_incapacidad_id)
            .all()
        )

    # Update
    def update(self, id_archivo: int, *, nombre: str | None, descripcion: str | None, estado: bool | None) -> Archivo | None:
        entity = self.get(id_archivo)
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
    def delete(self, id_archivo: int) -> bool:
        entity = self.get(id_archivo)
        if entity is None:
            return False
        self.db.delete(entity)
        self.db.commit()
        return True


