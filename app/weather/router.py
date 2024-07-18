from typing import Dict
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.database import async_session_maker
from sqlalchemy import select
from app.weather.models import Cities, Users
from app.dao.base import *


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/weather", response_class=HTMLResponse)
async def get_weather(request: Request, city: str = Form(...)):
    return templates.TemplateResponse("weather.html", await BaseDao.get_weather(city, request))


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    async with async_session_maker() as db:
        client_ip = request.client.host
        result = await db.execute(select(Users).filter(Users.IP == client_ip))
        user = result.scalars().first()
        city = user.last_query if user else None
    return templates.TemplateResponse("weather.html", {"request": request, "weather_data": None, 'last_query': city})

# Этот эндпоинт необходимо сделать доступным только для админов, но это ненастоящий проект, так что пусть будет так)
@router.get('/get_history/{id}', response_model=Dict)
async def get_history_by_id(request: Request, id: int):
    async with async_session_maker() as db:
        result = await db.execute(select(Users).filter(id==id))
    user = result.scalars().first()
    return user.history


@router.post("/weather_last", response_class=HTMLResponse)
async def get_weather_last(request: Request, last_query: str = Form(...)):
    return templates.TemplateResponse("weather.html", await BaseDao.get_weather(last_query, request))


@router.get("/autocomplete")
async def autocomplete(term: str):
    async with async_session_maker() as session:
        result = await session.execute(
            select(Cities.city).where(Cities.city.ilike(f'{term}%')).limit(3)
        )
        cities = result.scalars().all()
    return JSONResponse(cities)
