from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from blockchain.blockchain import Blockchain
from schemas.transaction import TransactionCreate
from tests.factories.account import AccountFactory

faker = Faker('en_US')


def test_get_transactions(
    client: TestClient,
    blockchain: Blockchain,
    db: Session
) -> None:
    account_factory = AccountFactory(db)
    account1 = account_factory.create()
    account2 = account_factory.create()

    transaction1 = TransactionCreate(sender=account1.id, recipient=account2.id, value=1000)
    transaction2 = TransactionCreate(sender=account2.id, recipient=account1.id, value=100)
    transaction3 = TransactionCreate(sender=account2.id, recipient=account1.id, value=10000)
    blockchain.add_transaction(transaction1)
    blockchain.add_transaction(transaction2)

    response = client.get('/transactions')
    content = response.json()

    assert response.status_code == 200
    assert len(content) == len(blockchain.unconfirmed_transactions)
    assert transaction1.dict() in content
    assert transaction2.dict() in content
    assert transaction3.dict() not in content


def test_create_transaction__success(
    client: TestClient,
    blockchain: Blockchain,
    db: Session
) -> None:
    account_factory = AccountFactory(db)
    account1 = account_factory.create()
    account2 = account_factory.create()

    data = {
        'sender': account1.id,
        'recipient': account2.id,
        'value': 1000
    }

    response = client.post(
        '/transactions/new',
        headers={'X-Token': faker.word()},
        json=data
    )

    assert response.status_code == 200


def test_create_transaction__sender_not_exist(
    client: TestClient,
    blockchain: Blockchain,
    db: Session
) -> None:
    account_factory = AccountFactory(db)
    account = account_factory.create()

    data = {
        'sender': 999,
        'recipient': account.id,
        'value': 1000
    }

    response = client.post(
        '/transactions/new',
        headers={'X-Token': faker.word()},
        json=data
    )
    content = response.json()

    assert response.status_code == 404
    assert content['detail'] == f'Sender(999) account not found'


def test_create_transaction__recipient_not_exist(
    client: TestClient,
    blockchain: Blockchain,
    db: Session
) -> None:
    account_factory = AccountFactory(db)
    account = account_factory.create()

    data = {
        'sender': account.id,
        'recipient': 999,
        'value': 1000
    }

    response = client.post(
        '/transactions/new',
        headers={'X-Token': faker.word()},
        json=data
    )
    content = response.json()

    assert response.status_code == 404
    assert content['detail'] == f'Recipient(999) account not found'


def test_create_transaction__self_transaction(
    client: TestClient,
    blockchain: Blockchain,
    db: Session
) -> None:
    account_factory = AccountFactory(db)
    account = account_factory.create()

    data = {
        'sender': account.id,
        'recipient': account.id,
        'value': 1000
    }

    response = client.post(
        '/transactions/new',
        headers={'X-Token': faker.word()},
        json=data
    )
    content = response.json()

    assert response.status_code == 400
    assert content['detail'] == 'You cannot make a transaction to yourself'