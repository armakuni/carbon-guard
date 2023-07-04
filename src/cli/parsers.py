from httpx import URL


def parse_url(url: str) -> URL:
    return URL(url)
