from typing import Generator

import httpx
from httpx import Request, Response


class CO2SignalAuthClient(httpx.Auth):
    def __init__(self, api_key: str):
        self._api_key = api_key

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        request.headers["auth-token"] = self._api_key
        yield request
