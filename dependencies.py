import datetime

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
from security import oauth2_scheme, SECRET_KEY, ALGORITHM


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_admin(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> schemas.AdminCreate:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        job_number: str = payload.get('sub')
        if job_number is None:
            raise credentials_exception
        expire_time: datetime.datetime = datetime.datetime.fromtimestamp(payload.get('exp'))
        if datetime.datetime.utcnow() > expire_time:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    admin = crud.get_admin_by_job_number(db, job_number)
    if admin is None:
        raise credentials_exception
    return admin
