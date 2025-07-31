from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import get_settings # Importación clave

settings = get_settings()

# --- Líneas de Depuración ---
print(f"DEBUG: SECRET_KEY cargada en security.py: {settings.SECRET_KEY[:5]}...") # Muestra solo los primeros 5 caracteres
print(f"DEBUG: ALGORITHM cargado en security.py: {settings.ALGORITHM}")
# --- Fin Líneas de Depuración ---

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    # --- Línea de Depuración ---
    print(f"DEBUG: Token creado con SECRET_KEY: {settings.SECRET_KEY[:5]}... y ALGORITHM: {settings.ALGORITHM}")
    # --- Fin Líneas de Depuración ---
    
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # --- Línea de Depuración ---
        print(f"DEBUG: Token decodificado con SECRET_KEY: {settings.SECRET_KEY[:5]}... y ALGORITHM: {settings.ALGORITHM}")
        # --- Fin Línea de Depuración ---
        
        return payload
    except JWTError:
        # --- Línea de Depuración ---
        print("DEBUG: JWTError al decodificar el token. Posiblemente token inválido o expirado.")
        # --- Fin Línea de Depuración ---
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar la credencial",
            headers={"WWW-Authenticate": "Bearer"},
        )
    