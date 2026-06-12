import functools
from collections.abc import Callable

from fastapi import HTTPException


def value_error_to_http(status_code: int) -> Callable:
    """Decorator that converts ``ValueError`` into an ``HTTPException``."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ValueError as e:
                raise HTTPException(status_code=status_code, detail=str(e))

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                raise HTTPException(status_code=status_code, detail=str(e))

        import asyncio

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
