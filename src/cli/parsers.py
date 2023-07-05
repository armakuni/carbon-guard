import datetime as dt
from typing import Self

from dateparser import parse
from httpx import URL


class ArgumentParserError(ValueError):
    @classmethod
    def from_invalid_duration(cls, given_duration: str) -> Self:
        return cls(f"Could not parse {given_duration} as a human readable duration")

    @classmethod
    def from_invalid_url(cls, url: str) -> Self:
        return cls(f"{url} is not a valid http or https URL")


def http_or_https_url(url: str) -> URL:
    u = URL(url)

    if u.scheme not in ("http", "https"):
        raise ArgumentParserError.from_invalid_url(url)

    return u


def human_readable_duration(given_duration: str) -> dt.timedelta:
    anchor_time = dt.datetime.now()

    time = parse(given_duration, settings={"RELATIVE_BASE": anchor_time})

    if time is None:
        raise ArgumentParserError.from_invalid_duration(given_duration)

    return anchor_time - time
