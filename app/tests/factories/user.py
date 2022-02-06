from faker import Faker
from sqlalchemy.orm import Session

from crud.user import create_user
from schemas.user import User as UserSchema
from schemas.user import UserCreate as UserSchemaCreate

faker = Faker('en_US')


class UserFactory(object):
    def __init__(self, db: Session):
        self.db = db

    def create(self) -> UserSchema:
        first_name = faker.first_name()
        last_name = faker.last_name()

        user_to_create = UserSchemaCreate(
            first_name=first_name,
            last_name=last_name
        )

        created_user = create_user(db=self.db, user=user_to_create)
        return created_user
        