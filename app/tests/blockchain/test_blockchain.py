from blockchain.blockchain import Block
from blockchain.blockchain import Blockchain
from schemas.transaction import TransactionCreate


def test_init() -> None:
    blockchain = Blockchain()

    assert blockchain.unconfirmed_transactions == []
    assert len(blockchain.chain) == 1
    assert blockchain.chain[0].previous_hash == 'GENESIS_BLOCK'


def test_last_block() -> None:
    blockchain = Blockchain()
    previous_hash = blockchain.chain[0].hash
    transactions = [
        {
            'sender': 1,
            'recipient': 2,
            'value': 300
        }
    ]
    block = Block(
        index=1,
        transactions=transactions,
        previous_hash=previous_hash
    )
    blockchain.chain.append(block)

    assert blockchain.last_block == block


def test_add_transaction() -> None:
    blockchain = Blockchain()

    transaction = TransactionCreate(sender=1, recipient=2, value=1000)
    blockchain.add_transaction(transaction=transaction)

    assert len(blockchain.unconfirmed_transactions) == 1
    assert {'sender': 1, 'recipient': 2, 'value': 1000} in blockchain.unconfirmed_transactions


def test_add_block__success(
    mocker
) -> None:
    mocker.patch('blockchain.blockchain.Blockchain.is_valid_proof', return_value=True)
    blockchain = Blockchain()

    block = Block(
        index=1,
        transactions=[],
        previous_hash=blockchain.last_block.hash
    )

    result = blockchain.add_block(block, 'hash')

    assert result == True


def test_add_block__invalid_previous_hash(
    mocker
) -> None:
    mocker.patch('blockchain.blockchain.Blockchain.is_valid_proof', return_value=True)
    blockchain = Blockchain()

    block = Block(
        index=1,
        transactions=[],
        previous_hash='invalid_hash'
    )

    result = blockchain.add_block(block, 'hash')

    assert result == False


def test_add_block__invalid_proof(
    mocker
) -> None:
    mocker.patch('blockchain.blockchain.Blockchain.is_valid_proof', return_value=False)
    blockchain = Blockchain()

    block = Block(
        index=1,
        transactions=[],
        previous_hash=blockchain.last_block.hash
    )

    result = blockchain.add_block(block, 'hash')

    assert result == False


def test_proof_of_work() -> None:
    blockchain = Blockchain()

    block = Block(
        index=1,
        transactions=[],
        previous_hash=blockchain.last_block.hash
    )

    proof = blockchain.proof_of_work(block)

    assert proof.startswith('0' * blockchain.DIFFICULTY) == True


def test_is_valid_proof__valid(
    mocker
) -> None:
    mocker.patch('blockchain.blockchain.Block.compute_hash', return_value='00hash')

    blockchain = Blockchain()
    block = Block(
        index=1,
        transactions=[],
        previous_hash=blockchain.last_block.hash
    )

    is_valid = blockchain.is_valid_proof(block, '00hash')

    assert is_valid == True


def test_is_valid_proof__difficulty_not_satisfied(
    mocker
) -> None:
    mocker.patch('blockchain.blockchain.Block.compute_hash', return_value='00hash')

    blockchain = Blockchain()
    block = Block(
        index=1,
        transactions=[],
        previous_hash=blockchain.last_block.hash
    )

    is_valid = blockchain.is_valid_proof(block, 'hash')

    assert is_valid == False


def test_is_valid_proof__hash_not_equal(
    mocker
) -> None:
    mocker.patch('blockchain.blockchain.Block.compute_hash', return_value='00hash1')

    blockchain = Blockchain()
    block = Block(
        index=1,
        transactions=[],
        previous_hash=blockchain.last_block.hash
    )

    is_valid = blockchain.is_valid_proof(block, '00hash2')

    assert is_valid == False


def test_mine__success(mocker) -> None:
    mocker.patch('blockchain.blockchain.Blockchain.add_block', return_value=True)
    blockchain = Blockchain()
    blockchain.unconfirmed_transactions = [
        {
            'sender': 1,
            'recipient': 2,
            'value': 300
        }
    ]

    msg = blockchain.mine()

    assert msg == 'New block added at position 1'


def test_mine__invalid_block(mocker) -> None:
    mocker.patch('blockchain.blockchain.Blockchain.add_block', return_value=False)
    blockchain = Blockchain()
    blockchain.unconfirmed_transactions = [
        {
            'sender': 1,
            'recipient': 2,
            'value': 300
        }
    ]

    msg = blockchain.mine()

    assert msg == 'Block not added'


def test_mine__no_transactions() -> None:
    blockchain = Blockchain()

    msg = blockchain.mine()

    assert msg == 'No transactions in pool'
