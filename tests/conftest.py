import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.database import Base
from app.models import Wallet
from app.main import get_db, app


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def async_engine():
    database_url = "postgresql+asyncpg://postgres:postgres@localhost:5433/wallets_test"

    engine = create_async_engine(
        database_url,
        echo=False,
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture()
async def db_session(async_engine):
    AsyncSessionLocalTest = async_sessionmaker(async_engine, expire_on_commit=False)
    async with AsyncSessionLocalTest() as session:
        yield session


@pytest_asyncio.fixture()
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()



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
