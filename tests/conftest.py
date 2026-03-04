import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from app.database import Base, get_session

AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

DATABASE_URL = "sqlite+aiosqlite://./test.db"

test_engine = create_async_engine(DATABASE_URL)
session = async_sessionmaker(test_engine, expire_on_commit=False)


