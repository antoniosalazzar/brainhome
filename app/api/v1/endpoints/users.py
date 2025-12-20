from fastapi import Depends, APIRouter

from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Obtiene la información del usuario autenticado.
    
    Requiere: Token JWT válido en header Authorization: Bearer <token>
    
    Returns:
        Datos del usuario (id, email, is_active, is_superuser)
    """
    return current_user