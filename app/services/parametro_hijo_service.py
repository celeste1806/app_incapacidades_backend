from typing import List
from sqlalchemy.orm import Session

from app.repositories.parametro_repository import ParametroRepository
from app.repositories.parametro_hijo_repository import ParametroHijoRepository
from app.schemas.parametro_hijo import ParametroHijoCreate, ParametroHijoOut, ParametroHijoUpdate
from app.models.parametro_hijo import ParametroHijo

class ParametroHijoService:
    def __init__(self, db: Session) -> None:
        self.repo = ParametroRepository(db)
        self.repohijo = ParametroHijoRepository(db)

    def create(self, payload: ParametroHijoCreate) -> ParametroHijoOut | None:
        entity = self.repo.get(payload.parametro_id)
        if entity is None:
            return None

        hijo = self.repohijo.create(
            parametro_id=payload.parametro_id,
            nombre=payload.nombre,
            descripcion=payload.descripcion,
            estado=payload.estado,
        )
        return ParametroHijoOut.model_validate(hijo)

    def get(self, id_parametro_hijo: int) -> ParametroHijoOut | None:
        hijo = self.repohijo.obtener_id(id_parametro_hijo)
        return None if hijo is None else ParametroHijoOut.model_validate(hijo)


    def list(self, skip: int = 0, limit: int = 100) -> List[ParametroHijoOut]:
        items = self.repohijo.list(skip=skip, limit=limit)
        return [ParametroHijoOut.model_validate(x) for x in items]

    def update(self, id_parametro_hijo: int, payload: ParametroHijoUpdate) -> ParametroHijoOut | None:
        if payload.parametro_id is not None:
            entity_param = self.repo.get(payload.parametro_id)
            if entity_param is None:
                return None
        entity = self.repohijo.update(
            id_parametro_hijo,
            parametro_id=payload.parametro_id,
            nombre=payload.nombre,
            descripcion=payload.descripcion,
            estado=payload.estado,
        )
        return None if entity is None else ParametroHijoOut.model_validate(entity)

    def delete(self, id_parametro_hijo: int) -> bool:
        return self.repohijo.delete(id_parametro_hijo)

    def hijospapa(self, id_parametro: int) -> List[ParametroHijoOut]:
        entity = self.repo.get(id_parametro)
        if entity is None:
            return []
        hijos = self.repohijo.papa(id_parametro) or []
        return [ParametroHijoOut.model_validate(x) for x in hijos]

    def cambiar_estado(self, id_parametro_hijo: int) -> bool:
        return self.repohijo.cambiar_estado(id_parametro_hijo)


