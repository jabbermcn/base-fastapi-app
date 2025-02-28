from src.exceptions.base import BaseError


__all__ = ["ProjectInternalServerError"]


class ProjectInternalServerError(BaseError):
    detail = "project_internal_error"
