from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("DB_URL")
async_db_url = os.getenv("ASYNC_DB_URL")

engine = create_engine(db_url, echo=True)
SessionLocal = sessionmaker(bind=engine)


async_engine = create_async_engine(async_db_url, echo=True)
AsyncSessionLocal = sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession)



def init_db():
    SQLModel.metadata.create_all(engine)


async def async_init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)