import pytest

@pytest.mark.asyncio
async def test_get_wallet_balance(client, wallet):
    response = await client.get("/app/v1/wallets/1")

    assert response.status_code == 200
    assert response.json()["amount"] == 1000


@pytest.mark.asyncio
async def test_deposit_wallet(client, wallet):
    response = await client.post(
        "/app/v1/wallets/2/operation",
        json={
            "operation_type": "DEPOSIT",
            "amount": 200,
        }
    )
    assert response.status_code == 200
    assert response.json()["amount"] == 700


@pytest.mark.asyncio
async def test_withdraw_wallet(client, wallet):
    response = await client.post(
        "/app/v1/wallets/1/operation",
        json={
            "operation_type": "WITHDRAW",
            "amount": 200,
        }
    )
    assert response.status_code == 200
    assert response.json()["amount"] == 800