from datetime import datetime
from pydantic import BaseModel


class TransactionBase(BaseModel):
    sender: int
    recipient: int
    value: float


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    pass
