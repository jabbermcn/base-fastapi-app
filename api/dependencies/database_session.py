from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import alchemy_db_connection


__all__ = ["DBSession"]

DBSession = Annotated[AsyncSession, Depends(dependency=alchemy_db_connection.get_session)]
