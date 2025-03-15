from collections.abc import AsyncGenerator
from uuid import uuid4

from pydantic_core import MultiHostUrl
from sqlalchemy import URL, NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class AlchemyDBConnection:
    def __init__(self, dsn: MultiHostUrl | URL | str):
        self._dsn = dsn
        self.engine = create_async_engine(
            url=self._dsn,
            pool_recycle=0,
            poolclass=NullPool,
            query_cache_size=0,
            connect_args={
                "prepared_statement_name_func": lambda: f"__asyncpg_{uuid4()}__",
                "statement_cache_size": 0,
                "prepared_statement_cache_size": 0,
                "command_timeout": 30,
            },
            execution_options={"isolation_level": "READ COMMITTED"},
        )
        self.session_maker = async_sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)

    async def get_session(self) -> AsyncGenerator:
        async with self.session_maker() as session:  # type: AsyncSession
            yield session

    async def close(self):
        await self.engine.dispose()
