from datetime import datetime

from pre_process.data_frame import does_client_have_order_in_interval
from pre_process.time_intervals import TimeWindow
from test.pre_process.orders_test import Order


def test_does_client_has_order_in_interval_false():
    assert not does_client_have_order_in_interval(
        TimeWindow(
            start_time=datetime(2017, 1, 7),
            end_time=datetime(2017, 1, 8)
        ),
        [
            Order(cdate=datetime(2017, 1, 1)),
            Order(cdate=datetime(2017, 1, 6)),
            Order(cdate=datetime(2017, 1, 8))
        ]
    )


def test_does_client_has_order_in_interval_true():
    assert does_client_have_order_in_interval(
        TimeWindow(
            start_time=datetime(2017, 1, 7),
            end_time=datetime(2017, 1, 8)
        ),
        [
            Order(cdate=datetime(2017, 1, 1)),
            Order(cdate=datetime(2017, 1, 6)),
            Order(cdate=datetime(2017, 1, 7))
        ]
    )

