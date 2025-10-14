from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True
    is_admin: bool = False
    


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str | None = None
    password: str
    is_admin: bool = False

class UserUpdate(BaseModel):
    full_name: str | None = None
    password: str | None = None

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
