from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))

    accounts = relationship('Account', back_populates='user')

    def __repr__(self):
        return f'User<first_name={self.first_name}, last_name={self.last_name}>'


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='accounts')

    def __repr__(self):
        return f'Account<name={self.fullname}, user={self.user_id}>'