from sqlalchemy import Column, Integer, String, Float, Enum

from database import Base
from enums import RoomType, RoomStatus


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    phone_number = Column(String, unique=True, index=True)
    identity_number = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # is_active = Column(Boolean, default=True)


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    room_number = Column(String, unique=True, index=True)
    type_ = Column(Enum(RoomType), index=True)
    price = Column(Float, index=True)
    room_status = Column(Enum(RoomStatus), index=True, default=RoomStatus.VACANT)


# class Order(Base):
#     __tablename__ = "orders"
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     user = relationship("User", backref="users")
#     room_id = Column(Integer, ForeignKey("rooms.id"))
#     room = relationship("Room", backref="rooms")
#     # check_in_time = Column()
#     stay_length = Column(Integer)
#     expense = Column(Float)
#     payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.UNPAID)


# class Admin(Base):
#     __tablename__ = "admins"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     hashed_password = Column(String)
