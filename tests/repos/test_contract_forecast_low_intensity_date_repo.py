import csv
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

from src.repos.carbon_intensity.file import FromFileCarbonIntensityRepo
from src.repos.carbon_intensity.in_memory import InMemoryCarbonIntensityRepo
from src.repos.carbon_intensity.national_grid_eso import (
    NationalGridESOCarbonIntensityApiRepo,
)
from src.repos.carbon_intensity.protocol import ForecastLowIntensityDateRepo


class TestCarbonIntensityRepository:
    @pytest.fixture(params=["inmemory", "file", "uk-carbon-intensity"])
    def carbon_intensity_repo(
        self,
        request: FixtureRequest,
        expected_carbon_intensity: int,
        expected_run_time: dt.datetime,
    ) -> Generator[ForecastLowIntensityDateRepo, None, None]:
        now = dt.datetime.now(dt.UTC)

        intensities: list[tuple[dt.datetime, int]] = [
            (now, expected_carbon_intensity),
            (expected_run_time, 1),
            (expected_run_time + dt.timedelta(seconds=40), 9999999999),
            (
                expected_run_time + dt.timedelta(days=100),
                expected_carbon_intensity - 10,
            ),
        ]

        if request.param == "inmemory":
            yield InMemoryCarbonIntensityRepo(carbon_intensity=intensities)

        if request.param == "file":
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8"
            ) as named_temp_file:
                csv_writer = csv.writer(named_temp_file)

                for occurance_time, occurance_value in intensities:
                    csv_writer.writerow([occurance_time.isoformat(), occurance_value])

                named_temp_file.seek(0)
                yield FromFileCarbonIntensityRepo(file_path=Path(named_temp_file.name))

        if request.param == "uk-carbon-intensity":
            with WireMockServer(max_attempts=100) as wm:
                base_url = f"http://localhost:{wm.port}"
                self.uk_carbon_intensity_fixture(
                    base_url, expected_carbon_intensity, intensities
                )
                yield NationalGridESOCarbonIntensityApiRepo(base_url=URL(base_url))

        return None

    def uk_carbon_intensity_fixture(
        self,
        base_url: str,
        expected_carbon_intensity: int,
        expected_run_intensities: list[tuple[dt.datetime, int]],
    ) -> None:
        Config.base_url = f"{base_url}/__admin"
        response_array = []
        for run_date, run_actual in expected_run_intensities:
            actual = run_actual if run_date <= dt.datetime.now(dt.UTC) else None
            expected = run_actual if run_date > dt.datetime.now(dt.UTC) else -99
            from_date = run_date.isoformat()
            to_date = (run_date + dt.timedelta(minutes=30)).isoformat()
            data_item = {
                "from": from_date,
                "to": to_date,
                "intensity": {
                    "forecast": expected,
                    "actual": actual,
                    "index": "moderate",
                },
            }
            response_array.append(data_item)
        current_intensity = Mapping(
            priority=100,
            request=MappingRequest(
                method=HttpMethods.GET,
                url_path_pattern="/intensity/[^/]+/[^/]+",
            ),
            response=MappingResponse(
                status=200,
                body=json.dumps({"data": response_array[1:2]}),
            ),
        )
        Mappings.create_mapping(mapping=current_intensity)

    @pytest.fixture()
    def expected_carbon_intensity(self) -> int:
        return 7

    @pytest.fixture()
    def expected_run_time(self) -> dt.datetime:
        return dt.datetime.now(dt.UTC) + dt.timedelta(days=2)

    @pytest.mark.asyncio
    async def test_gives_me_a_best_time_to_run(
        self,
        carbon_intensity_repo: ForecastLowIntensityDateRepo,
        expected_run_time: dt.datetime,
    ) -> None:
        assert (
            await carbon_intensity_repo.get_best_time_to_run_within_period(
                dt.timedelta(days=2)
            )
            == expected_run_time
        )
