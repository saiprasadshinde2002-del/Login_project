from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserOut, Token
from models.user import User
from security.auth import hash_password, verify_password, create_access_token
from api.deps import get_db
from tasks.jobs import send_welcome_email


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserOut, status_code=201)
def signup(body: UserCreate, db: Session= Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=body.email,
        full_name=body.full_name,
        hashed_password=hash_password(body.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    send_welcome_email.delay(user.email)
    return user

@router.post("/login", response_model=Token)
def login(body: UserCreate, db: Session= Depends(get_db)):
    user=db.query(User).filter(User.email==body.email).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token=create_access_token(sub=user.email)
    return Token(access_token=token)




