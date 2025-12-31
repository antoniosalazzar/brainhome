# app/api/endpoints/items.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.item import Item
from app.schemas.user import UserResponse
from app.schemas.item import ItemCreate, ItemUpdate, ItemRead
from app.services.item_service import (
    create_item, 
    get_item, 
    get_user_items, 
    update_item, 
    delete_item
)

# Usar prefix y tags para mejor organización
router = APIRouter()

@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item_endpoint(
    item: ItemCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo ítem para el usuario autenticado.
    """
    db_item = create_item(
        db=db, 
        item_create=item, 
        owner_id=current_user.id
    )
    return db_item


@router.get("/", response_model=list[ItemRead])
def read_user_items(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50    
):
    """
    Obtiene todos los ítems del usuario autenticado.
    
    Parámetros de consulta:
    - skip: Número de items a saltar (paginación)
    - limit: Máximo número de items a retornar
    """
    items = get_user_items(
        db=db, 
        owner_id=current_user.id, 
        skip=skip, 
        limit=limit
    )
    return items


@router.get("/{item_id}", response_model=ItemRead)
def read_item(
    item_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene un ítem específico por su ID.
    
    Solo funciona si el item pertenece al usuario autenticado.
    """
    db_item = get_item(
        db=db, 
        item_id=item_id, 
        owner_id=current_user.id
    )
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    return db_item


@router.put("/{item_id}", response_model=ItemRead)
def update_item_endpoint(
    item_id: int,
    item_update: ItemUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza un ítem existente.
    
    Solo actualiza los campos proporcionados en la solicitud.
    """
    # 1. Buscar el item (sin verificar owner todavía)
    item = db.query(Item).filter(Item.id == item_id).first()
    
    # 2. Validaciones detalladas
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    
    if item.owner_id is not current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso")
    
    # 3. Llamar al servicio (ahora sin verificación de owner)
    updated_item = update_item(
        db=db, 
        item_id=item_id,
        owner_id=current_user.id,
        item_update=item_update
    )
    
    return updated_item



@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_endpoint(
    item_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Elimina un ítem.
    """
    item = db.query(Item).filter(Item.id == item_id).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado"
        )
    
    if item.owner_id is not current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este item"
        )
    
    # Llamar al servicio modificado
    delete_item(db=db, item_id=item_id, owner_id=current_user.id)
    
    # No return para status 204