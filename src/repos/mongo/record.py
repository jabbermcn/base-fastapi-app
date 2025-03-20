from src.database.mongo.models import Record
from src.repos.mongo.base import BaseMongoRepo


__all__ = ["RecordRepo"]


class RecordRepo(BaseMongoRepo[Record]):
    def __init__(self):
        super().__init__(Record)
