import datetime as dt
from pathlib import Path
from typing import Optional

import typer
from httpx import URL
from typing_extensions import Annotated

from src.cli.command.check import run as check_run
from src.cli.command.schedule import run as schedule_run
from src.cli.parsers import http_or_https_url, human_readable_duration
from src.repos.carbon_intensity.protocol import (
    CurrentIntensityDataSource,
    ForecastLowIntensityDateDataSource,
    MissingParameterError,
    make_current_intensity_repo,
    make_forecast_low_intensity_date_repo,
)

NATIONAL_GRID_ESO_CARBON_INTENSITY_API_BASE_URL: URL = URL(
    "https://api.carbonintensity.org.uk"
)
CO2_SIGNAL_API_BASE_URL: URL = URL("https://api.co2signal.com")
FILE_FOR_INTENSITY_READING: str = ".carbon_intensity"

app = typer.Typer()


@app.command(help="Check the current carbon intensity.")
def check(
    max_carbon_intensity: Annotated[
        int,
        typer.Option(
            envvar="MAX_CARBON_INTENSITY",
            help="Set the max carbon intensity in gCO2eq/kWh.",
        ),
    ],
    advise_only: Annotated[
        bool,
        typer.Option(
            envvar="ADVISE_ONLY",
            help="Do not exit with an error if the carbon intensity is above the max carbon intensity.",
        ),
    ] = False,
    data_source: Annotated[
        CurrentIntensityDataSource,
        typer.Option(
            case_sensitive=False,
            envvar="DATA_SOURCE",
            help="Where to read carbon intensity data from",
        ),
    ] = CurrentIntensityDataSource.NATIONAL_GRID_ESO_CARBON_INTENSITY,
    from_file_carbon_intensity_file_path: Annotated[
        Path,
        typer.Option(
            envvar="FROM_FILE_CARBON_INTENSITY_FILE_PATH",
            help="File to read carbon intensity from in file mode",
        ),
    ] = Path(FILE_FOR_INTENSITY_READING),
    national_grid_eso_carbon_intensity_api_base_url: Annotated[
        URL,
        typer.Option(
            envvar="NATIONAL_GRID_ESO_CARBON_INTENSITY_API_BASE_URL",
            help="URL for the National Grid ESO Carbon Intensity API",
            parser=http_or_https_url,
        ),
    ] = NATIONAL_GRID_ESO_CARBON_INTENSITY_API_BASE_URL,
    co2_signal_carbon_intensity_api_base_url: Annotated[
        URL,
        typer.Option(
            envvar="CO2_SIGNAL_API_BASE_URL",
            help="URL for the CO2 Signal api",
            parser=http_or_https_url,
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
    try:
        intensity_repo = make_current_intensity_repo(
            co2_signal_api_key,
            co2_signal_carbon_intensity_api_base_url,
            co2_signal_country_code,
            data_source,
            from_file_carbon_intensity_file_path,
            national_grid_eso_carbon_intensity_api_base_url,
        )
    except MissingParameterError as e:
        typer.echo(f"{e}")
        raise typer.Exit(1) from e

    check_run(
        max_carbon_intensity,
        advise_only,
        intensity_repo,
    )


@app.command(help="Find the lowest carbon time.")
def schedule(
    within: Annotated[
        dt.timedelta,
        typer.Option(
            envvar="WITHIN",
            help="Time period to predict the lowest intensity within",  #
            parser=human_readable_duration,
        ),
    ],
    data_source: Annotated[
        ForecastLowIntensityDateDataSource,
        typer.Option(
            case_sensitive=False,
            envvar="DATA_SOURCE",
            help="Where to read carbon intensity data from",
        ),
    ] = ForecastLowIntensityDateDataSource.NATIONAL_GRID_ESO_CARBON_INTENSITY,
    from_file_carbon_intensity_file_path: Annotated[
        Path,
        typer.Option(
            envvar="FROM_FILE_CARBON_INTENSITY_FILE_PATH",
            help="File to read carbon intensity from in file mode",
        ),
    ] = Path(FILE_FOR_INTENSITY_READING),
    national_grid_eso_carbon_intensity_api_base_url: Annotated[
        URL,
        typer.Option(
            envvar="NATIONAL_GRID_ESO_CARBON_INTENSITY_API_BASE_URL",
            help="URL for the National Grid ESO Carbon Intensity API",
            parser=http_or_https_url,
        ),
    ] = NATIONAL_GRID_ESO_CARBON_INTENSITY_API_BASE_URL,
) -> None:
    intensity_repo = make_forecast_low_intensity_date_repo(
        data_source,
        from_file_carbon_intensity_file_path,
        national_grid_eso_carbon_intensity_api_base_url,
    )
    schedule_run(
        within,
        intensity_repo,
    )


def run() -> None:
    app()


if __name__ == "__main__":
    run()
