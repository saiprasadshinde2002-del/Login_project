# app/api/deps.py
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from db.session import sessionlocal
from security.auth import decode_token
from models.user import User

# Single shared security scheme
security = HTTPBearer(auto_error=False)

def get_db() -> Generator[Session, None, None]:
    db = sessionlocal()  # make sure this matches your sessionmaker name
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    # 1) Require Authorization header with Bearer scheme
    if not creds or creds.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    # 2) Decode JWT; must return a dict with 'sub'
    payload = decode_token(creds.credentials)
    if not isinstance(payload, dict) or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    # 3) Load user by subject (email) and require active status
    sub_value = payload.get("sub") if isinstance(payload, dict) else None
    user = db.query(User).filter(User.email == sub_value).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive or missing user",
        )

    return user