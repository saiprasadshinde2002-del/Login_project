from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
def create_access_token(sub: str) -> str:
    to_encode = {"sub": sub, 'exp': datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)}
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_alg)

def decode_token(token: str) -> str | None:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg]).get("sub")
    except JWTError:
        return None
    
