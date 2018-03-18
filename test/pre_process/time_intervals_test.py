from datetime import datetime
from datetime import timedelta

from pre_process.time_intervals import falls_in_time_interval, TimeWindow, get_time_intervals


def test_falls_in_time_interval_true_at_start_time():
    assert falls_in_time_interval(
        TimeWindow(datetime(2017, 1, 1), datetime(2017, 1, 2)),
        datetime(2017, 1, 1)
    )

def test_falls_in_time_interval_false_at_end_time():
    assert not falls_in_time_interval(
        TimeWindow(datetime(2017, 1, 1), datetime(2017, 1, 2)),
        datetime(2017, 1, 2)
    )

def test_falls_in_time_interval_true():
    assert falls_in_time_interval(
        TimeWindow(datetime(2017, 1, 1), datetime(2017, 1, 2)),
        datetime(2017, 1, 1, 5, 1)
    )

def test_get_time_intervals_two_days():
    assert \
        [
            TimeWindow(
                start_time=datetime(2017, 1, 1, 0, 0),
                end_time=datetime(2017, 1, 1, 12, 0)
            ),
            TimeWindow(
                start_time=datetime(2017, 1, 1, 12, 0),
                end_time=datetime(2017, 1, 2, 0, 0)
            ),
            TimeWindow(
                start_time=datetime(2017, 1, 2, 0, 0),
                end_time=datetime(2017, 1, 2, 12, 0)
            ),
            TimeWindow(
                start_time=datetime(2017, 1, 2, 12, 0),
                end_time=datetime(2017, 1, 3, 0, 0)
            )
        ] == get_time_intervals(
            datetime(2017, 1, 1),
            datetime(2017, 1, 3),
            timedelta(hours=12)
        )

def test_get_time_intervals_18_hour_blocks():
    assert \
        [
            TimeWindow(
                start_time=datetime(2017, 1, 1, 0, 0),
                end_time=datetime(2017, 1, 1, 18, 0)
            ),
            TimeWindow(
                start_time=datetime(2017, 1, 1, 18, 0),
                end_time=datetime(2017, 1, 2, 12, 0)
            ),
            TimeWindow(
                start_time=datetime(2017, 1, 2, 12, 0),
                end_time=datetime(2017, 1, 3, 6, 0)
            ),
            TimeWindow(
                start_time=datetime(2017, 1, 3, 6, 0),
                end_time=datetime(2017, 1, 4, 0, 0)
            )
        ] == get_time_intervals(
            datetime(2017, 1, 1),
            datetime(2017, 1, 4),
            timedelta(hours=18)
        )
