from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from crud.user import get_users
from tests.factories.user import UserFactory

faker = Faker('en_US')


def test_get_users(client: TestClient, db: Session) -> None:
    user_factory = UserFactory(db)
    user = user_factory.create()

    response = client.get('/users')
    content = response.json()

    users = get_users(db)

    assert response.status_code == 200
    assert len(content) == len(users)


def test_get_user(client: TestClient, db: Session) -> None:
    user_factory = UserFactory(db)
    user = user_factory.create()

    response = client.get(f'/users/{user.id}')
    content = response.json()

    assert response.status_code == 200
    assert content['id'] == user.id
    assert content['first_name'] == user.first_name
    assert content['last_name'] == user.last_name


def test_create_user(client: TestClient, db: Session) -> None:
    first_name, last_name = faker.first_name(), faker.last_name()
    data = {'first_name': first_name, 'last_name': last_name}

    response = client.post('/users/', headers={'X-Token': faker.word()}, json=data)
    content = response.json()

    assert response.status_code == 200
    assert content['first_name'] == first_name
    assert content['last_name'] == last_name


def test_update_user(client: TestClient, db: Session) -> None:
    first_name = faker.first_name()
    data = {'first_name': first_name}

    user_factory = UserFactory(db)
    user = user_factory.create()

    assert user.first_name != first_name

    response = client.put(f'/users/{user.id}', headers={'X-Token': faker.word()}, json=data)
    content = response.json()

    assert response.status_code == 200
    assert content['first_name'] == first_name


def test_delete_user(client: TestClient, db: Session) -> None:
    user_factory = UserFactory(db)
    user = user_factory.create()

    response = client.delete(f'/users/{user.id}', headers={'X-Token': faker.word()})
    content = response.json()

    assert response.status_code == 200
    assert content['id'] == user.id

    response = client.get(f'/users/{user.id}')
    assert response.status_code == 404