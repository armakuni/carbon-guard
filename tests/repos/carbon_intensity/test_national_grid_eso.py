import pytest

from src.repos.carbon_intensity.national_grid_eso import (
    NationalGridESOCarbonIntensityResponse,
)


def test_no_uk_carbon_intensity_data_raises() -> None:
    with pytest.raises(ValueError):
        NationalGridESOCarbonIntensityResponse.model_validate_json('{"data": []}')
