import datetime as dt


class InMemoryCarbonIntensityRepo:
    def __init__(self, carbon_intensity: list[tuple[dt.datetime, int]]) -> None:
        self._carbon_intensity = carbon_intensity

    async def get_carbon_intensity(self) -> int:
        intensity = self._carbon_intensity
        utcnow = dt.datetime.now(dt.UTC)

        intensity_in_present = filter(lambda x: x[0] <= utcnow, intensity)
        max_date = max(intensity_in_present, key=lambda x: x[0])

        return max_date[1]

    async def get_best_time_to_run_within_period(
        self, within: dt.timedelta
    ) -> dt.datetime:
        intensity = self._carbon_intensity
        utcnow = dt.datetime.now(dt.UTC)

        intensity_in_future = filter(lambda x: x[0] > utcnow, intensity)
        intensity_within_duratation = filter(
            lambda x: (x[0] - utcnow) <= within, intensity_in_future
        )
        cleanest_time = min(intensity_within_duratation, key=lambda x: x[1])

        return cleanest_time[0]
