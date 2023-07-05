import typer

from src.cli.async_helper import async_to_sync
from src.main import FAILURE_TEMPLATE, SUCCESS_TEMPLATE
from src.repos.carbon_intensity import CarbonIntensityRepo


@async_to_sync
async def run(
        max_carbon_intensity: int,
        advise_only: bool,
        intensity_repo: CarbonIntensityRepo,
) -> None:
    carbon_intensity = await intensity_repo.get_carbon_intensity()
    if carbon_intensity > max_carbon_intensity:
        typer.echo(
            FAILURE_TEMPLATE.format(
                max_carbon_intensity=max_carbon_intensity,
                carbon_intensity=carbon_intensity,
            )
        )
        raise typer.Exit(1 if not advise_only else 0)
    typer.echo(
        SUCCESS_TEMPLATE.format(
            max_carbon_intensity=max_carbon_intensity, carbon_intensity=carbon_intensity
        )
    )
