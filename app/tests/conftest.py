import asyncio
import json
import pytest
from sqlalchemy import insert
from app.database import Base, async_session_maker, engine
from app.config import settings
from app.weather.models import Users
from httpx import AsyncClient
from main import app as fastapi_app


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding='utf-8') as file:
            return json.load(file)
    
    users = open_mock_json('users')

    async with async_session_maker() as session:
        add_users = insert(Users).values(users)
        await session.execute(add_users)
        await session.commit()


# Из документации
@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        yield ac
