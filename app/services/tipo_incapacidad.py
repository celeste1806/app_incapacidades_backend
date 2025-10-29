from typing import List
from sqlalchemy.orm import Session

from app.models.tipo_incapacidad import TipoIncapacidad
from app.repositories.tipo_incapacidad import TipoIncapacidadRepository
from app.schemas.tipo_incapacidad import TipoIncapacidadCreate, TipoIncapacidadOut, TipoIncapacidadUpdate

class TipoIncapacidadService:
    def __init__(self, db: Session) -> None:
        self.repoin = TipoIncapacidadRepository(db)
        
    def create(self, payload: TipoIncapacidadCreate) -> TipoIncapacidadOut:
        entity = self.repoin.create(
            nombre=payload.nombre,
            descripcion=payload.descripcion,
            estado=payload.estado,
        )
        return TipoIncapacidadOut.model_validate(entity)

    def get(self, id_tipo_incapacidad: int) -> TipoIncapacidadOut | None:
        tipo = self.repoin.obtener_id(id_tipo_incapacidad)
        return None if tipo is None else TipoIncapacidadOut.model_validate(tipo)

    def list(self, skip: int = 0, limit: int = 100) -> List[TipoIncapacidadOut]:
        items = self.repoin.list(skip=skip, limit=limit)
        return [TipoIncapacidadOut.model_validate(x) for x in items]

    def update(self, id_tipo_incapacidad: int, payload: TipoIncapacidadUpdate) -> TipoIncapacidadOut | None:
        entity = self.repoin.update(
            id_tipo_incapacidad,
            nombre=payload.nombre,
            descripcion=payload.descripcion,
            estado=payload.estado,
        )
        return None if entity is None else TipoIncapacidadOut.model_validate(entity)

    def delete(self, id_tipo_incapacidad: int) -> bool:
        return self.repoin.delete(id_tipo_incapacidad)