from typing import List
from sqlalchemy.orm import Session

from app.repositories.parametro_repository import ParametroRepository
from app.schemas.parametro import ParametroCreate, ParametroOut, ParametroUpdate


class ParametroService:
    def __init__(self, db: Session) -> None:
        self.repo = ParametroRepository(db)

    def create(self, payload: ParametroCreate) -> ParametroOut:
        entity = self.repo.create(
            nombre=payload.nombre,
            descripcion=payload.descripcion,
            estado=payload.estado,
        )
        return ParametroOut.model_validate(entity)

    def get(self, id_parametro: int) -> ParametroOut | None:
        entity = self.repo.get(id_parametro)
        return None if entity is None else ParametroOut.model_validate(entity)

    def list(self, skip: int = 0, limit: int = 100) -> List[ParametroOut]:
        items = self.repo.list(skip=skip, limit=limit)
        return [ParametroOut.model_validate(x) for x in items]

    def update(self, id_parametro: int, payload: ParametroUpdate) -> ParametroOut | None:
        entity = self.repo.update(
            id_parametro,
            nombre=payload.nombre,
            descripcion=payload.descripcion,
            estado=payload.estado,
        )
        return None if entity is None else ParametroOut.model_validate(entity)

    def delete(self, id_parametro: int) -> bool:
        return self.repo.delete(id_parametro)
