import uuid
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import func

from .database import create_tables, get_db
from .services import geocod, weather, add_to_history
from .models import SearchHistory

app = FastAPI(title="Weather App")

base = os.path.dirname(os.path.abspath(__file__))
static = os.path.join(base, "static")
template = os.path.join(base, "templates")

app.mount("/static", StaticFiles(directory=static), name="static")
templates = Jinja2Templates(directory=template)

create_tables()


def get_session_id(request: Request) -> str:
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id


def get_history_and_popular(session_id: str):
    db = next(get_db())
    history = db.query(SearchHistory).filter_by(session_id=session_id).order_by(
        SearchHistory.updated_at.desc()).limit(5).all()

    popular = db.query(
        SearchHistory.city_name,
        func.sum(SearchHistory.search_count).label('total_searches')
    ).group_by(SearchHistory.city_name).order_by(
        func.sum(SearchHistory.search_count).desc()
    ).limit(5).all()

    return history, popular


def set_response_cookie(response, request, session_id):
    if not request.cookies.get("session_id"):
        response.set_cookie("session_id", session_id, max_age=86400 * 30)
    return response


@app.get("/")
async def home(request: Request):
    session_id = get_session_id(request)
    history, popular = get_history_and_popular(session_id)

    response = templates.TemplateResponse("home.html", {
        "request": request,
        "history": history,
        "popular": popular
    })

    return set_response_cookie(response, request, session_id)


@app.post("/api/weather")
async def search(request: Request, city: str = Form(...)):
    session_id = get_session_id(request)
    template_data = {"request": request}

    try:
        city_name, latitude, longitude, country = await geocod(city)
        temp = await weather(latitude, longitude)
        weather_data = {"city": city_name, "temperature": temp}

        print(f"🌍 Город: {city_name}")
        print(f"🌡️ Температура: {temp}°C")

        await add_to_history(session_id, city_name, country, latitude, longitude)
        template_data["weather_data"] = weather_data

    except Exception as e:
        print(f"Ошибка: {e}")
        template_data["error"] = str(e)

    history, popular = get_history_and_popular(session_id)
    template_data.update({"history": history, "popular": popular})

    response = templates.TemplateResponse("home.html", template_data)
    return set_response_cookie(response, request, session_id)