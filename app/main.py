import uvicorn

from fastapi import FastAPI

from api.v1.routers.accounts import router as account_router
from api.v1.routers.blockchain import router as blockchain_router
from api.v1.routers.transactions import router as transaction_router
from api.v1.routers.users import router as user_router


app = FastAPI()

app.include_router(account_router)
app.include_router(blockchain_router)
app.include_router(transaction_router)
app.include_router(user_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)