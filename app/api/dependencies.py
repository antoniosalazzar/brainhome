from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User


# Esquema de seguridad HTTP Bearer
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency para obtener el usuario actual desde el token JWT.
    
    Args:
        credentials: Token JWT del header Authorization
        db: Sesión de BD
        
    Returns:
        Usuario autenticado
        
    Raises:
        HTTPException 401 si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Extraer token del header Authorization: Bearer <token>
    token = credentials.credentials
    
    # decode_access_token devuelve el email directamente o None
    email = decode_access_token(token)
    
    if email is None:
        raise credentials_exception
    
    # Buscar usuario en BD
    user = db.query(User).filter(User.email == email).first()
    
    if user is None:
        raise credentials_exception
    
    if user.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user