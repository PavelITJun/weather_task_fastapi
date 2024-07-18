from datetime import datetime, timedelta
from sqlalchemy import select
from app.weather.models import Users
from app.weather.services import *
from app.database import async_session_maker
from sqlalchemy.orm.attributes import flag_modified


class BaseDao:
    city = None
    request = None


    @classmethod
    async def get_weather_data_all(cls, city):
        latitude, longitude = get_city_coordinates(city)
        weather_data_all = get_weather_forecast(latitude, longitude)
        return weather_data_all


    @classmethod
    async def get_weather_data(cls, weather_data_all):
        dates = []
        current_time = datetime.now()
        for ind, el in enumerate(weather_data_all['hourly']['time']):
            if datetime.fromisoformat(el) >= current_time:
                first_date = datetime.fromisoformat(el)
                first_temp_ind = ind
                break

        temps = []
        for el in range(3):
            dates.append((first_date + timedelta(hours=el)).strftime("%d-%m-%Y %H:%M"))
            temps.append((weather_data_all['hourly']['temperature_2m'][first_temp_ind + el]))

        weather_data = list(zip(dates, temps))
        return weather_data


    @classmethod
    async def get_weather(cls, city, request):
        weather_data_all = await cls.get_weather_data_all(city)
        weather_data = await cls.get_weather_data(weather_data_all)
        client_ip = request.client.host
        async with async_session_maker() as db:
            # Поиск пользователя в базе данных по IP
            result = await db.execute(select(Users).filter(Users.IP == client_ip))
            user = result.scalars().first()

            if user:
                # Обновление истории запросов
                if city in user.history:
                    user.history[city] += 1
                else:
                    user.history[city] = 1
                user.last_query = city
                flag_modified(user, "history")
                db.merge(user)
            else:
                # Создание новой записи для пользователя
                user = Users(IP=client_ip, history={city: 1}, last_query=city)
                db.add(user)
            await db.commit()
            await db.refresh(user)

            return {"request": request, "weather_data": weather_data, 'last_query': city}
