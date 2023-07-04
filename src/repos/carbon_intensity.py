from pathlib import Path
from typing import Protocol


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
