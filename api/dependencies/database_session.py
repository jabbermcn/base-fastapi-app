from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import db_connection


__all__ = ["DBSession"]


DBSession = Annotated[AsyncSession, Depends(dependency=db_connection.get_session)]
