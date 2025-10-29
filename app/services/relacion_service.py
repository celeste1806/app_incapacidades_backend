from typing import List
from sqlalchemy.orm import Session

from app.repositories.relacion_repository import RelacionRepository
from app.schemas.relacion import RelacionCreate, RelacionOut, RelacionWithNamesOut
from app.schemas.archivo import ArchivoOut
from app.repositories.tipo_incapacidad import TipoIncapacidadRepository
from app.repositories.archivo_repository import ArchivoRepository


class RelacionService:
    def __init__(self, db: Session) -> None:
        self.repo = RelacionRepository(db)
        self.tipo_repo = TipoIncapacidadRepository(db)
        self.archivo_repo = ArchivoRepository(db)

    # 1) Obtener todos los objetos, con opción de validar si existen
    def list(self, *, skip: int = 0, limit: int = 100, raise_if_empty: bool = False) -> List[RelacionOut]:
        items = self.repo.list(skip=skip, limit=limit)
        if raise_if_empty and not items:
            raise LookupError("No existen relaciones registradas")
        # Enriquecer con nombres
        result: List[dict] = []
        for x in items:
            tipo = self.tipo_repo.get(x.tipo_incapacidad_id)
            arch = self.archivo_repo.get(x.archivo_id)
            result.append({
                "tipo_incapacidad_id": x.tipo_incapacidad_id,
                "tipo_incapacidad_nombre": getattr(tipo, "nombre", None) if tipo else None,
                "archivo_id": x.archivo_id,
                "archivo_nombre": getattr(arch, "nombre", None) if arch else None,
            })
        return result

    # 2) Crear un objeto relacion
    def create(self, payload: RelacionCreate) -> RelacionOut:
        # Validar existencia de tipo_incapacidad
        if self.tipo_repo.get(payload.tipo_incapacidad_id) is None:
            raise ValueError(f"tipo_incapacidad_id inexistente: {payload.tipo_incapacidad_id}")
        # Validar existencia de archivo
        if self.archivo_repo.get(payload.archivo_id) is None:
            raise ValueError(f"archivo_id inexistente: {payload.archivo_id}")
        # Validar duplicados
        if self.repo.exists(payload.tipo_incapacidad_id, payload.archivo_id):
            raise ValueError("La relación ya existe para los identificadores proporcionados")
        entity = self.repo.create(
            tipo_incapacidad_id=payload.tipo_incapacidad_id,
            archivo_id=payload.archivo_id,
        )
        return RelacionOut.model_validate(entity)

    # 3) Eliminar un objeto relacion por (tipo_incapacidad_id, archivo_id)
    def delete(self, tipo_incapacidad_id: int, archivo_id: int) -> bool:
        return self.repo.delete(tipo_incapacidad_id=tipo_incapacidad_id, archivo_id=archivo_id)

    # 4) Obtener todos los objetos con el mismo tipo_incapacidad_id
    def list_by_tipo_incapacidad(self, tipo_incapacidad_id: int, *, raise_if_empty: bool = False) -> List[RelacionOut]:
        items = self.repo.list_by_tipo_incapacidad(tipo_incapacidad_id=tipo_incapacidad_id)
        if raise_if_empty and not items:
            raise LookupError("No existen relaciones para el tipo_incapacidad_id proporcionado")
        result: List[dict] = []
        for x in items:
            tipo = self.tipo_repo.get(x.tipo_incapacidad_id)
            arch = self.archivo_repo.get(x.archivo_id)
            result.append({
                "tipo_incapacidad_id": x.tipo_incapacidad_id,
                "tipo_incapacidad_nombre": getattr(tipo, "nombre", None) if tipo else None,
                "archivo_id": x.archivo_id,
                "archivo_nombre": getattr(arch, "nombre", None) if arch else None,
            })
        return result

    # 5) Obtener lista de archivos asociados a un tipo_incapacidad_id
    def list_archivos_by_tipo_incapacidad(self, tipo_incapacidad_id: int) -> List[ArchivoOut]:
        archivos = self.archivo_repo.list_by_tipo_incapacidad(tipo_incapacidad_id)
        return [ArchivoOut.model_validate(a) for a in archivos]