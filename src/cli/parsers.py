from httpx import URL


def url(url: str) -> URL:
    return URL(url)
