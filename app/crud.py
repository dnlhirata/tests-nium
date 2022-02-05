from sqlalchemy.orm import Session

from ..db.models import User
from ..db.schemas import User as UserSchema


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserSchema):
    user = User(first_name=user.first_name, last_name=user.last_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user