from httpx import AsyncClient


async def test_get_weather(ac: AsyncClient):
    response = await ac.post('/weather', data={"city": "Moscow"})
    assert response.status_code == 200


async def test_read_root(ac: AsyncClient):
    response = await ac.get('/')
    assert response.status_code == 200


async def test_get_history_by_id(ac: AsyncClient):
    response = await ac.get('/get_history/1', params={"id": 1})
    assert response.status_code == 200


async def test_get_weather_last(ac: AsyncClient):
    response = await ac.post('/weather_last', data={"city": "Moscow"})
    assert response.status_code == 200
    