from pydantic import BaseModel


class SWeatherRequest(BaseModel):
    city: str