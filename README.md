# Weather App

Веб-приложение для получения информации о погоде в любом городе мира. Использует Open-Meteo API для получения данных о погоде и геокодировании.

## Функции

- 🌍 Поиск погоды по названию города
- 📋 История поиска для каждого пользователя
- 🔥 Статистика популярных городов
- 🎯 Сессии пользователей с помощью cookies
- 📱 Адаптивный дизайн для мобильных устройств

## Технологии

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: HTML, CSS, Bootstrap, Jinja2
- **API**: Open-Meteo (геокодирование и погода)
- **Тестирование**: pytest
- **Контейнеризация**: Docker, Docker Compose

## Установка и запуск
                                 Oткройте терминал:

### Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Ixollozi/weather-app
cd weather-app
```

2. Создайте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  
.venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` (см. пример в `.env`):
```bash
cp .env.example .env
```

5. Запустите приложение:
```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: http://localhost:8000

### Запуск с Docker

1. Соберите и запустите контейнер:
```bash
docker-compose up --build
```

2. Приложение будет доступно по адресу: http://localhost:8000

## Структура проекта

```
weather-app/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI приложение и маршруты
│   ├── database.py       # Настройка базы данных
│   ├── models.py         # SQLAlchemy модели
│   ├── services.py       # Внешние API сервисы
│   ├── static/   
│   │   └── style.css     # CSS стили
│   └── templates/
│       └── home.html     # Jinja2 шаблон
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # Конфигурация тестов
│   └── test_app.py       # Тесты приложения
├── .env                  # Переменные окружения
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## API Endpoints

### GET /
Главная страница приложения

### POST /api/weather
Получение погоды по названию города

**Параметры:**
- `city` (form-data): Название города

**Ответ:**
```json
{
  "weather_data": {
    "city": "Moscow",
    "temperature": 15.2
  }
}
```

## База данных

Приложение использует SQLite базу данных с таблицей `search_history`:


## Тестирование

Запуск всех тестов:
```bash
pytest
```


Тесты включают:
- Тестирование API endpoints
- Тестирование моделей базы данных
- Тестирование внешних API сервисов
- Интеграционные тесты

## Развертывание

### Переменные окружения

Создайте файл `.env` со следующими переменными:

```env
DATABASE_URL=sqlite:///./weather.db
DEBUG=False
SESSION_SECRET_KEY=ващ ключ
```

### Docker в продакшене

1. Измените `docker-compose.yml` для продакшена:
```yaml
environment:
  - DATABASE_URL=sqlite:///./data/weather.db
  - DEBUG=False
  - SESSION_SECRET_KEY=ваш ключ
```

2. Запустите:
```bash
docker-compose -f docker-compose.yml up -d
```

## Мониторинг

Логи приложения доступны через:
```bash
docker-compose logs -f weather-app
```

## Спасибо за внимание!