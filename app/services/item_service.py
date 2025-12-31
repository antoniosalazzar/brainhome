# app/services/item_service.py
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


def create_item(
    db: Session, 
    item_create: ItemCreate,
    owner_id: int
) -> Item:
    """
    Crea un nuevo ítem en la base de datos

    Args:
        db (Session): Sesión de base de datos
        item_create (ItemCreate): Datos del ítem a crear
        owner_id (int): ID del usuario propietario del ítem

    Returns:
        Item: El ítem creado
    """
    db_item = Item(
        title=item_create.title,
        description=item_create.description,
        owner_id=owner_id  # Asignar el propietario del ítem
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)  # Refrescar para obtener datos generados (como ID)
    return db_item


def get_item(
    db: Session, 
    item_id: int,
    owner_id: int
) -> Optional[Item]:
    """
    Obtiene un ítem por su ID y el ID del propietario

    Args:
        db (Session): Sesión de base de datos
        item_id (int): ID del ítem a obtener
        owner_id (int): ID del usuario propietario del ítem

    Returns:
        Optional[Item]: El ítem si se encuentra, None en caso contrario
    """
    return db.query(Item).filter(
        Item.id == item_id, 
        Item.owner_id == owner_id
    ).first()


def get_user_items(
    db: Session,
    owner_id: int,
    skip: int = 0,
    limit: int = 50
) -> List[Item]:
    """
    Obtiene una lista de ítems para un usuario específico

    Args:
        db (Session): Sesión de base de datos
        owner_id (int): ID del usuario propietario de los ítems
        skip (int, optional): Número de ítems a omitir para paginación. Defaults to 0.
        limit (int, optional): Número máximo de ítems a retornar. Defaults to 100.

    Returns:
        List[Item]: Lista de ítems del usuario
    """
    return db.query(Item).filter(
        Item.owner_id == owner_id
    ).offset(skip).limit(limit).all()


def update_item(
    db: Session,
    item_id: int,
    owner_id: int,
    item_update: ItemUpdate
) -> Optional[Item]:
    """
    Actualiza un ítem existente

    Args:
        db (Session): Sesión de base de datos
        item_id (int): ID del ítem a actualizar
        owner_id (int): ID del usuario propietario del ítem
        item_update (ItemUpdate): Datos para actualizar el ítem

    Returns:
        Item: El ítem actualizado

    Nota: usa exclude_unset para actualizar solo los campos proporcionados
    """
    # 1. Buscar el item y verificar dueño
    db_item = db.query(Item).filter(
        Item.id == item_id,
        Item.owner_id == owner_id
    ).first()
    
    if not db_item:
        return None
    
    # 2. Actualizar solo campos enviados
    update_data = item_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if value is not None:
            setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(
    db: Session,
    item_id: int,
    owner_id: int
) -> bool:
    """
    Elimina un item si existe y pertenece al usuario.
    
    Args:
        db: Sesión de base de datos
        item_id: ID del item a eliminar
        owner_id: ID del dueño (para verificación)
    
    Returns:
        True si se eliminó, False si no existe/no pertenece
    """
    db_item = db.query(Item).filter(
        Item.id == item_id,
        Item.owner_id == owner_id
    ).first()
    
    if not db_item:
        return False
    
    db.delete(db_item)
    db.commit()
    return True