import csv
import datetime as dt
from pathlib import Path


class FromFileCarbonIntensityRepo(object):
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    async def get_carbon_intensity(self) -> int:
        parsed_rows = self._read_csv()
        utcnow = dt.datetime.now(dt.UTC)

        intensity_in_present = filter(lambda x: x[0] <= utcnow, parsed_rows)
        max_date = max(intensity_in_present, key=lambda x: x[0])

        return max_date[1]

    def _read_csv(self) -> list[tuple[dt.datetime, int]]:
        with self._file_path.open("r") as file:
            raw_rows = csv.reader(file)

            return [
                (
                    dt.datetime.fromisoformat(row[0]).replace(tzinfo=dt.timezone.utc),
                    int(row[1]),
                )
                for row in raw_rows
            ]

    async def get_best_time_to_run_within_period(
        self, within: dt.timedelta
    ) -> dt.datetime:
        parsed_rows = self._read_csv()
        utcnow = dt.datetime.now(dt.UTC)

        intensity_in_future = filter(lambda x: x[0] > utcnow, parsed_rows)
        intensity_within_duratation = filter(
            lambda x: (x[0] - utcnow) <= within, intensity_in_future
        )
        cleanest_time = min(intensity_within_duratation, key=lambda x: x[1])

        return cleanest_time[0]
