from typing import Optional

from sqlalchemy.orm import Session

import models
import schemas
import security


def create_admin(db: Session, admin: schemas.AdminCreate) -> models.Admin:
    hashed_password = security.get_password_hash(admin.password)
    db_admin = models.Admin(
        job_number=admin.job_number,
        name=admin.name,
        hashed_password=hashed_password
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


def get_admin_by_id(db: Session, admin_id: int) -> Optional[models.Admin]:
    return db.query(models.Admin).filter(models.Admin.id == admin_id).first()


def get_admin_by_job_number(db: Session, job_number: str) -> Optional[models.Admin]:
    return db.query(models.Admin).filter(models.Admin.job_number == job_number).first()


def update_admin(
        db: Session,
        admin_id: int,
        admin: schemas.AdminUpdate
) -> models.Admin:
    db_admin: models.Admin = get_admin_by_id(db, admin_id)
    if admin.name is not None:
        db_admin.name = admin.name
    if admin.new_password is not None:
        db_admin.hashed_password = security.get_password_hash(admin.new_password)
    db.commit()
    db.refresh(db_admin)
    return db_admin


def delete_admin(db: Session, admin_id: int) -> None:
    db_admin = get_admin_by_id(db, admin_id)
    db.delete(db_admin)
    db.commit()


def is_admin_exist_by_job_number(db: Session, job_number: str) -> bool:
    return get_admin_by_job_number(db, job_number) is not None


def authenticate_admin(db: Session, job_number: str, password: str) -> bool:
    admin: models.Admin = get_admin_by_job_number(db, job_number)
    return security.verify_password(password, admin.hashed_password)
