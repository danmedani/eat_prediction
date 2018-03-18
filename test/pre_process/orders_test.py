from collections import namedtuple
from datetime import datetime

import pandas as pd

from pre_process.orders import build_order_map, convert_cdates, get_earliest_client_order, \
    filter_out_low_frequency_users, days_from_first_order, get_client_order_map

Order = namedtuple('Order', ['cdate'])


def test_build_order_map():
    order_map = build_order_map(
        pd.DataFrame(
            data=[
                ['client_A', 10, '2017-01-14'],
                ['client_B', 20, '2017-01-12'],
                ['client_A', 15, '2017-02-09']
            ],
            columns=['client', 'order_id', 'cdate']
        )
    )

    assert len(order_map) == 2
    assert order_map['client_B'][0].cdate == '2017-01-12'


def test_convert_cdates():
    data_frame = pd.DataFrame(
        data=[
            ['client_A', 10, '2017-01-14'],
            ['client_B', 20, '2017-01-12'],
            ['client_A', 15, '2017-02-09']
        ],
        columns=['client', 'order_id', 'cdate'])

    converted_cdates = convert_cdates(data_frame).cdate
    assert len(converted_cdates) == 3
    assert converted_cdates[0] == datetime(2017, 1, 14)
    assert converted_cdates[1] == datetime(2017, 1, 12)
    assert converted_cdates[2] == datetime(2017, 2, 9)


def test_convert_cdates():
    data_frame = pd.DataFrame(
        data=[
            ['client_A', 10, '2017-01-14'],
            ['client_B', 20, '2017-01-12'],
            ['client_A', 15, '2017-02-09']
        ],
        columns=['client', 'order_id', 'cdate'])

    converted_cdates = convert_cdates(data_frame).cdate
    assert len(converted_cdates) == 3
    assert converted_cdates[0] == datetime(2017, 1, 14)
    assert converted_cdates[1] == datetime(2017, 1, 12)
    assert converted_cdates[2] == datetime(2017, 2, 9)


def test_get_earliest_client_order():
    client_order_map = {
        'client_A': [
            Order(cdate=datetime(2017, 1, 1)),
            Order(cdate=datetime(2016, 8, 1))
        ],
        'client_B': [
            Order(cdate=datetime(2017, 4, 1))
        ]
    }
    assert {
        'client_A': datetime(2016, 8, 1),
        'client_B': datetime(2017, 4, 1)
        } == get_earliest_client_order(client_order_map)


def test_days_from_first_order_month():
    assert 31 == days_from_first_order(
        [
            Order(cdate=datetime(2017, 1, 1)),
            Order(cdate=datetime(2017, 1, 6)),
            Order(cdate=datetime(2017, 1, 8))
        ],
        datetime(2017, 2, 1)
    )


def test_days_from_first_order_one_day():
    assert 1 == days_from_first_order(
        [
            Order(cdate=datetime(2017, 1, 31))
        ],
        datetime(2017, 2, 1)
    )


def test_days_from_first_order_zero_day():
    assert 1 == days_from_first_order(
        [
            Order(cdate=datetime(2017, 2, 1))
        ],
        datetime(2017, 2, 1)
    )


def test_filter_out_low_frequency_users():
    """
    Let's say:
        client A ordered 5 times in the last 2 months, frequency = 2.5 / month
        client B ordered 2 times in the last 13 days, frequency = 2.3 / month
        client C ordered 5 times in the last 3 months, frequency = 1.66 / month
    Filter out client C, because our cutoff is 2.
    """
    end_time = datetime(2017, 2, 1)

    client_order_map = {
        'client_A': [
            Order(cdate=datetime(2016, 12, 1)),
            Order(cdate=datetime(2016, 12, 5)),
            Order(cdate=datetime(2017, 1, 5)),
            Order(cdate=datetime(2017, 1, 6)),
            Order(cdate=datetime(2017, 1, 8))
        ],
        'client_B': [
            Order(cdate=datetime(2017, 1, 14)),
            Order(cdate=datetime(2017, 1, 19))
        ],
        'client_C': [
            Order(cdate=datetime(2016, 11, 1)),
            Order(cdate=datetime(2016, 12, 1)),
            Order(cdate=datetime(2017, 1, 5)),
            Order(cdate=datetime(2017, 1, 6)),
            Order(cdate=datetime(2017, 1, 8))
        ]
    }

    filtered_set = filter_out_low_frequency_users(
        client_order_map=client_order_map,
        end_time=end_time,
        minimum_visits=2
    )
    assert len(filtered_set) == 2
    assert 'client_A' in filtered_set
    assert 'client_B' in filtered_set
    assert 'client_C' not in filtered_set


def test_filter_out_low_frequency_users_one_day():
    """
    If from user's first order until today has only been one day, make sure we don't filter.
    """
    end_time = datetime(2017, 2, 2)

    client_order_map = {
        'client_A': [
            Order(cdate=datetime(2017, 2, 1))
        ],
        'client_B': [
            Order(cdate=datetime(2017, 2, 2))
        ]
    }

    filtered_set = filter_out_low_frequency_users(
        client_order_map=client_order_map,
        end_time=end_time,
        minimum_visits=1
    )
    assert len(filtered_set) == 2
    assert 'client_A' in filtered_set
    assert 'client_B' in filtered_set
    assert 'client_C' not in filtered_set


def test_get_client_order_map():
    data_frame = pd.DataFrame(
        data=[
            ['client_A', 10, '2017-01-14'],
            ['client_B', 20, '2017-01-12'],
            ['client_A', 15, '2017-02-09']
        ],
        columns=['client', 'order_id', 'cdate'])

    client_order_map = get_client_order_map(
        orders=data_frame,
        minimum_visits=2,
        end_time=datetime(2017, 2, 1)
    )

    assert len(client_order_map) == 1
    assert len(client_order_map['client_A']) == 2
    assert client_order_map['client_A'][0].client == 'client_A'
    assert client_order_map['client_A'][0].cdate == datetime(2017, 1, 14)
