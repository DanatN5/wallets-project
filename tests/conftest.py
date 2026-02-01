import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app, get_db
from app.models import Base, Wallet

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/wallets_test"

engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
AsyncSessionLocalTest = async_sessionmaker(engine_test, expire_on_commit=False)

@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture()
async def db_session():
    async with AsyncSessionLocalTest() as session:
        yield session

@pytest.fixture()
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest.fixture()
async def wallets(db_session):
    w1 = Wallet(id=1, amount=1000)
    w2 = Wallet(id=2, amount=500)
    
    db_session.add_all([w1, w2])
    await db_session.commit()

    return {1: w1, 2: w2}
