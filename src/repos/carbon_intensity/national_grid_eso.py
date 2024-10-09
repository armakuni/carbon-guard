import datetime as dt
from urllib.parse import quote

from httpx import URL, AsyncClient, Timeout
from pydantic import BaseModel, Field


class NationalGridESOCarbonIntensityIntensity(BaseModel):
    actual: int | None
    forecast: int


class NationalGridESOCarbonIntensityData(BaseModel):
    intensity: NationalGridESOCarbonIntensityIntensity
    from_: dt.datetime = Field(..., alias="from")


class NationalGridESOCarbonIntensityResponse(BaseModel):
    data: list[NationalGridESOCarbonIntensityData]


class NationalGridESOCarbonIntensityApiRepo:
    def __init__(self, base_url: URL):
        self._client = AsyncClient(base_url=base_url, http2=True, timeout=Timeout(5.0))

    async def get_carbon_intensity(self) -> int:
        response = await self._client.get("/intensity")
        response.raise_for_status()

        parsed_response = NationalGridESOCarbonIntensityResponse.model_validate_json(
            response.content
        )

        if not parsed_response.data:
            raise ValueError("data is empty")

        first_item = parsed_response.data[0]

        return first_item.intensity.actual or first_item.intensity.forecast

    async def get_best_time_to_run_within_period(
        self, within: dt.timedelta
    ) -> dt.datetime:
        utcnow = dt.datetime.now(dt.UTC)
        start_time_escaped = quote(
            utcnow.isoformat(timespec="minutes").replace("+00:00", "Z"), safe=":"
        )
        end_time_escaped = quote(
            (utcnow + within).isoformat(timespec="minutes").replace("+00:00", "Z"),
            safe=":",
        )

        response = await self._client.get(
            f"/intensity/{start_time_escaped}/{end_time_escaped}"
        )
        response.raise_for_status()

        parsed_response: NationalGridESOCarbonIntensityResponse = (
            NationalGridESOCarbonIntensityResponse.model_validate_json(response.content)
        )

        lowest_intensity = min(parsed_response.data, key=lambda x: x.intensity.forecast)

        return lowest_intensity.from_
