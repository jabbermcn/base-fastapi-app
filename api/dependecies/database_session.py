from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection import async_session_maker


__all__ = ["DBSession"]


async def _create_database_session() -> AsyncSession:
    async with async_session_maker() as session:  # type: AsyncSession
        yield session


DBSession = Annotated[AsyncSession, Depends(dependency=_create_database_session)]
