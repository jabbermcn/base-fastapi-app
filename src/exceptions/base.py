class BaseError(Exception):
    details: str = "something_went_wrong"

    def __str__(self) -> str:
        return self.details
