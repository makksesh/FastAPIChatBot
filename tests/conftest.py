import sys
import os

# Получаем путь к папке, где лежит этот файл (tests/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Получаем путь к родительской папке (FastAPIProject/)
parent_dir = os.path.dirname(current_dir)
# Добавляем родительскую папку в системные пути поиска Python
sys.path.insert(0, parent_dir)


import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from main import app
import db

# 1. Настраиваем тестовую БД
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"  # "sqlite+aiosqlite:///test.db"

# Переопределяем движок БД в модуле db
test_engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=False)
test_async_session = async_sessionmaker(bind=test_engine, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def override_db():
    """
    Эта фикстура автоматически подменяет engine и сессию в модуле db
    перед каждым тестом и создает чистые таблицы.
    """
    # Подмена глобальных переменных в твоем db.py
    # Это "грязный хак", но для текущей архитектуры (без DI) это самый простой путь
    original_engine = db.engine
    original_session = db.async_session

    db.engine = test_engine
    db.async_session = test_async_session

    # Создаем таблицы
    async with db.engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)

    yield

    # Чистим за собой (удаляем таблицы)
    async with db.engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.drop_all)

    # Возвращаем все как было (на всякий случай)
    db.engine = original_engine
    db.async_session = original_session


@pytest_asyncio.fixture
async def client():
    """Асинхронный клиент для запросов к API"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
