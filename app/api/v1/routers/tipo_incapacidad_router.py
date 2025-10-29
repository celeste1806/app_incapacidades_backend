from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.tipo_incapacidad import TipoIncapacidadCreateV2, TipoIncapacidadOut, TipoIncapacidadUpdate
from app.services.tipo_incapacidad import TipoIncapacidadService

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> TipoIncapacidadService:
    return TipoIncapacidadService(db)


@router.post("/tipo_incapacidad", response_model=TipoIncapacidadOut)
def create_tipo_incapacidad(
    payload: TipoIncapacidadCreateV2,
    service: TipoIncapacidadService = Depends(get_service),
):
    return service.create(payload)


@router.get("/tipo_incapacidad/{id_tipo_incapacidad}", response_model=TipoIncapacidadOut)
def get_tipo_incapacidad(
    id_tipo_incapacidad: int,
    service: TipoIncapacidadService = Depends(get_service),
):
    result = service.get(id_tipo_incapacidad)
    if result is None:
        raise HTTPException(status_code=404, detail="Tipo de incapacidad no encontrado")
    return result


@router.get("/tipo_incapacidad", response_model=list[TipoIncapacidadOut])
def list_tipo_incapacidad(
    skip: int = 0,
    limit: int = 100,
    service: TipoIncapacidadService = Depends(get_service),
):
    return service.list(skip=skip, limit=limit)


@router.put("/tipo_incapacidad/{id_tipo_incapacidad}", response_model=TipoIncapacidadOut)
def update_tipo_incapacidad(
    id_tipo_incapacidad: int,
    payload: TipoIncapacidadUpdate,
    service: TipoIncapacidadService = Depends(get_service),
):
    result = service.update(id_tipo_incapacidad, payload)
    if result is None:
        raise HTTPException(status_code=404, detail="Tipo de incapacidad no encontrado")
    return result


@router.delete("/tipo_incapacidad/{id_tipo_incapacidad}")
def delete_tipo_incapacidad(
    id_tipo_incapacidad: int,
    service: TipoIncapacidadService = Depends(get_service),
):
    success = service.delete(id_tipo_incapacidad)
    if not success:
        raise HTTPException(status_code=404, detail="Tipo de incapacidad no encontrado")
    return {"message": "Tipo de incapacidad eliminado correctamente"}
