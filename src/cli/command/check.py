import typer

from src.cli.async_helper import async_to_sync
from src.repos.carbon_intensity.protocol import CurrentCarbonIntensityRepo

SUCCESS_TEMPLATE: str = "Carbon intensity is {carbon_intensity} gCO2eq/kWh, which is below or equal to the max of {max_carbon_intensity} gCO2eq/kWh"
FAILURE_TEMPLATE: str = "Carbon intensity is {carbon_intensity} gCO2eq/kWh, which is above the max of {max_carbon_intensity} gCO2eq/kWh"


@async_to_sync
async def run(
    max_carbon_intensity: int,
    advise_only: bool,
    intensity_repo: CurrentCarbonIntensityRepo,
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
