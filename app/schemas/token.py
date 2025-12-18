from pydantic import BaseModel

class Token(BaseModel):
    """Schema para respuesta de login"""
    access_token: str
    token_type: str = "bearer"  # Tipo de token, por defecto "bearer"

class TokenData(BaseModel):
    """Schema para datos dentro del token"""
    email: str | None = None