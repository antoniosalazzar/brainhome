from passlib.context import CryptContext

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