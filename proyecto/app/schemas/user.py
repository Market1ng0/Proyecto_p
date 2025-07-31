from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase): # Para uso interno, por ejemplo, en controladores
    id: int
    hashed_password: str
    is_active: bool

    class Config:
        from_attributes = True

class UserResponse(UserBase): # Para la respuesta de la API al cliente
    id: int
    is_active: bool

    class Config:
        from_attributes = True