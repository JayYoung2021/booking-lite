from typing import List, Union

from pydantic import BaseModel


class OrderBase(BaseModel):
    user_id: int
    room_id: int
    # check_in_time
    stay_length: int
    expense: float


class Order(OrderBase):
    pass


