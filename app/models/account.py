
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship

from models.database import Base


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    type = Column(Enum('CHECKING', 'SAVING', name='account_types'))
    user_id = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='accounts')

    def __repr__(self):
        return f'Account<name={self.fullname}, user={self.user_id}>'