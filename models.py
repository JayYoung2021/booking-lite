from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base
from enums import RoomType, RoomStatus, PaymentStatus


class User(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    phone_number = Column(String, unique=True, index=True)
    identity_number = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # is_active = Column(Boolean, default=True)
    orders = relationship('Order', back_populates='user')


class Room(Base):
    __tablename__ = "room_table"

    id = Column(Integer, primary_key=True)
    room_number = Column(String, unique=True, index=True)
    type_ = Column(Enum(RoomType), index=True)
    price = Column(Float, index=True)
    room_status = Column(Enum(RoomStatus), index=True, default=RoomStatus.VACANT)
    orders = relationship('Order', back_populates='room')


class Order(Base):
    __tablename__ = "order_table"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    user = relationship("User", back_populates="orders")
    room_id = Column(Integer, ForeignKey("room_table.id"))
    room = relationship("Room", back_populates="orders")
    check_in_time = Column(DateTime)
    stay_length = Column(Integer)
    expense = Column(Float)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.UNPAID)


class Admin(Base):
    __tablename__ = "admin_table"

    id = Column(Integer, primary_key=True)
    job_number = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    hashed_password = Column(String)
