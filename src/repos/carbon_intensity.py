from pathlib import Path
from typing import Generator, Protocol

import httpx
from httpx import URL, AsyncClient, Request
from pydantic import BaseModel, field_validator


class CarbonIntensityRepo(Protocol):
    async def get_carbon_intensity(self) -> int:
        ...


class InMemoryCarbonIntensityRepo(object):
    def __init__(self, carbon_intensity: int) -> None:
        self._carbon_intensity = carbon_intensity

    async def get_carbon_intensity(self) -> int:
        return self._carbon_intensity


class FromFileCarbonIntensityRepo(object):
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    async def get_carbon_intensity(self) -> int:
        return int(self._file_path.read_text(encoding="utf8"))


class NationalGridESOCarbonIntensityIntensity(BaseModel):
    actual: int


class NationalGridESOCarbonIntensityData(BaseModel):
    intensity: NationalGridESOCarbonIntensityIntensity


class NationalGridESOCarbonIntensityResponse(BaseModel):
    data: list[NationalGridESOCarbonIntensityData]

    @field_validator("data")
    def ensure_data_is_not_empty(
        cls, v: list[NationalGridESOCarbonIntensityData]
    ) -> list[NationalGridESOCarbonIntensityData]:
        if not v:
            raise ValueError("data is empty")

        return v


class CO2SignalCarbonIntensityData(BaseModel):
    carbonIntensity: int


class CO2SignalCarbonIntensityResponse(BaseModel):
    data: CO2SignalCarbonIntensityData


class NationalGridESOCarbonIntensityApiRepo:
    def __init__(self, base_url: URL):
        self._client = AsyncClient(base_url=base_url, http2=True)

    async def get_carbon_intensity(self) -> int:
        response = await self._client.get("/intensity")
        response.raise_for_status()

        parsed_response = NationalGridESOCarbonIntensityResponse.model_validate_json(
            response.content
        )

        return parsed_response.data[0].intensity.actual


class CO2SignalCarbonIntensityRepo:
    def __init__(self, base_url: URL, api_key: str, country_code: str):
        self._client = AsyncClient(
            base_url=base_url, http2=True, auth=CO2SignalAuthClient(api_key=api_key)
        )
        self._country_code = country_code

    async def get_carbon_intensity(self):
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

    def auth_flow(self, request: Request) -> Generator[Request, None, None]:
        request.headers["auth-token"] = self._api_key
        yield request
