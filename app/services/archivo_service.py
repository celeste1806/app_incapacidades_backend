from typing import List
from sqlalchemy.orm import Session

from app.models.archivo import Archivo
from app.repositories.archivo_repository import ArchivoRepository
from app.schemas.archivo import ArchivoCreate, ArchivoOut, ArchivoUpdate

class ArchivoService:
    def __init__(self, db: Session) -> None:
        self.repoin = ArchivoRepository(db)
        
    def create(self, payload: ArchivoCreate) -> ArchivoOut:
        entity = self.repoin.create(payload)
        return ArchivoOut.model_validate(entity)

    def get(self, id_archivo: int) -> ArchivoOut | None:
        tipo = self.repoin.obtener_id(id_archivo)
        return None if tipo is None else ArchivoOut.model_validate(tipo)

    def list(self, skip: int = 0, limit: int = 100) -> List[ArchivoOut]:
        items = self.repoin.list(skip=skip, limit=limit)
        return [ArchivoOut.model_validate(x) for x in items]

    def update(self, id_archivo: int, payload: ArchivoUpdate) -> ArchivoOut | None:
        entity = self.repoin.update(
            id_archivo,
            nombre=payload.nombre,
            descripcion=payload.descripcion,
            estado=payload.estado,
        )
        return None if entity is None else ArchivoOut.model_validate(entity)

    def delete(self, id_archivo: int) -> bool:
        return self.repoin.delete(id_archivo)

    def list_by_tipo_incapacidad(self, tipo_incapacidad_id: int) -> List[ArchivoOut]:
        items = self.repoin.list_by_tipo_incapacidad(tipo_incapacidad_id)
        return [ArchivoOut.model_validate(x) for x in items]