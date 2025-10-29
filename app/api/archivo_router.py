from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.archivo import ArchivoCreate, ArchivoOut, ArchivoUpdate
from app.services.archivo_service import ArchivoService

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> ArchivoService:
    return ArchivoService(db)


@router.post("/archivo", response_model=ArchivoOut)
def create_archivo(
    payload: ArchivoCreate,
    service: ArchivoService = Depends(get_service),
):
    return service.create(payload)


@router.get("/archivo/{id_archivo}", response_model=ArchivoOut)
def get_archivo(
    id_archivo: int,
    service: ArchivoService = Depends(get_service),
):
    result = service.get(id_archivo)
    if result is None:
        raise HTTPException(status_code=404, detail="archivo no encontrado" )
    return result


@router.get("/archivo", response_model=List[ArchivoOut])
def list_archivo(
    skip: int = 0,
    limit: int = 100,
    service: ArchivoService = Depends(get_service),
):
    return service.list(skip=skip, limit=limit)


@router.put("/archivo/{id_archivo}", response_model=ArchivoOut)
def update_archivo(
    id_archivo: int,
    payload: ArchivoUpdate,
    service: ArchivoService = Depends(get_service),
):
    result = service.update(id_archivo, payload)
    if result is None:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return result


@router.delete("/archivo/{id_archivo}")
def delete_archivo(
    id_archivo: int,
    service: ArchivoService = Depends(get_service),
):
    success = service.delete(id_archivo)
    if not success:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return {"message": "Archivo eliminado correctamente"}


@router.get("/archivo/por_tipo/{tipo_incapacidad_id}", response_model=List[ArchivoOut])
def list_archivo_por_tipo(
    tipo_incapacidad_id: int,
    service: ArchivoService = Depends(get_service),
):
    return service.list_by_tipo_incapacidad(tipo_incapacidad_id)