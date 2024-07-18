from fastapi import HTTPException
import requests


def get_city_coordinates(city: str):
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geocoding_response = requests.get(geocoding_url)
    if geocoding_response.status_code != 200:
        raise HTTPException(status_code=geocoding_response.status_code, detail="Ошибка при получении координат города")
    
    geocoding_data = geocoding_response.json()
    if not geocoding_data.get("results"):
        raise HTTPException(status_code=404, detail="Город не найден")
    
    latitude = geocoding_data["results"][0]["latitude"]
    longitude = geocoding_data["results"][0]["longitude"]
    return latitude, longitude


def get_weather_forecast(latitude: float, longitude: float):
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"
    weather_response = requests.get(weather_url)
    if weather_response.status_code != 200:
        raise HTTPException(status_code=weather_response.status_code, detail="Ошибка при получении прогноза погоды")
    return weather_response.json()
