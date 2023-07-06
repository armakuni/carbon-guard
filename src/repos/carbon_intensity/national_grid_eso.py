from httpx import URL, AsyncClient
from pydantic import BaseModel, field_validator


class NationalGridESOCarbonIntensityIntensity(BaseModel):
    actual: int


class NationalGridESOCarbonIntensityData(BaseModel):
    intensity: NationalGridESOCarbonIntensityIntensity


class NationalGridESOCarbonIntensityResponse(BaseModel):
    data: list[NationalGridESOCarbonIntensityData]

    @field_validator("data")
    def ensure_data_is_not_empty(
        cls, v: list[NationalGridESOCarbonIntensityData]
    ) -> list[NationalGridESOCarbonIntensityData]:
        if not v:
            raise ValueError("data is empty")

        return v


class NationalGridESOCarbonIntensityApiRepo:
    def __init__(self, base_url: URL):
        self._client = AsyncClient(base_url=base_url, http2=True)

    async def get_carbon_intensity(self) -> int:
        response = await self._client.get("/intensity")
        response.raise_for_status()

        parsed_response = NationalGridESOCarbonIntensityResponse.model_validate_json(
            response.content
        )

        return parsed_response.data[0].intensity.actual
