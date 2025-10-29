from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.auth_dependency import get_current_admin
from app.schemas.parametro_hijo import ParametroHijoCreate, ParametroHijoOut, ParametroHijoUpdate
from app.services.parametro_hijo_service import ParametroHijoService


router = APIRouter(prefix="/parametro_hijo", tags=["parametro_hijo"])

def get_service(db: Session = Depends(get_db)) -> ParametroHijoService:
    return ParametroHijoService(db)

@router.post("", response_model=ParametroHijoOut, status_code=status.HTTP_201_CREATED)
def create_parametro_hijo(
    payload: ParametroHijoCreate, 
    service: ParametroHijoService = Depends(get_service),
    admin = Depends(get_current_admin)
):
    return service.create(payload)

@router.get("/{id_parametro_hijo}", response_model=ParametroHijoOut)
def get_parametro(id_parametro_hijo: int, service: ParametroHijoService = Depends(get_service)):
    result = service.get(id_parametro_hijo)
    if result is None:
        raise HTTPException(status_code=404, detail="Parametro hijo no encontrado")
    return result


@router.get("", response_model=list[ParametroHijoOut])
def list_parametro_hijo(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: ParametroHijoService = Depends(get_service),
):
    return service.list(skip=skip, limit=limit)

@router.put("/{id_parametro_hijo}", response_model=ParametroHijoOut)
def update_parametro_hijo(
    id_parametro_hijo: int,
    payload: ParametroHijoUpdate,
    service: ParametroHijoService = Depends(get_service),
    admin = Depends(get_current_admin)
):
    result = service.update(id_parametro_hijo, payload)
    if result is None:
        raise HTTPException(status_code=404, detail="Parametro hijo no encontrado")
    return result

@router.delete("/{id_parametro_hijo}", status_code=status.HTTP_204_NO_CONTENT)
def delete_parametro_hijo(
    id_parametro_hijo: int, 
    service: ParametroHijoService = Depends(get_service),
    admin = Depends(get_current_admin)
):
    ok = service.delete(id_parametro_hijo)
    if not ok:
        raise HTTPException(status_code=404, detail="Parametro hijo no encontrado")
    return None

@router.get("/papashijos/{id_parametro}", response_model=list[ParametroHijoOut])
def papashijos( 
    id_parametro: int,
    service: ParametroHijoService = Depends(get_service)):

    return service.hijospapa(id_parametro)

@router.put("/cambiar_estado/{id_parametro_hijo}", response_model=bool)
def cambiar_estado ( 
    id_parametro_hijo: int,
    service: ParametroHijoService = Depends(get_service)):

    return service.cambiar_estado(id_parametro_hijo)