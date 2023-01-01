from enum import Enum


class RoomType(Enum):
    SINGLE = "single"
    TWIN = "twin"
    FAMILY = "family"


class RoomStatus(Enum):
    VACANT = "vacant"
    OCCUPIED = "occupied"
    DIRTY = "dirty"
    RESERVED = "reserved"


class PaymentStatus(Enum):
    UNPAID = "unpaid"
    PAID = "paid"
