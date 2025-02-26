from typing import Generic, TypeVar

from pydantic import Field

from src.types.base import ImmutableDTO


__all__ = ["Paginator", "Pagination"]


Schema = TypeVar("Schema", bound=ImmutableDTO)


class Pagination(ImmutableDTO):
    page: int = Field(..., ge=1, description="The current page number")
    page_count: int = Field(..., ge=1, description="The total number of pages in the selection")
    page_size: int = Field(..., ge=1, description="The number of items per page")


class Paginator(ImmutableDTO, Generic[Schema]):
    results: list[Schema]
    pagination: Pagination
