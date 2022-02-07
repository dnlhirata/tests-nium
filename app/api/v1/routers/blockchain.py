import json

from fastapi import APIRouter
from fastapi import Depends
from typing import Any

from blockchain.blockchain import Blockchain

from ...deps import get_blockchain

router = APIRouter(
    prefix='/chain',
)


@router.post('/')
def get_chain(
    blockchain: Blockchain = Depends(get_blockchain)
) -> Any:
    chain = []
    for block in blockchain.chain:
        b = block.__dict__
        if hasattr(b, 'nonce'):
            b.pop('nonce')
        chain.append(b)
    return json.dumps({'chain': chain, 'length': len(chain)})


@router.post('/mine')
def mine(blockchain: Blockchain = Depends(get_blockchain)) -> str:
    msg = blockchain.mine()
    return msg
