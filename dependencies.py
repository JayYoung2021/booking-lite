import datetime

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session

import schemas
from crud import get_user_by_phone_number
from database import SessionLocal
from security import oauth2_scheme, SECRET_KEY, ALGORITHM


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> schemas.UserCreate:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone_number: str = payload.get('sub')
        if phone_number is None:
            raise credentials_exception
        # token_data = schemas.TokenData(phone_number=phone_number)
        expire_time: datetime.datetime = datetime.datetime.fromtimestamp(payload.get('exp'))
        if datetime.datetime.utcnow() > expire_time:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_phone_number(db, phone_number)
    if user is None:
        raise credentials_exception
    return user
