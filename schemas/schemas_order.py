import datetime

from pydantic import BaseModel, conint

from enums import PaymentStatus


class OrderBase(BaseModel):
    user_id: conint(ge=1)
    room_id: conint(ge=1)
    check_in_time: datetime.datetime
    stay_length: conint(ge=1)


class OrderCreate(OrderBase):
    pass


class OrderOut(OrderBase):
    id: int
    expense: float
    payment_status: PaymentStatus

    class Config:
        orm_mode = True
