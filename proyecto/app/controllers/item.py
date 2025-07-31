from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.item import Item # Importación clave
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse # Importación clave
from app.models.user import User # Importación clave

def create_item(item: ItemCreate, db: Session, current_user: User) -> ItemResponse:
    db_item = Item(**item.model_dump(), owner_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return ItemResponse.from_orm(db_item)

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[ItemResponse]:
    items = db.query(Item).offset(skip).limit(limit).all()
    return [ItemResponse.from_orm(item) for item in items]

def get_item_by_id(item_id: int, db: Session) -> ItemResponse:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
    return ItemResponse.from_orm(db_item)

def update_item(item_id: int, item: ItemUpdate, db: Session, current_user: User) -> ItemResponse:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para actualizar este item")

    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return ItemResponse.from_orm(db_item)

def delete_item(item_id: int, db: Session, current_user: User):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para eliminar este item")

    db.delete(db_item)
    db.commit()
    return {"message": "Item eliminado exitosamente"}