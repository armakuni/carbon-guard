from enum import StrEnum
from pathlib import Path

from httpx import URL

from src.cli.async_helper import async_to_sync
from src.cli.parsers import parse_url

UK_CARBON_INTENSITY_API_BASE_URL: URL = URL("https://api.carbonintensity.org.uk")
FILE_FOR_INTENSITY_READING: str = ".carbon_intensity"

import typer
from typing_extensions import Annotated

from src.repos.carbon_intensity import (
    CarbonIntensityRepo,
    FromFileCarbonIntensityRepo,
    UkCarbonIntensityApiRepo,
)


class DataSource(StrEnum):
    FILE = "file"
    UK_CARBON_INTENSITY = "uk-carbon-intensity"


def main(
    max_carbon_intensity: Annotated[
        int,
        typer.Option(
            help="Set the max carbon intensity in gCO2eq/kWh.",
            envvar="MAX_CARBON_INTENSITY",
        ),
    ],
    data_source: Annotated[
        DataSource,
        typer.Option(
            case_sensitive=False,
            help="Where to read carbon intensity data from",
            envvar="REPOSITORY_MODE",
        ),
    ] = DataSource.UK_CARBON_INTENSITY,
    from_file_carbon_intensity_file_path: Annotated[
        Path,
        typer.Option(
            help="File to read carbon intensity from in file mode",
            envvar="FROM_FILE_CARBON_INTENSITY_FILE_PATH",
        ),
    ] = Path(FILE_FOR_INTENSITY_READING),
    uk_carbon_intensity_api_base_url: Annotated[
        URL,
        typer.Option(
            help="URL for the carbon intensity API",
            envvar="UK_CARBON_INTENSITY_API_BASE_URL",
            parser=parse_url,
        ),
    ] = UK_CARBON_INTENSITY_API_BASE_URL,
) -> None:
    carbon_intensity(
        data_source,
        from_file_carbon_intensity_file_path,
        max_carbon_intensity,
        uk_carbon_intensity_api_base_url,
    )


@async_to_sync
async def carbon_intensity(
    data_source: DataSource,
    from_file_carbon_intensity_file_path: Path,
    max_carbon_intensity: int,
    uk_carbon_intensity_api_base_url: URL,
) -> None:
    intensity_repo: CarbonIntensityRepo = FromFileCarbonIntensityRepo(
        from_file_carbon_intensity_file_path
    )
    match data_source:
        case DataSource.FILE:
            intensity_repo = intensity_repo
        case DataSource.UK_CARBON_INTENSITY:
            intensity_repo = UkCarbonIntensityApiRepo(
                base_url=uk_carbon_intensity_api_base_url
            )
    if await intensity_repo.get_carbon_intensity() > max_carbon_intensity:
        typer.echo("Carbon levels exceed threshold, skipping.")
        raise typer.Exit(1)
    typer.echo("Carbon levels under threshold, proceeding.")


def run() -> None:
    typer.run(main)
