import json
import tempfile
from pathlib import Path
from typing import Generator
from urllib.parse import urlparse

import pytest
from pytest import FixtureRequest
from wiremock.constants import Config
from wiremock.resources.mappings import (
    HttpMethods,
    Mapping,
    MappingRequest,
    MappingResponse,
)
from wiremock.resources.mappings.resource import Mappings
from wiremock.server import WireMockServer

from src.repos.carbon_intensity import (
    CarbonIntensityRepo,
    FromFileCarbonIntensityRepo,
    InMemoryCarbonIntensityRepo,
    UkCarbonIntensityApiRepo,
    UkCarbonIntensityResponse,
)


@pytest.fixture(params=["inmemory", "file", "uk-carbon-intensity"])
def carbon_intensity_repo(
    request: FixtureRequest, expected_carbon_intensity: int
) -> Generator[CarbonIntensityRepo, None, None]:
    if request.param == "inmemory":
        yield InMemoryCarbonIntensityRepo(carbon_intensity=expected_carbon_intensity)
        return

    if request.param == "file":
        with tempfile.NamedTemporaryFile() as file:
            file.write(str(expected_carbon_intensity).encode("utf8"))
            file.seek(0)
            yield FromFileCarbonIntensityRepo(file_path=Path(file.name))

    if request.param == "uk-carbon-intensity":
        with WireMockServer() as wm:
            base_url = f"http://localhost:{wm.port}"
            Config.base_url = f"{base_url}/__admin"

            current_intensity = Mapping(
                priority=100,
                request=MappingRequest(
                    method=HttpMethods.GET,
                    url_path="/intensity",
                ),
                response=MappingResponse(
                    status=200,
                    body=json.dumps(
                        {
                            "data": [
                                {
                                    "from": "2023-07-04T10:00Z",
                                    "to": "2023-07-04T10:30Z",
                                    "intensity": {
                                        "forecast": 116,
                                        "actual": expected_carbon_intensity,
                                        "index": "moderate",
                                    },
                                }
                            ]
                        }
                    ),
                ),
            )

            Mappings.create_mapping(mapping=current_intensity)
            yield UkCarbonIntensityApiRepo(base_url=urlparse(base_url))

    return None


@pytest.fixture()
def expected_carbon_intensity() -> int:
    return 7


def test_gives_me_a_global_carbon_intensity_repo(
    carbon_intensity_repo: CarbonIntensityRepo, expected_carbon_intensity: int
) -> None:
    assert carbon_intensity_repo.get_carbon_intensity() == expected_carbon_intensity


def test_no_uk_carbon_intensity_data_raises() -> None:
    with pytest.raises(ValueError):
        UkCarbonIntensityResponse.model_validate_json('{"data": []}')
