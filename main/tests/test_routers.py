import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from main.app import app
from main.models.models import Rates, CargoTypes
from main.crud import RatePoster
import json
from tortoise.contrib.fastapi import register_tortoise


class JSONTest:

    def __init__(self, cargo_type_1: str = None,
                 cargo_type_2: str = None,
                 rate_1: str = None,
                 rate_2: str = None,
                 rate_3: str = None,
                 rate_4: str = None,
                 date_1: str = None,
                 date_2: str = None) -> None:
        self.cargo_type_1 = cargo_type_1 or "Glass"
        self.cargo_type_2 = cargo_type_2 or "Other"
        self.rate_1 = rate_1 or "0.04"
        self.rate_2 = rate_2 or "0.01"
        self.rate_3 = rate_3 or "0.035"
        self.rate_4 = rate_4 or "0.015"
        self.date_1 = date_1 or "2020-06-01"
        self.date_2 = date_2 or "2020-07-01"

    def get_payload(self) -> dict:
        return {
            self.date_1: [
                {
                    "cargo_type": self.cargo_type_1,
                    "rate": self.rate_1
                },
                {
                    "cargo_type": self.cargo_type_2,
                    "rate": self.rate_2
                }
            ],
            "2020-07-01": [
                {
                    "cargo_type": self.cargo_type_1,
                    "rate": self.rate_3
                },
                {
                    "cargo_type": self.cargo_type_2,
                    "rate": self.rate_4
                }
            ]
        }

@pytest.fixture(scope="function")
def client():
    register_tortoise(
        app,
        db_url="sqlite://:memory:",
        modules={"models": ["main.models.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as client:
        yield client


@pytest.mark.asyncio
async def test_post_rates(client):
    test_data = JSONTest()
    response = client.post('/api/rates', json=test_data.get_payload())
    assert response.status_code == 202
    cargo_glass = await CargoTypes.get(name=test_data.cargo_type_1)
    assert cargo_glass.name == test_data.cargo_type_1
    cargo_type_1_rates = await cargo_glass.rates
    assert float(test_data.rate_1) in [rate.rate for rate in cargo_type_1_rates]

    
@pytest.mark.asyncio
async def test_post_rates_wrong_data(client):
    response = client.post('/api/rates', json={"wrong_data": "wrong_data"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_post_rates_two_date_type_pair(client):
    test_data = JSONTest()
    payload = test_data.get_payload()
    payload[test_data.date_1].append({"cargo_type": test_data.cargo_type_1, "rate": test_data.rate_1})
    response = client.post('/api/rates', json=payload)
    assert response.status_code == 409

@pytest.mark.asyncio
async def test_get_rates(client):
    test_data = JSONTest()
    await RatePoster(test_data.get_payload()).post()
    response = client.get('/api/rates')
    assert response.status_code == 200
    assert json.loads(response.content) == test_data.get_payload()

@pytest.mark.asyncio
async def test_get_price(client):
    test_data = JSONTest()
    price = 100
    await RatePoster(test_data.get_payload()).post()
    response = client.get(f'/api/shipment?price={price}&date={test_data.date_1}&cargo_type={test_data.cargo_type_1}')
    assert response.status_code == 200
    content = json.loads(response.content)
    assert content['price'] == price * float(test_data.rate_1)

@pytest.mark.asyncio
async def test_get_price_different_date(client):
    test_data = JSONTest()
    price = 100
    await RatePoster(test_data.get_payload()).post()
    response = client.get(f'/api/shipment?price={price}&date=2020-07-03&cargo_type={test_data.cargo_type_1}')
    assert response.status_code == 200
    content = json.loads(response.content)
    assert content['price'] == price * float(test_data.rate_3)

@pytest.mark.asyncio
async def test_get_price_wrong_cargo_type(client):
    test_data = JSONTest()
    price = 100
    await RatePoster(test_data.get_payload()).post()
    response = client.get(f'/api/shipment?price={price}&date={test_data.date_1}&cargo_type=wrong_cargo_type')
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_price_wrong_date(client):
    test_data = JSONTest()
    price = 100
    await RatePoster(test_data.get_payload()).post()
    response = client.get(f'/api/shipment?price={price}&date=1453-05-29&cargo_type=wrong_cargo_type')
    assert response.status_code == 404
