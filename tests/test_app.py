import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import SearchHistory

# Настройка тестовой БД
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@patch('app.main.templates')
def test_home_page_loads(mock_templates):
    """Тест загрузки главной страницы"""
    mock_templates.TemplateResponse.return_value.status_code = 200
    response = client.get("/")
    assert response.status_code == 200


@patch('app.main.geocod', new_callable=AsyncMock)
@patch('app.main.weather', new_callable=AsyncMock)
@patch('app.main.add_to_history', new_callable=AsyncMock)
def test_weather_search_success(mock_history, mock_weather, mock_geocod):
    """Тест успешного поиска погоды"""
    mock_geocod.return_value = ("New York", 40.7128, -74.0060, "US")
    mock_weather.return_value = 22.5
    mock_history.return_value = None

    response = client.post("/api/weather", data={"city": "New York"})

    assert response.status_code == 200
    mock_geocod.assert_called_once_with("New York")
    mock_weather.assert_called_once_with(40.7128, -74.0060)


@patch('app.main.geocod', new_callable=AsyncMock)
def test_weather_search_city_not_found(mock_geocod):
    """Тест поиска несуществующего города"""
    mock_geocod.side_effect = Exception("City not found")

    response = client.post("/api/weather", data={"city": "InvalidCity"})
    assert response.status_code == 200


def test_weather_search_empty_city():
    """Тест поиска с пустым названием города"""
    response = client.post("/api/weather", data={"city": ""})
    assert response.status_code == 422


def test_search_history_model():
    """Тест модели истории поиска"""
    db = TestingSessionLocal()

    history = SearchHistory(
        session_id="test-session",
        city_name="Paris",
        country="FR",
        latitude=48.8566,
        longitude=2.3522
    )

    db.add(history)
    db.commit()

    saved = db.query(SearchHistory).filter_by(session_id="test-session").first()
    assert saved.city_name == "Paris"
    assert saved.country == "FR"

    db.close()





def test_session_id_generation():
    """Тест генерации ID сессии"""
    from app.main import get_session_id
    from unittest.mock import Mock

    # Тест без cookie
    request = Mock()
    request.cookies.get.return_value = None

    session_id = get_session_id(request)
    assert session_id is not None
    assert len(session_id) > 10

    # Тест с существующим cookie
    request.cookies.get.return_value = "existing-session"
    session_id = get_session_id(request)
    assert session_id == "existing-session"