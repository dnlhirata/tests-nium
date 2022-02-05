import uvicorn

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from sqlalchemy.orm import Session

from services.crud import create_user as crud_create_user
from main.services.crud import get_user
from main.db.database import SessionLocal
from main.db.schemas import User as UserSchema
from main.db.schemas import UserCreate as UserCreateSchema

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}", response_model=UserSchema)
def retrieve_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=UserSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    created_user = crud_create_user(db=db, user=user)
    return created_user


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)