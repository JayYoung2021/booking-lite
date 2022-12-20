from sqlalchemy.orm import Session

import models
import schemas


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "not-really-hashed"
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


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_phone_number(db: Session, phone_number: str):
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()


def get_user_by_identity_number(db: Session, identity_number: str):
    return db.query(models.User).filter(models.User.identity_number == identity_number).first()


def get_users(db: Session, name: str):
    criterion: tuple = () if name is None else (models.User.name == name,)  # never delete the comma
    return db.query(models.User).filter(*criterion).all()


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user: models.User = get_user_by_id(db, user_id)
    update_data: dict = user.dict(exclude_unset=True)
    db_user = db_user.copy(update=update_data)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    db.delete(db_user)
    db.commit()
