import json

from hashlib import sha256
from time import time

from schemas.transaction import TransactionCreate


class Block:
    def __init__(self, index: int, transactions: list, previous_hash: str, nonce=0):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = time()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    DIFFICULTY = 2

    def __init__(self):
        self.chain = []
        self.unconfirmed_transactions = []

        genesis_block = Block(0, [], 'GENESIS_BLOCK')
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction: TransactionCreate):
        data = transaction.dict(exclude_unset=True)
        self.unconfirmed_transactions.append(data)

    def add_block(self, block: Block, proof: str) -> bool:
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def proof_of_work(self, block: Block):
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.DIFFICULTY):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def is_valid_proof(self, block: Block, hash: str) -> bool:
        is_difficulty_satisfied = hash.startswith('0' * Blockchain.DIFFICULTY)
        is_hash_equal = block.compute_hash() == hash

        return is_difficulty_satisfied and is_hash_equal

    def mine(self) -> str:
        if not self.unconfirmed_transactions:
            return 'No transactions in pool'

        block = Block(
            index=self.last_block.index + 1,
            transactions=self.unconfirmed_transactions,
            previous_hash=self.last_block.hash
        )

        proof = self.proof_of_work(block)
        if not self.add_block(block, proof):
            return 'Block not added'

        self.unconfirmed_transactions = []
        return f'New block added at position {block.index}'
