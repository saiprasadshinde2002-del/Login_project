from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.deps import get_db, get_current_user
from models.user import User
from schemas.user import UserOut, UserUpdate
from security.auth import hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(User).all()

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return user

@router.patch("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    body: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    print(current_user.id, current_user.is_admin)


    # Only allow if same user or admin
    if current_user.id == user_id or current_user.is_admin:
        if body.full_name is not None:
            user.full_name = body.full_name
        if body.password is not None:
            user.hashed_password = hash_password(body.password)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    else:
        raise HTTPException(status_code=403, detail="Not authorized")

    

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Only allow if same user or admin
    if current_user.id == user_id or current_user.is_admin:
        db.delete(user)
        db.commit()
        return
    else:
        raise HTTPException(status_code=403, detail="Not authorized")

    
