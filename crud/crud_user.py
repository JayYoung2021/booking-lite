from typing import Optional, List

from sqlalchemy.orm import Session

import models
import schemas
import security


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    fake_hashed_password = security.get_password_hash(user.password)
    print(user.password)
    print(fake_hashed_password)
    print(security.verify_password(user.password, fake_hashed_password))
    db_user = models.User(
        name=user.name,
        phone_number=user.phone_number,
        identity_number=user.identity_number,
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_phone_number(db: Session, phone_number: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()


def get_user_by_identity_number(db: Session, identity_number: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.identity_number == identity_number).first()


def get_users(db: Session, name: str) -> Optional[List[models.User]]:
    criterion: tuple = () if name is None else (models.User.name == name,)  # never delete the comma
    return db.query(models.User).filter(*criterion).all()


def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> models.User:
    db_user: models.User = get_user_by_id(db, user_id)
    update_data: dict = user.dict(exclude_unset=True)
    # https://github.com/tiangolo/fastapi/discussions/2561
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> None:
    db_user = get_user_by_id(db, user_id)
    db.delete(db_user)
    db.commit()


def get_user_orders(db: Session, user_id: int) -> Optional[List[models.Order]]:
    db_user = get_user_by_id(db, user_id)
    return db_user.orders


def is_user_exist_by_phone_number(db: Session, phone_number: str) -> bool:
    return get_user_by_phone_number(db, phone_number) is not None


def authenticate_user(db: Session, phone_number: str, password: str) -> bool:
    user: models.User = get_user_by_phone_number(db, phone_number)
    return security.verify_password(password, user.hashed_password)
