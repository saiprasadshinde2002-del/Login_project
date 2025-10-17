from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., example="Product A")
    description: Optional[str] = Field(None, example="Product description")
    price: float = Field(..., gt=0, example=000)
    quantity: int = Field(..., ge=0, example=10)
    tags: List[str] = Field(default_factory=list, example=["tag1", "tag2"])

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str = Field(..., example="Product A")
    description: Optional[str]
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    tags: List[str] = Field(default_factory=list, example=[])

class ProductOut(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
