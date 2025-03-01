from collections.abc import Callable
from functools import wraps
from logging import getLogger


__all__ = ["ExceptionHandlerFactory"]


logger = getLogger(__name__)


ExceptionClass = type[Exception]


class ExceptionHandlerFactory:
    """
    A factory for creating exception handler decorators. It maps exceptions to custom exceptions
    and applies the mapping during function execution.

    :param exc_mapping: A dictionary where keys are source exception types and values are custom exception types or instances.
    :type exc_mapping: dict[ExceptionClass, ExceptionClass | Exception]
    :param default_exc: The default exception type to raise if no mapping is found.
    :type default_exc: ExceptionClass | Exception
    """

    def __init__(
        self,
        exc_mapping: dict[ExceptionClass, ExceptionClass | Exception],
        default_exc: ExceptionClass | Exception,
    ) -> None:
        self.exc_mapping = exc_mapping
        self.default_exc = default_exc

    def __call__(self, exc_override: dict[ExceptionClass, ExceptionClass | Exception] | None = None) -> Callable:
        """
        Creates a decorator that applies the exception-to-custom-exception mapping.

        :param exc_override: An optional dictionary to override the default exception mappings.
        :type exc_override: dict[ExceptionClass, ExceptionClass | Exception], optional
        :return: A decorator that wraps the target function.
        :rtype: Callable
        """

        if exc_override is None:
            exc_override = {}

        exceptions = self.exc_mapping | exc_override

        def wrapper(func: Callable) -> Callable:
            """
            Wraps the target function to handle exceptions and raise custom exceptions.

            :param func: The target function to be wrapped.
            :type func: Callable
            :return: The wrapped asynchronous function.
            :rtype: Callable
            """

            @wraps(wrapped=func)
            async def wrapped(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Exception handling {func.__qualname__}: {e}")
                    exc_or_instance = exceptions.get(e.__class__, self.default_exc)
                    if isinstance(exc_or_instance, type) and issubclass(exc_or_instance, Exception):
                        raise exc_or_instance()
                    raise exc_or_instance

            return wrapped

        return wrapper
