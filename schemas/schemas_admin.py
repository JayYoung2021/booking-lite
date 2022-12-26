from typing import Optional

from pydantic import BaseModel, constr

from regexs import JOB_NUMBER_REGEX


class AdminBase(BaseModel):
    job_number: constr(strip_whitespace=True, regex=JOB_NUMBER_REGEX)
    name: constr(strip_whitespace=True)


class AdminCreate(AdminBase):
    password: constr(strip_whitespace=True)


class AdminOut(AdminBase):
    id: int

    class Config:
        orm_mode = True


class AdminUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True)]
    password: Optional[constr(strip_whitespace=True)]
