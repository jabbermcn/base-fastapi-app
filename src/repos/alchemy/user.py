from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy.models import User
from src.repos.alchemy.base import BaseRepo


__all__ = ["UserRepo"]


class UserRepo(BaseRepo[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=User)
