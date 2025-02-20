import re

from sqlalchemy.orm import DeclarativeBase, declared_attr


__all__ = ["Base"]


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive  # noqa
    @classmethod
    def __tablename__(cls) -> str:
        snake = re.sub(
            r"([A-Z]+)([A-Z][a-z])",
            lambda m: f"{m.group(1)}_{m.group(2)}",
            cls.__name__,
        )
        snake = re.sub(r"([a-z])([A-Z])", lambda m: f"{m.group(1)}_{m.group(2)}", snake)
        snake = re.sub(r"([0-9])([A-Z])", lambda m: f"{m.group(1)}_{m.group(2)}", snake)
        snake = re.sub(r"([a-z])([0-9])", lambda m: f"{m.group(1)}_{m.group(2)}", snake)
        snake = snake.replace("-", "_")
        return snake.lower()
