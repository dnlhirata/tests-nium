from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    accounts = relationship('Account', back_populates='user')

    def __repr__(self):
        return f'User<first_name={self.first_name}, last_name={self.last_name}>'


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    type = Column(Enum('CHECKING', 'SAVING', name='account_types'))
    user_id = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='accounts')

    def __repr__(self):
        return f'Account<name={self.fullname}, user={self.user_id}>'