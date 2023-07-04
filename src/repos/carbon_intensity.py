from pathlib import Path
from typing import Protocol

from httpx import URL, Client
from pydantic import BaseModel, field_validator


class CarbonIntensityRepo(Protocol):
    def get_carbon_intensity(self) -> int:
        ...


class InMemoryCarbonIntensityRepo(object):
    def __init__(self, carbon_intensity: int) -> None:
        self._carbon_intensity = carbon_intensity

    def get_carbon_intensity(self) -> int:
        return self._carbon_intensity


class FromFileCarbonIntensityRepo(object):
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def get_carbon_intensity(self) -> int:
        return int(self._file_path.read_text(encoding="utf8"))


class UkCarbonIntensityIntensity(BaseModel):
    actual: int


class UkCarbonIntensityData(BaseModel):
    intensity: UkCarbonIntensityIntensity


class UkCarbonIntensityResponse(BaseModel):
    data: list[UkCarbonIntensityData]

    @field_validator("data")
    def ensure_data_is_not_empty(
        cls, v: list[UkCarbonIntensityData]
    ) -> list[UkCarbonIntensityData]:
        if not v:
            raise ValueError("data is empty")

        return v


class UkCarbonIntensityApiRepo:
    def __init__(self, base_url: URL):
        self._client = Client(base_url=base_url, http2=True)

    def get_carbon_intensity(self) -> int:
        response = self._client.get("/intensity")
        response.raise_for_status()

        parsed_reponse = UkCarbonIntensityResponse.model_validate_json(response.content)

        return parsed_reponse.data[0].intensity.actual
