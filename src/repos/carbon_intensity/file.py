from pathlib import Path


class FromFileCarbonIntensityRepo(object):
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    async def get_carbon_intensity(self) -> int:
        return int(self._file_path.read_text(encoding="utf8"))
