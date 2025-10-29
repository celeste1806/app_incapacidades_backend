from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_token
from app.repositories.usuario_repository import UsuarioRepository


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    print(f"DEBUG: Token recibido: {credentials.credentials[:20]}...")
    try:
        payload = decode_token(credentials.credentials)
        user_id = payload.get("sub")
        print(f"DEBUG: Payload decodificado - user_id: {user_id}, payload: {payload}")
        if user_id is None:
            raise ValueError("sub faltante")
    except Exception as e:
        print(f"DEBUG: Error al decodificar token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    repo = UsuarioRepository(db)
    user = repo.get(int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Validar que el usuario esté activo
    if not user.estado:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    
    return user


def get_current_employee(current_user = Depends(get_current_user)):
    print(f"DEBUG: Usuario ID: {current_user.id_usuario}, Rol: {current_user.rol_id}, Estado: {current_user.estado}")
    if current_user.rol_id != 9:
        raise HTTPException(status_code=403, detail="Acceso restringido a empleados")
    return current_user


def get_current_admin(current_user = Depends(get_current_user)):
    if current_user.rol_id != 10:
        raise HTTPException(status_code=403, detail="Acceso restringido a administradores")
    return current_user


def get_current_employee_or_admin(current_user = Depends(get_current_user)):
    """Permite acceso a empleados (9) y administradores (10)."""
    if current_user.rol_id not in (9, 10):
        raise HTTPException(status_code=403, detail="Acceso restringido a empleados/administradores")
    return current_user
