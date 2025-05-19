import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

load_dotenv()

DEBUG = os.getenv("DEBUG") == "True"

if DEBUG:
    DATABASE_URL = os.getenv("DATABASE_DEBUG_URL")
else:
    DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
sync_engine = create_engine(DATABASE_URL.replace("+asyncpg", ""), future=True)
SessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
