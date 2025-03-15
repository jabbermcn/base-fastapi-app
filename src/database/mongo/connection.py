from collections.abc import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class MongoDBConnection:
    def __init__(self, dsn: str, database_name: str):
        self._dsn = dsn
        self._database_name = database_name
        self._client = AsyncIOMotorClient(self._dsn)
        self._db = self._client[self._database_name]

    @property
    def database(self) -> AsyncIOMotorDatabase:
        return self._db

    async def get_database(self) -> AsyncGenerator[AsyncIOMotorDatabase, None]:
        yield self._db

    async def close(self):
        self._client.close()
