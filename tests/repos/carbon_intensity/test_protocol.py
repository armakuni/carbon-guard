from pathlib import Path

import pytest
from httpx import URL

from src.repos.carbon_intensity.co2_signal import CO2SignalCarbonIntensityRepo
from src.repos.carbon_intensity.file import FromFileCarbonIntensityRepo
from src.repos.carbon_intensity.national_grid_eso import (
    NationalGridESOCarbonIntensityApiRepo,
)
from src.repos.carbon_intensity.protocol import (
    CurrentIntensityDataSource,
    ForecastLowIntensityDateDataSource,
    MissingParameterError,
    make_current_intensity_repo,
    make_forecast_low_intensity_date_repo,
)


class TestMakeCurrentIntensityRepo:
    def test_can_make_a_file_repository(self) -> None:
        assert isinstance(
            make_current_intensity_repo(
                data_source=CurrentIntensityDataSource.FILE,
                from_file_carbon_intensity_file_path=Path("abc"),
                national_grid_eso_carbon_intensity_api_base_url=URL(
                    "https://example.com"
                ),
                co2_signal_carbon_intensity_api_base_url=URL("https://example.com"),
                co2_signal_api_key="",
                co2_signal_country_code="",
            ),
            FromFileCarbonIntensityRepo,
        )

    def test_it_can_make_an_eso_repo(self) -> None:
        assert isinstance(
            make_current_intensity_repo(
                data_source=CurrentIntensityDataSource.NATIONAL_GRID_ESO_CARBON_INTENSITY,
                from_file_carbon_intensity_file_path=Path("abc"),
                national_grid_eso_carbon_intensity_api_base_url=URL(
                    "https://example.com"
                ),
                co2_signal_carbon_intensity_api_base_url=URL("https://example.com"),
                co2_signal_api_key="",
                co2_signal_country_code="",
            ),
            NationalGridESOCarbonIntensityApiRepo,
        )

    def test_it_can_make_an_co2_signal_repo(self) -> None:
        assert isinstance(
            make_current_intensity_repo(
                data_source=CurrentIntensityDataSource.CO2_SIGNAL,
                from_file_carbon_intensity_file_path=Path("abc"),
                national_grid_eso_carbon_intensity_api_base_url=URL(
                    "https://example.com"
                ),
                co2_signal_carbon_intensity_api_base_url=URL("https://example.com"),
                co2_signal_api_key="value here",
                co2_signal_country_code="GB",
            ),
            CO2SignalCarbonIntensityRepo,
        )

    def test_it_does_not_make_a_co2_signal_repo_without_an_api_key(self) -> None:
        with pytest.raises(MissingParameterError):
            make_current_intensity_repo(
                data_source=CurrentIntensityDataSource.CO2_SIGNAL,
                from_file_carbon_intensity_file_path=Path("abc"),
                national_grid_eso_carbon_intensity_api_base_url=URL(
                    "https://example.com"
                ),
                co2_signal_carbon_intensity_api_base_url=URL("https://example.com"),
                co2_signal_api_key="",
                co2_signal_country_code="GB",
            )

    def test_it_does_not_make_a_co2_signal_repo_without_a_country_code(self) -> None:
        with pytest.raises(MissingParameterError):
            make_current_intensity_repo(
                data_source=CurrentIntensityDataSource.CO2_SIGNAL,
                from_file_carbon_intensity_file_path=Path("abc"),
                national_grid_eso_carbon_intensity_api_base_url=URL(
                    "https://example.com"
                ),
                co2_signal_carbon_intensity_api_base_url=URL("https://example.com"),
                co2_signal_api_key="def",
                co2_signal_country_code="",
            )


class TestMakeForecastLowIntensityDateRepo:
    def test_can_make_a_file_repository(self) -> None:
        assert isinstance(
            make_forecast_low_intensity_date_repo(
                data_source=ForecastLowIntensityDateDataSource.FILE,
                from_file_carbon_intensity_file_path=Path("abc"),
                national_grid_eso_carbon_intensity_api_base_url=URL(
                    "https://example.com"
                ),
            ),
            FromFileCarbonIntensityRepo,
        )

    def test_it_can_make_an_eso_repo(self) -> None:
        assert isinstance(
            make_forecast_low_intensity_date_repo(
                data_source=ForecastLowIntensityDateDataSource.NATIONAL_GRID_ESO_CARBON_INTENSITY,
                from_file_carbon_intensity_file_path=Path("abc"),
                national_grid_eso_carbon_intensity_api_base_url=URL(
                    "https://example.com"
                ),
            ),
            NationalGridESOCarbonIntensityApiRepo,
        )
