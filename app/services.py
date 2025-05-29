import aiohttp
from datetime import datetime
from .database import get_db
from .models import SearchHistory

async def geocod(city):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=ru&format=json'
        )
        data = await response.json()
        result = data["results"][0]
        return result["name"], result["latitude"], result["longitude"], result["country"]

async def weather(lat, lon):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&forecast_days=1&timezone=auto'
        )
        data = await response.json()
        return data["hourly"]["temperature_2m"][0]

async def add_to_history(session_id, city, country, lat, lon):
    db = next(get_db())
    history = db.query(SearchHistory).filter_by(session_id=session_id, city_name=city).first()

    if history:
        history.search_count += 1
        history.updated_at = datetime.utcnow()
    else:
        new_entry = SearchHistory(
            session_id=session_id,
            city_name=city,
            country=country,
            latitude=lat,
            longitude=lon,
            search_count=1
        )
        db.add(new_entry)

    db.commit()
