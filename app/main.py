from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select
from .database import AsyncSessionLocal
from .models import Wallet
from .schemas import OperationTypeBase, AmountBase

app = FastAPI()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get('/')
def hello():
    return 'hello'

@app.get('/api/v1/wallets/{WALLET_UUID}')
async def get_balance(WALLET_UUID: int, db: AsyncSession = Depends(get_db)):
    query = select(Wallet).where(Wallet.id == WALLET_UUID)
    try:
        result = await db.execute(query)
        wallet = result.scalars().one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Нет кошелька {WALLET_UUID}')
    return wallet.amount


@app.post('/api/v1/wallets/{WALLET_UUID}/operation')
async def change_balance(WALLET_UUID: int,
                  operation_type: OperationTypeBase,
                  amount: AmountBase,
                  db: AsyncSession = Depends(get_db)):
    async with db.begin():
        query = select(Wallet).where(Wallet.id == WALLET_UUID).with_for_update()
        result = await db.execute(query)
        wallet = result.scalars().one()
        if operation_type.type == 'DEPOSIT':
            wallet.amount += amount.amount
        else:
            wallet.amount -= amount.amount
    return wallet
        






        

