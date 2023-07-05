import datetime as dt
import json
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from httpx import URL
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
    CO2SignalCarbonIntensityRepo,
    FromFileCarbonIntensityRepo,
    InMemoryCarbonIntensityRepo,
    NationalGridESOCarbonIntensityApiRepo,
    NationalGridESOCarbonIntensityResponse,
)


class TestCarbonIntensityRepository:
    @pytest.fixture(params=["inmemory", "file", "uk-carbon-intensity", "co2-signal"])
    def carbon_intensity_repo(
            self, request: FixtureRequest, expected_carbon_intensity: int, expected_run_time: dt.datetime
    ) -> Generator[CarbonIntensityRepo, None, None]:
        if request.param == "inmemory":
            now = dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)

            intensities = [
                (now, expected_carbon_intensity),
                (expected_run_time, 1),
                (expected_run_time + dt.timedelta(days=100), expected_carbon_intensity - 10)]
            yield InMemoryCarbonIntensityRepo(
                carbon_intensity=intensities
            )

        if request.param == "file":
            with tempfile.NamedTemporaryFile() as file:
                file.write(str(expected_carbon_intensity).encode("utf8"))
                file.seek(0)
                yield FromFileCarbonIntensityRepo(file_path=Path(file.name))

        if request.param == "uk-carbon-intensity":
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
                yield NationalGridESOCarbonIntensityApiRepo(base_url=URL(base_url))

        if request.param == "co2-signal":
            with WireMockServer(max_attempts=100) as wm:
                base_url = f"http://localhost:{wm.port}"
                Config.base_url = f"{base_url}/__admin"

                current_intensity = Mapping(
                    priority=100,
                    request=MappingRequest(
                        method=HttpMethods.GET,
                        headers={"auth-token": {"equalTo": "abcdef"}},
                        url_path="/v1/latest",
                        query_parameters={"countryCode": {"equalTo": "GB"}},
                    ),
                    response=MappingResponse(
                        status=200,
                        body=json.dumps(
                            {
                                "_disclaimer": "This data is the exclusive property of Electricity Maps",
                                "status": "ok",
                                "countryCode": "GB",
                                "data": {
                                    "datetime": "2023-07-04T16:00:00.000Z",
                                    "carbonIntensity": expected_carbon_intensity,
                                    "fossilFuelPercentage": 37.16,
                                },
                                "units": {"carbonIntensity": "gCO2eq/kWh"},
                            }
                        ),
                    ),
                )

                Mappings.create_mapping(mapping=current_intensity)
                yield CO2SignalCarbonIntensityRepo(
                    base_url=URL(base_url), api_key="abcdef", country_code="GB"
                )

        return None

    @pytest.fixture()
    def expected_carbon_intensity(self) -> int:
        return 7

    @pytest.fixture()
    def expected_run_time(self) -> dt.datetime:
        return dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc) + dt.timedelta(days=2)

    @pytest.mark.asyncio
    async def test_gives_me_a_carbon_intensity(
            self, carbon_intensity_repo: CarbonIntensityRepo, expected_carbon_intensity: int
    ) -> None:
        assert (
                await carbon_intensity_repo.get_carbon_intensity()
                == expected_carbon_intensity
        )

    @pytest.mark.asyncio
    async def test_gives_me_a_best_time_to_run(
            self, carbon_intensity_repo: CarbonIntensityRepo, expected_run_time: dt.datetime
    ) -> None:
        assert (
                await carbon_intensity_repo.get_best_time_to_run_within_period(dt.timedelta(days=2))
                == expected_run_time
        )


def test_no_uk_carbon_intensity_data_raises() -> None:
    with pytest.raises(ValueError):
        NationalGridESOCarbonIntensityResponse.model_validate_json('{"data": []}')
