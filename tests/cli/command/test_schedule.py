import datetime as dt

import src.cli.command.schedule
from src.cli import command
from src.repos.carbon_intensity import InMemoryCarbonIntensityRepo


def test_schedule(capsys) -> None:
    now = dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)
    tomorrow = now + dt.timedelta(days=1)
    overmorrow = now + dt.timedelta(days=2)
    day_after_overmorrow = now + dt.timedelta(days=3)

    repo = InMemoryCarbonIntensityRepo([(now, 300), (tomorrow, 200), (overmorrow, 100), (day_after_overmorrow, 50)])
    command.schedule.run(within=dt.timedelta(days=2), intensity_repo=repo)
    assert capsys.readouterr().out == f"{overmorrow.isoformat()}\n"
