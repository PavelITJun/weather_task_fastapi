from fastapi import FastAPI
import uvicorn
from app.weather.router import router as weather_router

app = FastAPI()
app.include_router(weather_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
