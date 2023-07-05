import datetime as dt
from enum import StrEnum
from pathlib import Path
from typing import Protocol

import typer
from httpx import URL, AsyncClient
from pydantic import BaseModel, field_validator

from src.auth.co2_signal import CO2SignalAuthClient


class CarbonIntensityRepo(Protocol):
    async def get_carbon_intensity(self) -> int:
        ...

    async def get_best_time_to_run_within_period(self, within: dt.timedelta) -> dt.datetime:
        ...


class InMemoryCarbonIntensityRepo(object):
    def __init__(self, carbon_intensity: list[tuple[dt.datetime, int]]) -> None:
        self._carbon_intensity = carbon_intensity

    async def get_carbon_intensity(self) -> int:
        intensity = self._carbon_intensity
        utcnow = dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)

        intensity_in_present = filter(lambda x: x[0] <= utcnow, intensity)
        max_date = max(intensity_in_present, key=lambda x: x[0])

        return max_date[1]

    async def get_best_time_to_run_within_period(self, within: dt.timedelta) -> dt.datetime:

        intensity = self._carbon_intensity
        utcnow = dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)

        intensity_in_future = filter(lambda x: x[0] > utcnow, intensity)
        intensity_within_duratation = filter(lambda x: (x[0]-utcnow) <= within, intensity_in_future)
        cleanest_time = min(intensity_within_duratation, key=lambda x: x[1])

        return cleanest_time[0]


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

    async def get_carbon_intensity(self) -> int:
        response = await self._client.get(
            "/v1/latest", params={"countryCode": self._country_code}
        )
        response.raise_for_status()

        parsed_response = CO2SignalCarbonIntensityResponse.model_validate_json(
            response.content
        )

        return parsed_response.data.carbonIntensity


class DataSource(StrEnum):
    FILE = "file"
    NATIONAL_GRID_ESO_CARBON_INTENSITY = "national-grid-eso-carbon-intensity"
    CO2_SIGNAL = "co2-signal"


def make_intensity_repo(co2_signal_api_key, co2_signal_carbon_intensity_api_base_url, co2_signal_country_code,
                        data_source, from_file_carbon_intensity_file_path,
                        national_grid_eso_carbon_intensity_api_base_url):
    intensity_repo: CarbonIntensityRepo = FromFileCarbonIntensityRepo(
        from_file_carbon_intensity_file_path
    )
    match data_source:
        case DataSource.FILE:
            intensity_repo = intensity_repo
        case DataSource.NATIONAL_GRID_ESO_CARBON_INTENSITY:
            intensity_repo = NationalGridESOCarbonIntensityApiRepo(
                base_url=national_grid_eso_carbon_intensity_api_base_url
            )
        case DataSource.CO2_SIGNAL:
            if not co2_signal_country_code:
                typer.echo("No country code provided to CO2 Signal Api.")
                raise typer.Exit(1)

            if not co2_signal_api_key:
                typer.echo("No API key found for CO2 Signal API.")
                raise typer.Exit(1)

            intensity_repo = CO2SignalCarbonIntensityRepo(
                base_url=co2_signal_carbon_intensity_api_base_url,
                api_key=co2_signal_api_key,
                country_code=co2_signal_country_code,
            )
    return intensity_repo
