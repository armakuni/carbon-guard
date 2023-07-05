import datetime as dt

import typer

from src.cli.async_helper import async_to_sync
from src.repos.carbon_intensity.protocol import ForecastLowIntensityDateRepo


@async_to_sync
async def run(
    within: dt.timedelta, intensity_repo: ForecastLowIntensityDateRepo
) -> None:
    best_time = await intensity_repo.get_best_time_to_run_within_period(within)
    typer.echo(best_time.isoformat())
    return
