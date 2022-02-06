from sqlalchemy.orm import Session

from models.user import User as User
from schemas.user import User as UserSchema
from schemas.user import UserCreate as UserCreateSchema
from schemas.user import UserUpdate as UserUpdateSchema


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, user: UserCreateSchema):
    db_user = User(first_name=user.first_name, last_name=user.last_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def update_user(db: Session, user: UserSchema, user_data: UserUpdateSchema):
    data = user_data.dict(exclude_unset=True)

    for field in data:
        if field in User.__table__.columns.keys():
            setattr(user, field, data[field])
    
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: int):
    user = db.query(User).get(user_id)
    db.delete(user)
    db.commit()
    return user