from faker import Faker
from sqlalchemy.orm import Session

from crud.user import create_user
from crud.user import delete_user
from crud.user import get_user
from crud.user import get_users
from crud.user import update_user
from schemas.user import UserCreate
from schemas.user import UserUpdate
from tests.factories.user import UserFactory

faker = Faker('en_US')


def test_get_user(db: Session) -> None:
    user_factory = UserFactory(db)
    user = user_factory.create()

    retrieved_user = get_user(db=db, user_id=user.id)

    assert retrieved_user == user


def test_get_users(db: Session) -> None:
    user_factory = UserFactory(db)
    user1 = user_factory.create()
    user2 = user_factory.create()

    users = get_users(db=db)

    assert user1 in users
    assert user2 in users


def test_create_user(db: Session) -> None:
    first_name, last_name = faker.first_name(), faker.last_name()
    data = UserCreate(first_name=first_name, last_name=last_name)

    user = create_user(db=db, user=data)

    assert user.first_name == first_name
    assert user.last_name == last_name


def test_update_user(db: Session) -> None:
    user_factory = UserFactory(db)
    user = user_factory.create()

    first_name = faker.first_name()
    data = UserUpdate(first_name=first_name)

    assert user.first_name != first_name

    updated_user = update_user(db=db, user=user, user_data=data)

    assert updated_user.first_name == first_name


def test_delete_user(db: Session) -> None:
    user_factory = UserFactory(db)
    user = user_factory.create()

    deleted_user = delete_user(db=db, user_id=user.id)
    assert deleted_user.id == user.id

    user = get_user(db=db, user_id=user.id)
    assert user == None


