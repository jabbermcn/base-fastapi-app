from settings import settings
from src.database.alchemy.connection import AlchemyDBConnection
from src.database.mongo.connection import MongoDBConnection


__all__ = ["alchemy_db_connection", "mongo_db_connection"]

alchemy_db_connection = AlchemyDBConnection(settings.DATABASE.POSTGRES_DSN.unicode_string())

mongo_db_connection = MongoDBConnection(
    dsn=settings.DATABASE.MONGO_DSN.unicode_string(), database_name=settings.DATABASE.MONGO_DATABASE_NAME
)
