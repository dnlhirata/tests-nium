from faker import Faker
from sqlalchemy.orm import Session

from crud.account import create_account
from models.account import Account
from models.user import User
from schemas.account import AccountCreate as AccountSchemaCreate

from .user import UserFactory

faker = Faker('en_US')


class AccountFactory(object):
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def _get_user(self) -> User:
        user_factory = UserFactory(self.db)
        return user_factory.create()

    def create(self) -> Account:
        name = faker.first_name()
        type = faker.random_element(elements=('CHECKING', 'SAVING'))
        user = self._get_user()

        account_to_create = AccountSchemaCreate(
            name=name,
            type=type,
            user_id=user.id
        )

        created_account = create_account(db=self.db, account=account_to_create)
        return created_account
        