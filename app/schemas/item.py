from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    """Schema base con campos comunes del ítem"""
    title: str = Field(..., max_length=200, min_length=1, description="Título del ítem")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción opcional")

class ItemCreate(ItemBase):
    """Schema para la creación de un nuevo ítem"""
    pass

class ItemRead(ItemBase):
    """Schema para la respuesta del ítem"""
    id: int
    owner_id: int
    created_at: Optional[datetime] = None  # ← Opcional
    updated_at: Optional[datetime] = None  # ← Opcional

    class Config:
        from_attributes = True  # Permite crear desde ORM models

class ItemUpdate(BaseModel):
    """Schema para actualizar un ítem (todos los campos opcionales)"""
    title: Optional[str] = None
    description: Optional[str] = None

