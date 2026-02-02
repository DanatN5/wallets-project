import pytest
import pytest_asyncio
import asyncpg
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.database import Base
from app.models import Wallet

POSTGRES_URL = "postgresql://postgres:postgres@localhost:5432/postgres"
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/wallets_test"

engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
AsyncSessionLocalTest = async_sessionmaker(engine_test, expire_on_commit=False)

@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def prepare_test_database():
    conn = await asyncpg.connect(POSTGRES_URL)

    try:
        await conn.execute("CREATE DATABASE wallets_test")
    except asyncpg.DuplicateDatabaseError:
        pass
    await conn.close()

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine_test.dispose()



@pytest_asyncio.fixture()
async def db_session():
    async with AsyncSessionLocalTest() as session:
        yield session



@pytest_asyncio.fixture()
async def wallets(db_session):
    wallet_1 = Wallet(id=1, amount=1000)
    wallet_2 = Wallet(id=2, amount=500)
    
    db_session.add_all([wallet_1, wallet_2])
    await db_session.commit()

    return {
        "wallet_1": wallet_1,
        "wallet_2": wallet_2,
    }
