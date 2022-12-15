from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    phone_number: str
    identify_number: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    # is_active: bool
    # orders: List[Order] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    identify_number: Optional[str] = None
