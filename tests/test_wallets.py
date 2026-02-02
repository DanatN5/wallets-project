import pytest
from httpx import AsyncClient

from app.main import app
from app.models import Wallet


@pytest.mark.asyncio
async def test_get_wallet_balance(wallets, db_session):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/app/v1/wallets/1")

    assert response.status_code == 200
    assert response.json()["amount"] == 1000


@pytest.mark.asyncio
async def test_deposit_wallet(wallets):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/app/v1/wallets/1/operation",
            json={
                "operation_type": "DEPOSIT",
                "amount": 200,
            }
        )
    assert response.status_code == 200
    assert response.json()["amount"] == 1200


