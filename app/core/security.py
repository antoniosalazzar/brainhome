from passlib.context import CryptContext
from datetime import datetime, timedelta,timezone
from typing import Optional
from jose import JWTError, jwt
from app.core.config import settings

# Configuracion de bcrypt para hashing de passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashea un password en texto plano usando bcrypt.
    
    Args:
        password: Password en texto plano
        
    Returns:
        Hash bcrypt del password
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si un password en texto plano coincide con su hash bcrypt.
    
    Args:
        plain_password: Password en texto plano
        hashed_password: Hash bcrypt del password
        
    Returns:
        True si coinciden, False en caso contrario
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un JWT firmado con expiración.
    
    Args:
        data: Payload a incluir en el token (ej: {"sub": "user@example.com"})
        expires_delta: Tiempo de vida del token (default: ACCESS_TOKEN_EXPIRE_MINUTES)
    
    Returns:
        Token JWT firmado como string
    """
    to_encode = data.copy()

    # Obtener tiempo actual con timezone UTC
    now = datetime.now(timezone.utc)

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[str]:
    """
    Decodifica un JWT token y extrae el email (claim 'sub').
    
    Args:
        token: JWT token a decodificar
        
    Returns:
        Email del usuario si el token es válido, None si no
    """
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        email: Optional[str] = payload.get("sub")
        return email  # Esto puede ser str o None
    except JWTError:
        return None