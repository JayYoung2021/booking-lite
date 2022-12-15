from enum import Enum


class EnhancedEnum(Enum):
    @classmethod
    def has_value(cls, value):
        return value in (it.value for it in cls)


class RoomType(EnhancedEnum):
    SINGLE = "single"
    TWIN = "twin"
    FAMILY = "family"


class RoomStatus(EnhancedEnum):
    VACANT = "vacant"
    OCCUPIED = "occupied"
    DIRTY = "dirty"
    RESERVED = "reserved"


class PaymentStatus(EnhancedEnum):
    UNPAID = "unpaid"
    PAID = "paid"
