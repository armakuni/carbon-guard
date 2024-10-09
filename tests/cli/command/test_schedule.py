import datetime as dt

from pytest import CaptureFixture

from src.cli.command import schedule
from src.repos.carbon_intensity.in_memory import InMemoryCarbonIntensityRepo


def test_schedule(capsys: CaptureFixture[str]) -> None:
    now = dt.datetime.now(dt.UTC)
    tomorrow = now + dt.timedelta(days=1)
    overmorrow = now + dt.timedelta(days=2)
    day_after_overmorrow = now + dt.timedelta(days=3)

    repo = InMemoryCarbonIntensityRepo(
        [(now, 300), (tomorrow, 200), (overmorrow, 100), (day_after_overmorrow, 50)]
    )
    schedule.run(within=dt.timedelta(days=2), intensity_repo=repo)
    assert capsys.readouterr().out == f"{overmorrow.isoformat()}\n"
