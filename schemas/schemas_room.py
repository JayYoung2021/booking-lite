from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, constr, condecimal

from regexs import ROOM_NUMBER_REGEX
from enums import RoomType, RoomStatus


class RoomBase(BaseModel):
    room_number: constr(strip_whitespace=True, regex=ROOM_NUMBER_REGEX)
    type_: RoomType
    price: condecimal(ge=Decimal(0.00), max_digits=2)


class RoomCreate(RoomBase):
    pass


class RoomOut(RoomBase):
    id: int
    room_status: RoomStatus

    class Config:
        org_mode = True


class RoomUpdate(BaseModel):
    type_: Optional[RoomType] = None
    price_min: Optional[condecimal(ge=Decimal(0.00), max_digits=2)] = None
    price_max: Optional[condecimal(ge=Decimal(0.00), max_digits=2)] = None
    room_status: Optional[RoomStatus] = None
