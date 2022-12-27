from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from dependencies import get_db, get_current_admin

router = APIRouter(
    prefix='/admins/me',
    tags=["admins"],
    dependencies=[Depends(get_current_admin)]
)


@router.get(
    '/',
    response_model=schemas.AdminOut,
    status_code=status.HTTP_200_OK,
)
def read_admin_me(current_admin: schemas.AdminOut = Depends(get_current_admin)):
    return current_admin


@router.patch(
    '/',
    response_model=schemas.AdminOut,
    status_code=status.HTTP_200_OK
)
def update_admin_me(
        admin: schemas.AdminUpdate,
        db: Session = Depends(get_db),
        current_admin: schemas.AdminOut = Depends(get_current_admin)
):
    if crud.authenticate_admin(db, current_admin.job_number, admin.password):
        return crud.update_admin(db, current_admin.id, admin)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect password"
    )


@router.delete(
    '/',
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_admin_me(
        admin: schemas.AdminDelete,
        db: Session = Depends(get_db),
        current_admin: schemas.AdminOut = Depends(get_current_admin)
):
    if crud.authenticate_admin(db, current_admin.job_number, admin.password):
        crud.delete_admin(db, current_admin.id)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect password"
    )
