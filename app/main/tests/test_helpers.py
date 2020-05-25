import datetime
import pytz

from app.main.helpers import is_even_year, primary_election_active


def test_is_even_year():
    assert is_even_year(year=2018)
    assert not is_even_year(year=2019)


def test_primary_election_active():
    deadline = "2020-05-26 17:00:00"

    # One minute before deadline
    current_time = datetime.datetime(year=2020, month=5, day=26, hour=21, minute=59, tzinfo=pytz.utc)
    assert primary_election_active(deadline, current_time) is True

    # One day before deadline
    current_time = datetime.datetime(year=2020, month=5, day=25, hour=22, minute=00, tzinfo=pytz.utc)
    assert primary_election_active(deadline, current_time) is True

    # One minute after deadline
    current_time = datetime.datetime(year=2020, month=5, day=26, hour=22, minute=1, tzinfo=pytz.utc)
    assert primary_election_active(deadline, current_time) is False

    # One day after deadline
    current_time = datetime.datetime(year=2020, month=5, day=27, hour=21, minute=59, tzinfo=pytz.utc)
    assert primary_election_active(deadline, current_time) is False
