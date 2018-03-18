from collections import namedtuple
from datetime import datetime

from pre_process.features import FeatureArgs, day_of_week, daily_order_frequency, \
    daily_order_frequency_per_active_restaurants_max, daily_order_frequency_per_active_restaurants_aggregate

from pre_process.time_intervals import TimeWindow

# These obj tuples represent entities parsed from the csv input files.
order_obj = namedtuple('Order', ['cdate'])


def test_day_of_week_sunday():
    # Jan 1st 2017 was a Sunday (6)
    assert 6 == day_of_week(
        FeatureArgs(
            orders=[],
            time_interval=TimeWindow(
                start_time=datetime(2017, 1, 1, 12, 0),
                end_time=datetime(2017, 1, 2, 0, 0)
            )
        )
    )


def test_day_of_week_tuesday():
    # Jan 3rd 2017 was a Tuesday (1)
    assert 1 == day_of_week(
        FeatureArgs(
            orders=[],
            time_interval=TimeWindow(
                start_time=datetime(2017, 1, 3, 0, 0),
                end_time=datetime(2017, 1, 3, 12, 0)
            )
        )
    )


def test_daily_order_frequency_one_day_max():
    """
    User ordered on the 1st, current time window is the first.
    """
    assert 1 == daily_order_frequency(
        FeatureArgs(
            orders=[
                order_obj(cdate=datetime(2017, 1, 1))
            ],
            time_interval=TimeWindow(
                start_time=datetime(2017, 1, 1, 0, 0),
                end_time=datetime(2017, 1, 1, 12, 0)
            )
        ))


def test_daily_order_frequency():
    """
    User ordered on the 1st, the 3rd, and the 17th. The current time_interval is the 24th, so we should
    get 3.0 / 24 = 0.125.
    """
    assert 0.125 == daily_order_frequency(
        FeatureArgs(
            orders=[
                order_obj(cdate=datetime(2017, 1, 1)),
                order_obj(cdate=datetime(2017, 1, 3)),
                order_obj(cdate=datetime(2017, 1, 17))
            ],
            time_interval=TimeWindow(
                start_time=datetime(2017, 1, 24, 0, 0),
                end_time=datetime(2017, 1, 24, 12, 0)
            )
        ))
