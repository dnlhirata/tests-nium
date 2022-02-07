from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Any

from crud.user import create_user as crud_create_user
from crud.user import delete_user
from crud.user import get_user
from crud.user import get_users
from crud.user import update_user as crud_update_user
from schemas.user import User as UserSchema
from schemas.user import UserCreate as UserCreateSchema
from schemas.user import UserUpdate as UserUpdateSchema

from ...deps import get_db


router = APIRouter(
    prefix='/users',
)


@router.get('/', response_model=list[UserSchema])
def list_users(db: Session = Depends(get_db)) -> Any:
    return get_users(db)


@router.get("/{user_id}", response_model=UserSchema)
def retrieve_user(user_id: int, db: Session = Depends(get_db)) -> Any:
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=UserSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)) -> Any:
    created_user = crud_create_user(db=db, user=user)
    return created_user


@router.put('/{user_id}', response_model=UserSchema)
def update_user(
    user_id: int,
    user_data: UserUpdateSchema,
    db: Session = Depends(get_db)
) -> Any:
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud_update_user(db=db, user=db_user, user_data=user_data)


@router.delete('/{user_id}', response_model=UserSchema)
def remove_user(user_id: int, db: Session = Depends(get_db)) -> Any:
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return delete_user(db=db, user_id=user_id)
