from src.repos.carbon_intensity import InMemoryCarbonIntensityRepo


def test_gives_me_a_global_carbon_intensity_repo() -> None:
    repo = InMemoryCarbonIntensityRepo(carbon_intensity=7)
    assert repo.get_carbon_intensity() == 7
