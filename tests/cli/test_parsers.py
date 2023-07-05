import datetime as dt

import pytest
from httpx import URL

from src.cli.parsers import http_or_https_url, human_readable_duration


class TestHttpOrHttpsUrl:
    def test_parsing_http_url(self) -> None:
        assert http_or_https_url("http://example.com") == URL("http://example.com")

    def test_raises_an_exception_on_garbage(self) -> None:
        with pytest.raises(ValueError):
            http_or_https_url("dfgbsdtfhznfghzjmn fdghjndgthzndgtfhzn")


class TestHumanReadableDuration:
    @pytest.mark.freeze_time
    def test_parsing_duration(self) -> None:
        utcnow = dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)
        actual = human_readable_duration("2 weeks")

        assert utcnow + actual == utcnow + dt.timedelta(days=14)

    def test_raises_an_exception_on_garbage(self) -> None:
        with pytest.raises(ValueError):
            human_readable_duration("dfgbsdtfhznfghzjmn fdghjndgthzndgtfhzn")
