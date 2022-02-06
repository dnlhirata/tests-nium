from typing import Optional

from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]


class User(UserBase):
    id: int
    modified_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True
