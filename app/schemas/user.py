from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    """Schema base con campos comunes del usuario"""
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    """Schema para la creación de un nuevo usuario (recibe password en texto plano)"""
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")


class UserResponse(UserBase):
    """Schema para la respuesta del usuario (sin password)"""
    id: int

    class Config:
        from_attributes = True # Permite crear desde ORM models

class UserUpdate(BaseModel):
    """Schema para actualizar un usuario (todos los campos opcionales)"""
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, description="Password must be at least 8 characters long")
    is_active: Optional[bool] = None