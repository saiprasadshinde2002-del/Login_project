from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from api.deps import get_db, get_current_user
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate, ProductOut
from models.user import User

router = APIRouter(prefix="/products", tags=["products"])

def verify_admin(user: User):
    if not getattr(user, "is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_admin(current_user)
    try:
        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create product")

@router.get("/", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_admin(current_user)
    products = db.query(Product).all()
    return products

@router.get("/{product_id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_admin(current_user)
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.patch("/{product_id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_admin(current_user)
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    try:
        update_data = product_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update product")

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_admin(current_user)
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    try:
        db.delete(product)
        db.commit()
        return
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete product")
