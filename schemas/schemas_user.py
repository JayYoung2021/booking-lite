from typing import Optional

from pydantic import BaseModel, constr

from regexs import PHONE_NUMBER_REGEX, IDENTITY_NUMBER_REGEX


class UserBase(BaseModel):
    name: constr(strip_whitespace=True)
    phone_number: constr(strip_whitespace=True, regex=PHONE_NUMBER_REGEX)
    identity_number: constr(strip_whitespace=True, regex=IDENTITY_NUMBER_REGEX)


class UserCreate(UserBase):
    password: constr(strip_whitespace=True)


class UserOut(UserBase):
    id: int

    # orders: List[Order] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True)] = None
    phone_number: Optional[constr(strip_whitespace=True, regex=PHONE_NUMBER_REGEX)] = None
    identity_number: Optional[constr(strip_whitespace=True, regex=IDENTITY_NUMBER_REGEX)] = None
