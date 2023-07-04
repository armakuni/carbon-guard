from pathlib import Path

import typer
from typing_extensions import Annotated

from src.repos.carbon_intensity import FromFileCarbonIntensityRepo


def main(
    max_carbon_intensity: Annotated[
        int, typer.Option(help="Set the max carbon intensity in gCO2eq/kWh.")
    ]
) -> None:
    file_intensity_repo = FromFileCarbonIntensityRepo(Path(".carbon_intensity"))
    if file_intensity_repo.get_carbon_intensity() > max_carbon_intensity:
        typer.echo("Carbon levels exceed threshold, skipping.")
        raise typer.Exit(1)

    typer.echo("Carbon levels under threshold, proceeding.")


def run() -> None:
    typer.run(main)
