from typing import Protocol


class CarbonIntensityRepo(Protocol):
    async def get_carbon_intensity(self) -> int:
        ...
