import asyncio
from typing import Callable, Coroutine, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def async_to_sync(f: Callable[P, Coroutine[None, None, R]]) -> Callable[P, R]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        return asyncio.run(f(*args, **kwargs))

    return inner
