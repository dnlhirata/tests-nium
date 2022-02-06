from faker import Faker
from sqlalchemy.orm import Session

from crud.account import create_account
from crud.account import get_account
from crud.account import get_accounts
from crud.account import update_account
from schemas.account import AccountCreate
from schemas.account import AccountUpdate
from tests.factories.account import AccountFactory
from tests.factories.user import UserFactory

faker = Faker('en_US')


def test_get_account(db: Session) -> None:
    account_factory = AccountFactory(db)
    account = account_factory.create()

    retrieved_account = get_account(db=db, account_id=account.id)

    assert retrieved_account == account


def test_get_accounts(db: Session) -> None:
    account_factory = AccountFactory(db)
    account1 = account_factory.create()
    account2 = account_factory.create()

    accounts = get_accounts(db=db)

    assert account1 in accounts
    assert account2 in accounts


def test_create_account(db: Session) -> None:
    name = faker.word()
    type = 'CHECKING'
    user_factory = UserFactory(db)
    user = user_factory.create()

    data = AccountCreate(name=name, type=type, user_id=user.id)

    account = create_account(db=db, account=data)

    assert account.name == name
    assert account.type == type
    assert account.user_id == user.id


def test_update_account(db: Session) -> None:
    account_factory = AccountFactory(db)
    account = account_factory.create()

    name = faker.word()
    data = AccountUpdate(name=name)

    assert account.name != name

    updated_account = update_account(db=db, account=account, account_data=data)

    assert updated_account.name == name