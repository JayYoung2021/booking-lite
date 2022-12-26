from typing import Optional

from pydantic import BaseModel, constr

from .schemas_user import UserUpdate


class UserUpdateWithPassword(UserUpdate):
    password: constr(strip_whitespace=True)
    new_password: Optional[constr(strip_whitespace=True)] = None


class UserDeleteWithPassword(BaseModel):
    password: constr(strip_whitespace=True)
