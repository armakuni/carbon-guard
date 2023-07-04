from typing import ParamSpec, TypeVar

from src.cli.async_helper import async_to_sync

P = ParamSpec("P")
R = TypeVar("R")


def test_can_run_async_code_with_annotations() -> None:
    @async_to_sync
    async def async_func() -> str:
        return "hello"

    result = async_func()

    assert result == "hello"
