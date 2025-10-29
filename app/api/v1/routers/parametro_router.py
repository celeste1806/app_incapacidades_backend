from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.parametro import ParametroCreate, ParametroOut, ParametroUpdate
from app.services.parametro_service import ParametroService


router = APIRouter(prefix="/parametros", tags=["parametros"])


def get_service(db: Session = Depends(get_db)) -> ParametroService:
    return ParametroService(db)


@router.post("", response_model=ParametroOut, status_code=status.HTTP_201_CREATED)
def create_parametro(payload: ParametroCreate, service: ParametroService = Depends(get_service)):
    return service.create(payload)


@router.get("/{id_parametro}", response_model=ParametroOut)
def get_parametro(id_parametro: int, service: ParametroService = Depends(get_service)):
    result = service.get(id_parametro)
    if result is None:
        raise HTTPException(status_code=404, detail="Parametro no encontrado")
    return result


@router.get("", response_model=list[ParametroOut])
def list_parametros(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: ParametroService = Depends(get_service),
):
    return service.list(skip=skip, limit=limit)


@router.put("/{id_parametro}", response_model=ParametroOut)
def update_parametro(
    id_parametro: int,
    payload: ParametroUpdate,
    service: ParametroService = Depends(get_service),
):
    result = service.update(id_parametro, payload)
    if result is None:
        raise HTTPException(status_code=404, detail="Parametro no encontrado")
    return result


@router.delete("/{id_parametro}", status_code=status.HTTP_204_NO_CONTENT)
def delete_parametro(id_parametro: int, service: ParametroService = Depends(get_service)):
    ok = service.delete(id_parametro)
    if not ok:
        raise HTTPException(status_code=404, detail="Parametro no encontrado")
    return None


