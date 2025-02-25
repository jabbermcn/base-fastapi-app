from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from settings import settings


async_engine = create_async_engine(settings.DATABASE.DSN.unicode_string())
async_session_maker = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
