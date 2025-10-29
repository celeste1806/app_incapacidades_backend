from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.relacion import RelacionCreate, RelacionOut, RelacionWithNamesOut
from app.schemas.archivo import ArchivoOut
from app.services.relacion_service import RelacionService


router = APIRouter(prefix="/relacion", tags=["relacion"])


def get_service(db: Session = Depends(get_db)) -> RelacionService:
    return RelacionService(db)


@router.get("", response_model=list[RelacionWithNamesOut])
def list_relaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: RelacionService = Depends(get_service),
):
    return service.list(skip=skip, limit=limit)


@router.post("", response_model=RelacionOut, status_code=status.HTTP_201_CREATED)
def create_relacion(payload: RelacionCreate, service: RelacionService = Depends(get_service)):
    try:
        return service.create(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_relacion(
    tipo_incapacidad_id: int,
    archivo_id: int,
    service: RelacionService = Depends(get_service),
):
    ok = service.delete(tipo_incapacidad_id, archivo_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")
    return None


@router.get("/por_tipo/{tipo_incapacidad_id}", response_model=list[RelacionWithNamesOut])
def list_relacion_por_tipo(
    tipo_incapacidad_id: int,
    service: RelacionService = Depends(get_service),
):
    return service.list_by_tipo_incapacidad(tipo_incapacidad_id)


@router.get("/por_tipo/{tipo_incapacidad_id}/archivos", response_model=list[ArchivoOut])
def list_archivos_por_tipo(
    tipo_incapacidad_id: int,
    service: RelacionService = Depends(get_service),
):
    return service.list_archivos_by_tipo_incapacidad(tipo_incapacidad_id)

