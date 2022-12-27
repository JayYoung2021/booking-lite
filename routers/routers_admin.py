from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas
from dependencies import get_db, get_current_admin

router = APIRouter(
    prefix='/admins',
    tags=['admins'],
    dependencies=[Depends(get_current_admin)]
)


@router.post(
    '/',
    response_model=schemas.AdminOut,
    status_code=status.HTTP_201_CREATED
)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    is_admin_exist: bool = crud.is_admin_exist_by_job_number(db, admin.job_number)
    if is_admin_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Job number already registered"
        )
    return crud.create_admin(db, admin)
