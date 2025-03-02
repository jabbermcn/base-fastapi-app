from settings import settings
from src.database.connection import DatabaseConnection


__all__ = ["db_connection"]

db_connection = DatabaseConnection(settings.DATABASE.DSN.unicode_string())
