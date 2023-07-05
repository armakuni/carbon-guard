import json
from typing import Generator

import pytest
from httpx import URL
from wiremock.constants import Config
from wiremock.resources.mappings import (
    HttpMethods,
    Mapping,
    MappingRequest,
    MappingResponse,
)
from wiremock.resources.mappings.resource import Mappings
from wiremock.server import WireMockServer

from src.repos.carbon_intensity.national_grid_eso import (
    NationalGridESOCarbonIntensityApiRepo,
)


@pytest.fixture()
def uk_carbon_intensity_repo_with_no_data() -> (
    Generator[NationalGridESOCarbonIntensityApiRepo, None, None]
):
    with WireMockServer(max_attempts=100) as wm:
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
                body=json.dumps({"data": []}),
            ),
        )
        Mappings.create_mapping(mapping=current_intensity)
        subject = NationalGridESOCarbonIntensityApiRepo(base_url=URL(base_url))

        yield subject


@pytest.mark.asyncio
async def test_raises_when_no_data(
    uk_carbon_intensity_repo_with_no_data: NationalGridESOCarbonIntensityApiRepo,
) -> None:
    with pytest.raises(ValueError):
        await uk_carbon_intensity_repo_with_no_data.get_carbon_intensity()


@pytest.fixture()
def uk_carbon_intensity_repo_with_only_forecast_data() -> (
    Generator[NationalGridESOCarbonIntensityApiRepo, None, None]
):
    with WireMockServer(max_attempts=100) as wm:
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
                                    "forecast": 7,
                                    "actual": None,
                                    "index": "moderate",
                                },
                            }
                        ]
                    }
                ),
            ),
        )
        Mappings.create_mapping(mapping=current_intensity)
        subject = NationalGridESOCarbonIntensityApiRepo(base_url=URL(base_url))

        yield subject


@pytest.mark.asyncio
async def test_falls_back_to_forecast_data(
    uk_carbon_intensity_repo_with_only_forecast_data: NationalGridESOCarbonIntensityApiRepo,
) -> None:
    assert (
        await uk_carbon_intensity_repo_with_only_forecast_data.get_carbon_intensity()
        == 7
    )
