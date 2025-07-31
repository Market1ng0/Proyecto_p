from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserResponse # Importación clave
from app.schemas.token import Token # Importación clave
from app.core.database import get_db # Importación clave
from app.controllers import auth as auth_controller # Importación clave

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, summary="Registrar un nuevo usuario")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return auth_controller.register_user(user=user, db=db)

@router.post("/login", response_model=Token, summary="Iniciar sesión y obtener token de acceso")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_controller.login_for_access_token(form_data=form_data, db=db)