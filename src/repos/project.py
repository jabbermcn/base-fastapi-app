from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy.models import Project
from src.repos.base import BaseRepo


__all__ = ["ProjectRepo"]


class ProjectRepo(BaseRepo[Project]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Project)
