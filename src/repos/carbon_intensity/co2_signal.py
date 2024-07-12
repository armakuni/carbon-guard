from typing import Generator

import httpx
from httpx import URL, AsyncClient, Request, Response, Timeout
from pydantic import BaseModel


class CO2SignalCarbonIntensityData(BaseModel):
    carbonIntensity: int


class CO2SignalCarbonIntensityResponse(BaseModel):
    data: CO2SignalCarbonIntensityData


class CO2SignalCarbonIntensityRepo:
    def __init__(self, base_url: URL, api_key: str, country_code: str):
        self._client = AsyncClient(
            base_url=base_url,
            http2=True,
            auth=CO2SignalAuthClient(api_key=api_key),
            timeout=Timeout(5.0),
        )
        self._country_code = country_code

    async def get_carbon_intensity(self) -> int:
        response = await self._client.get(
            "/v1/latest", params={"countryCode": self._country_code}
        )
        response.raise_for_status()

        parsed_response = CO2SignalCarbonIntensityResponse.model_validate_json(
            response.content
        )

        return parsed_response.data.carbonIntensity


class CO2SignalAuthClient(httpx.Auth):
    def __init__(self, api_key: str):
        self._api_key = api_key

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        request.headers["auth-token"] = self._api_key
        yield request
