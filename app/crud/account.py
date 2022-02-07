from sqlalchemy.orm import Session
from typing import List

from models.account import Account as Account
from schemas.account import Account as AccountSchema
from schemas.account import AccountUpdate as AccountUpdateSchema


def get_account(db: Session, account_id: int) -> Account:
    return db.query(Account).filter(Account.id == account_id).first()


def get_accounts(db: Session) -> List[Account]:
    return db.query(Account).all()


def create_account(db: Session, account: AccountSchema) -> Account:
    db_account = Account(
        name=account.name,
        type=account.type,
        user_id=account.user_id
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    
    return db_account


def update_account(
    db: Session,
    account: AccountSchema,
    account_data: AccountUpdateSchema
) -> Account:
    data = account_data.dict(exclude_unset=True)

    for field in data:
        if field in Account.__table__.columns.keys():
            setattr(account, field, data[field])
    
    db.add(account)
    db.commit()
    db.refresh(account)

    return account


def delete_account(db: Session, account_id: int) -> Account:
    account = db.query(Account).get(account_id)
    db.delete(account)
    db.commit()
    return account