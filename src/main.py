from enum import StrEnum
from pathlib import Path
from typing import Optional

import typer
from httpx import URL
from typing_extensions import Annotated

from src.cli.async_helper import async_to_sync
from src.cli.parsers import parse_url
from src.repos.carbon_intensity import (
    CarbonIntensityRepo,
    CO2SignalCarbonIntensityRepo,
    FromFileCarbonIntensityRepo,
    NationalGridESOCarbonIntensityApiRepo,
)

NATIONAL_GRID_ESO_CARBON_INTENSITY_API_BASE_URL: URL = URL(
    "https://api.carbonintensity.org.uk"
)
CO2_SIGNAL_API_BASE_URL: URL = URL("https://api.co2signal.com")
FILE_FOR_INTENSITY_READING: str = ".carbon_intensity"


class DataSource(StrEnum):
    FILE = "file"
    NATIONAL_GRID_ESO_CARBON_INTENSITY = "national-grid-eso-carbon-intensity"
    CO2_SIGNAL = "co2-signal"


def main(
    max_carbon_intensity: Annotated[
        int,
        typer.Option(
            envvar="MAX_CARBON_INTENSITY",
            help="Set the max carbon intensity in gCO2eq/kWh.",
        ),
    ],
    data_source: Annotated[
        DataSource,
        typer.Option(
            case_sensitive=False,
            envvar="DATA_SOURCE",
            help="Where to read carbon intensity data from",
        ),
    ] = DataSource.NATIONAL_GRID_ESO_CARBON_INTENSITY,
    from_file_carbon_intensity_file_path: Annotated[
        Path,
        typer.Option(
            envvar="FROM_FILE_CARBON_INTENSITY_FILE_PATH",
            help="File to read carbon intensity from in file mode",
        ),
    ] = Path(FILE_FOR_INTENSITY_READING),
    nation_grid_eso_carbon_intensity_api_base_url: Annotated[
        URL,
        typer.Option(
            envvar="NATIONAL_GRID_ESO_CARBON_INTENSITY_API_BASE_URL",
            help="URL for the National Grid ESO Carbon Intensity API",
            parser=parse_url,
        ),
    ] = NATIONAL_GRID_ESO_CARBON_INTENSITY_API_BASE_URL,
    co2_signal_carbon_intensity_api_base_url: Annotated[
        URL,
        typer.Option(
            envvar="CO2_SIGNAL_API_BASE_URL",
            help="URL for the CO2 Signal api",
            parser=parse_url,
        ),
    ] = CO2_SIGNAL_API_BASE_URL,
    co2_signal_api_key: Annotated[
        Optional[str],
        typer.Option(
            envvar="CO2_SIGNAL_API_KEY",
            help="Api key for the CO2 Signal api, required in CO2 Signal mode",
        ),
    ] = None,
    co2_signal_country_code: Annotated[
        Optional[str],
        typer.Option(
            envvar="CO2_SIGNAL_COUNTRY_CODE",
            help="Country code to get the carbon intensity from CO2 Signal api",
        ),
    ] = None,
) -> None:
    carbon_intensity(
        data_source,
        from_file_carbon_intensity_file_path,
        max_carbon_intensity,
        nation_grid_eso_carbon_intensity_api_base_url,
        co2_signal_carbon_intensity_api_base_url,
        co2_signal_api_key,
        co2_signal_country_code,
    )


@async_to_sync
async def carbon_intensity(
    data_source: DataSource,
    from_file_carbon_intensity_file_path: Path,
    max_carbon_intensity: int,
    national_grid_eso_carbon_intensity_api_base_url: URL,
    co2_signal_carbon_intensity_api_base_url: URL,
    co2_signal_api_key: Optional[str],
    co2_signal_country_code: Optional[str],
) -> None:
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
    if await intensity_repo.get_carbon_intensity() > max_carbon_intensity:
        typer.echo("Carbon levels exceed threshold, skipping.")
        raise typer.Exit(1)
    typer.echo("Carbon levels under threshold, proceeding.")


def run() -> None:
    typer.run(main)
