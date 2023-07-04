import tempfile
from pathlib import Path
from typing import Generator

import pytest
from pytest import FixtureRequest

from src.repos.carbon_intensity import (
    CarbonIntensityRepo,
    FromFileCarbonIntensityRepo,
    InMemoryCarbonIntensityRepo,
)


@pytest.fixture(params=["inmemory", "file"])
def carbon_intensity_repo(
    request: FixtureRequest, expected_carbon_intensity: int
) -> Generator[CarbonIntensityRepo, None, None]:
    if request.param == "inmemory":
        yield InMemoryCarbonIntensityRepo(carbon_intensity=expected_carbon_intensity)
        return

    with tempfile.NamedTemporaryFile() as file:
        file.write(str(expected_carbon_intensity).encode("utf8"))
        file.seek(0)
        yield FromFileCarbonIntensityRepo(file_path=Path(file.name))


@pytest.fixture()
def expected_carbon_intensity() -> int:
    return 7


def test_gives_me_a_global_carbon_intensity_repo(
    carbon_intensity_repo: CarbonIntensityRepo, expected_carbon_intensity: int
) -> None:
    assert carbon_intensity_repo.get_carbon_intensity() == expected_carbon_intensity
