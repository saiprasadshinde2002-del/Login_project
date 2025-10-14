from sqlalchemy import String, Boolean, Column, Integer
from sqlalchemy.orm import mapped_column, Mapped
from db.base import Base

class User(Base):
    __tablename__ = "emp"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)