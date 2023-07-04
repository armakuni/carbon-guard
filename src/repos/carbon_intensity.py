class InMemoryCarbonIntensityRepo(object):
    def __init__(self, carbon_intensity: int) -> None:
        self._carbon_intensity = carbon_intensity

    def get_carbon_intensity(self) -> int:
        return self._carbon_intensity
