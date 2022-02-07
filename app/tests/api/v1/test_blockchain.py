from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from blockchain.blockchain import Blockchain
from schemas.transaction import TransactionCreate
from tests.factories.account import AccountFactory

faker = Faker('en_US')


def test_get_chain(
    client: TestClient,
    blockchain: Blockchain,
) -> None:
    chain = blockchain.chain

    response = client.get('/chain')
    content = response.json()

    assert len(content) == len(chain)


def test_mine__success(
    client: TestClient,
    blockchain: Blockchain,
    db: Session
) -> None:
    account_factory = AccountFactory(db)
    account1 = account_factory.create()
    account2 = account_factory.create()

    transaction1 = TransactionCreate(sender=account1.id, recipient=account2.id, value=1000)
    transaction2 = TransactionCreate(sender=account2.id, recipient=account1.id, value=100)
    blockchain.add_transaction(transaction1)
    blockchain.add_transaction(transaction2)

    response = client.post('/chain/mine')
    content = response.json()

    assert content == 'New block added at position 1'


def test_mine__fail_to_add(
    mocker,
    client: TestClient,
    blockchain: Blockchain,
    db: Session
) -> None:
    mocker.patch('blockchain.blockchain.Blockchain.add_block', return_value=False)
    account_factory = AccountFactory(db)
    account1 = account_factory.create()
    account2 = account_factory.create()

    transaction1 = TransactionCreate(sender=account1.id, recipient=account2.id, value=1000)
    transaction2 = TransactionCreate(sender=account2.id, recipient=account1.id, value=100)
    blockchain.add_transaction(transaction1)
    blockchain.add_transaction(transaction2)

    response = client.post('/chain/mine')
    content = response.json()

    assert content == 'Block not added'


def test_mine__no_transactions(
    mocker,
    client: TestClient,
    blockchain: Blockchain,
    db: Session
) -> None:
    blockchain.unconfirmed_transactions = []

    response = client.post('/chain/mine')
    content = response.json()

    assert content == 'No transactions in pool'