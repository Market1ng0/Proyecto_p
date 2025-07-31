from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse # Importación clave
from app.core.database import get_db # Importación clave
from app.controllers import item as item_controller # Importación clave
from app.dependencies import get_current_active_user # ¡Importación clave!
from app.models.user import User # Importación clave

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo ítem (requiere autenticación)")
def create_new_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user) # ¡Ruta protegida!
):
    return item_controller.create_item(item=item, db=db, current_user=current_user)

@router.get("/", response_model=List[ItemResponse], summary="Obtener todos los ítems (requiere autenticación)")
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user) # ¡Ruta protegida!
):
    return item_controller.get_items(db=db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=ItemResponse, summary="Obtener un ítem por ID (requiere autenticación)")
def read_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user) # ¡Ruta protegida!
):
    return item_controller.get_item_by_id(item_id=item_id, db=db)

@router.put("/{item_id}", response_model=ItemResponse, summary="Actualizar un ítem (solo por su dueño, requiere autenticación)")
def update_existing_item(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user) # ¡Ruta protegida!
):
    return item_controller.update_item(item_id=item_id, item=item, db=db, current_user=current_user)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un ítem (solo por su dueño, requiere autenticación)")
def delete_existing_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user) # ¡Ruta protegida!
):
    item_controller.delete_item(item_id=item_id, db=db, current_user=current_user)
    return