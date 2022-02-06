from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class AccountBase(BaseModel):
    name: str
    user_id: int
    type: str


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    name: Optional['str']


class Account(AccountBase):
    id: int
    modified_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True