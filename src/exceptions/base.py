class BaseError(Exception):
    detail: str = "something_went_wrong"

    def __str__(self) -> str:
        return self.detail
