from typing import Optional

from sqlalchemy.orm import Session

import models
import schemas


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        name=user.name,
        phone_number=user.phone_number,
        identify_number=user.identify_number,
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    db.delete(db_user)
    db.commit()


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if user.name is not None:
        db_user.name = user.name
    if user.phone_number is not None:
        db_user.phone_number = user.phone_number
    if user.identify_number is not None:
        db_user.identify_number = user.identify_number
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_phone_number(db: Session, phone_number: str):
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()


def get_user_by_identify_number(db: Session, identify_number: str):
    return db.query(models.User).filter(models.User.identify_number == identify_number).first()


def get_users(db: Session):
    return db.query(models.User).all()


def get_users_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).all()
