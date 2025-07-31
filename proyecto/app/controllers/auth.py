from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User # Importación clave
from app.schemas.user import UserCreate, UserResponse # Importación clave
from app.core.security import get_password_hash, verify_password, create_access_token # Importación clave
from app.schemas.token import Token # Importación clave
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.config import get_settings # Importación clave

settings = get_settings()

def register_user(user: UserCreate, db: Session) -> UserResponse:
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nombre de usuario ya registrado")
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya registrado")

    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponse.from_orm(db_user)

def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: Session) -> Token:
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}