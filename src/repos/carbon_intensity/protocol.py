import datetime as dt
from enum import StrEnum
from pathlib import Path
from typing import Protocol, Self

from httpx import URL

from src.repos.carbon_intensity.co2_signal import CO2SignalCarbonIntensityRepo
from src.repos.carbon_intensity.file import FromFileCarbonIntensityRepo
from src.repos.carbon_intensity.national_grid_eso import (
    NationalGridESOCarbonIntensityApiRepo,
)


class CurrentCarbonIntensityRepo(Protocol):
    async def get_carbon_intensity(self) -> int: ...


class CurrentIntensityDataSource(StrEnum):
    FILE = "file"
    NATIONAL_GRID_ESO_CARBON_INTENSITY = "national-grid-eso-carbon-intensity"
    CO2_SIGNAL = "co2-signal"


class ForecastLowIntensityDateRepo(Protocol):
    async def get_best_time_to_run_within_period(
        self, within: dt.timedelta
    ) -> dt.datetime: ...


class ForecastLowIntensityDateDataSource(StrEnum):
    FILE = "file"
    NATIONAL_GRID_ESO_CARBON_INTENSITY = "national-grid-eso-carbon-intensity"


class MissingParameterError(ValueError):
    @classmethod
    def from_missing_country_code(cls) -> Self:
        return cls("No country code provided to CO2 Signal Api.")

    @classmethod
    def from_missing_api_key(cls) -> Self:
        return cls("No API key found for CO2 Signal API.")


def make_current_intensity_repo(
    co2_signal_api_key: str | None,
    co2_signal_carbon_intensity_api_base_url: URL,
    co2_signal_country_code: str | None,
    data_source: CurrentIntensityDataSource,
    from_file_carbon_intensity_file_path: Path,
    national_grid_eso_carbon_intensity_api_base_url: URL,
) -> CurrentCarbonIntensityRepo:
    intensity_repo: CurrentCarbonIntensityRepo = FromFileCarbonIntensityRepo(
        from_file_carbon_intensity_file_path
    )
    match data_source:
        case CurrentIntensityDataSource.FILE:
            intensity_repo = intensity_repo
        case CurrentIntensityDataSource.NATIONAL_GRID_ESO_CARBON_INTENSITY:
            intensity_repo = NationalGridESOCarbonIntensityApiRepo(
                base_url=national_grid_eso_carbon_intensity_api_base_url
            )
        case CurrentIntensityDataSource.CO2_SIGNAL:
            if not co2_signal_country_code:
                raise MissingParameterError.from_missing_country_code()

            if not co2_signal_api_key:
                raise MissingParameterError.from_missing_api_key()

            intensity_repo = CO2SignalCarbonIntensityRepo(
                base_url=co2_signal_carbon_intensity_api_base_url,
                api_key=co2_signal_api_key,
                country_code=co2_signal_country_code,
            )
    return intensity_repo


def make_forecast_low_intensity_date_repo(
    data_source: ForecastLowIntensityDateDataSource,
    from_file_carbon_intensity_file_path: Path,
    national_grid_eso_carbon_intensity_api_base_url: URL,
) -> ForecastLowIntensityDateRepo:
    intensity_repo: ForecastLowIntensityDateRepo = FromFileCarbonIntensityRepo(
        from_file_carbon_intensity_file_path
    )
    match data_source:
        case ForecastLowIntensityDateDataSource.FILE:
            intensity_repo = intensity_repo
        case ForecastLowIntensityDateDataSource.NATIONAL_GRID_ESO_CARBON_INTENSITY:
            intensity_repo = NationalGridESOCarbonIntensityApiRepo(
                base_url=national_grid_eso_carbon_intensity_api_base_url
            )
    return intensity_repo
