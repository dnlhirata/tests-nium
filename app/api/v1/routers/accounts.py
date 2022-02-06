from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from crud.account import create_account as crud_create_account
from crud.account import get_account
from crud.account import get_accounts
from crud.account import update_account as crud_update_account
from schemas.account import Account as AccountSchema
from schemas.account import AccountCreate as AccountCreateSchema
from schemas.account import AccountUpdate as AccountUpdateSchema

from ...deps import get_db


router = APIRouter(
    prefix='/accounts',
)


@router.get('/', response_model=list[AccountSchema])
def list_users(db: Session = Depends(get_db)):
    return get_accounts(db)


@router.get("/{account_id}", response_model=AccountSchema)
def retrieve_account(account_id: int, db: Session = Depends(get_db)):
    db_account = get_account(db=db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@router.post("/", response_model=AccountSchema)
def create_user(account: AccountCreateSchema, db: Session = Depends(get_db)):
    created_account = crud_create_account(db=db, account=account)
    return created_account


@router.put('/{account_id}', response_model=AccountSchema)
def update_account(account_id: int, account_data: AccountUpdateSchema, db: Session = Depends(get_db)):
    db_account = get_account(db=db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return crud_update_account(db=db, account=db_account, account_data=account_data)
    
