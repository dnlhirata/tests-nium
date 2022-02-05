from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str
    last_name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    modified_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    name: str
    user_id: int
    type: str


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    modified_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True