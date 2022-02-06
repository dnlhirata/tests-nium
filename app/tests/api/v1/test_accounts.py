from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from crud.account import get_accounts
from tests.factories.account import AccountFactory
from tests.factories.user import UserFactory

faker = Faker('en_US')


def test_get_accounts(client: TestClient, db: Session) -> None:
    account_factory = AccountFactory(db)
    account = account_factory.create()

    response = client.get('/accounts')
    content = response.json()

    accounts = get_accounts(db)

    assert response.status_code == 200
    assert len(content) == len(accounts)

def test_get_account(client: TestClient, db: Session) -> None:
    account_factory = AccountFactory(db)
    account = account_factory.create()

    response = client.get(f'/accounts/{account.id}')
    content = response.json()

    assert response.status_code == 200
    assert content['id'] == account.id
    assert content['name'] == account.name
    assert content['type'] == account.type
    assert content['user_id'] == account.user_id


def test_create_account(client: TestClient, db: Session) -> None:
    name = faker.word()
    type = 'CHECKING'
    user_factory = UserFactory(db)
    user = user_factory.create()

    data = {'name': name, 'type': type, 'user_id': user.id}

    response = client.post('/accounts/', headers={"X-Token": faker.word()}, json=data)
    content = response.json()

    assert response.status_code == 200
    assert content['name'] == name
    assert content['type'] == type


def test_update_account(client: TestClient, db: Session) -> None:
    name = faker.word()
    data = {'name': name}

    account_factory = AccountFactory(db)
    account = account_factory.create()

    assert account.name != name

    response = client.put(f'/accounts/{account.id}', headers={"X-Token": faker.word()}, json=data)
    content = response.json()

    assert response.status_code == 200
    assert content['name'] == name


def test_delete_account(client: TestClient, db: Session) -> None:
    account_factory = AccountFactory(db)
    account = account_factory.create()

    response = client.delete(f'/accounts/{account.id}', headers={"X-Token": faker.word()})
    content = response.json()

    assert response.status_code == 200
    assert content['id'] == account.id

    response = client.get(f'/accounts/{account.id}')
    assert response.status_code == 404
