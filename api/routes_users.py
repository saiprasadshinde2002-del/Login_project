from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from api.deps import get_db, get_current_user
from models.user import User
from schemas.user import UserOut, UserUpdate
from security.auth import hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserOut], status_code=status.HTTP_200_OK)
def list_users(db: Session = Depends(get_db), _=Depends(get_current_user)):
    users = db.query(User).all()
    return users

@router.get("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
def update_user(
    user_id: int,
    body: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not (current_user.id == user_id or getattr(current_user, "is_admin", False)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    try:
        if body.full_name is not None:
            user.full_name = body.full_name
        if body.password is not None:
            user.hashed_password = hash_password(body.password)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update user")

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not (current_user.id == user_id or getattr(current_user, "is_admin", False)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    try:
        db.delete(user)
        db.commit()
        return
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete user")
