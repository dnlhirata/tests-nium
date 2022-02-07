from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from blockchain.blockchain import Blockchain
from crud.account import get_account
from schemas.transaction import TransactionCreate

from ...deps import get_blockchain
from ...deps import get_db

router = APIRouter(
    prefix='/transactions',
)


@router.get('/')
def get_transactions(blockchain: Blockchain = Depends(get_blockchain)) -> list:
    return blockchain.unconfirmed_transactions


@router.post('/new')
def create_transaction(
    transaction: TransactionCreate,
    blockchain: Blockchain = Depends(get_blockchain),
    db: Session = Depends(get_db)
) -> None:
    sender_account = get_account(db, transaction.sender)
    if not sender_account:
        raise HTTPException(
            status_code=404,
            detail=f'Sender({transaction.sender}) account not found'
        )

    recipient_account = get_account(db, transaction.recipient)
    if not recipient_account:
        raise HTTPException(
            status_code=404,
            detail=f'Recipient({transaction.recipient}) account not found'
        )

    if sender_account == recipient_account:
        raise HTTPException(
            status_code=400,
            detail=f'You cannot make a transaction to yourself'
        )

    blockchain.add_transaction(transaction)
