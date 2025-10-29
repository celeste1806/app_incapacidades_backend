from typing import List
from sqlalchemy.orm import Session

from app.models.parametro import Parametro


class ParametroRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    # Create
    def create(self, *, nombre: str, descripcion: str | None, estado: bool) -> Parametro:
        entity = Parametro(nombre=nombre, descripcion=descripcion, estado=estado)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    # Read
    def get(self, id_parametro: int) -> Parametro | None:
        return self.db.get(Parametro, id_parametro)

    def list(self, *, skip: int = 0, limit: int = 100) -> List[Parametro]:
        return (
            self.db.query(Parametro)  # type: ignore[attr-defined]
            .offset(skip)
            .limit(limit)
            .all()
        )

    # Update
    def update(self, id_parametro: int, *, nombre: str | None, descripcion: str | None, estado: bool | None) -> Parametro | None:
        entity = self.get(id_parametro)
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
    def delete(self, id_parametro: int) -> bool:
        entity = self.get(id_parametro)
        if entity is None:
            return False
        self.db.delete(entity)
        self.db.commit()
        return True


