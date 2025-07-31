"""Módulo para la gestión de dependencias y autenticación de usuarios."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.security import decode_access_token
from app.core.database import get_db
from app.models.user import User
from app.schemas.token import TokenData
from jose import JWTError # Importación adicional necesaria para el try/except

oauth2_scheme = HTTPBearer(auto_error=False) # auto_error=False para manejar la excepción manualmente

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Obtiene el usuario actual a partir del token JWT proporcionado.
    Lanza HTTPException si el token es inválido o el usuario no existe.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar la credencial",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Si no hay credenciales, significa que no se envió el token
    if not credentials:
        raise credentials_exception

    try:
        # El token ahora viene en credentials.credentials
        payload = decode_access_token(credentials.credentials)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as exc:
        raise credentials_exception from exc

    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Verifica si el usuario actual está activo.
    Lanza HTTPException si el usuario está inactivo.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return current_user
    