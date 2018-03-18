import pandas as pd

from pre_process.orders import get_earliest_client_order
from pre_process.time_intervals import get_time_intervals, falls_in_time_interval
from pre_process.features import FeatureArgs


def does_client_have_order_in_interval(time_interval, orders):
    """
    Does at least one of the orders fall within this time interval?
    """
    return len([True for order in orders if falls_in_time_interval(time_interval, order.cdate)]) > 0


def add_client_columns(data_set):
    """
    Given a data set, add a column for each unique user and set it to 1 for that user's row(s), 0 otherwise.
    particular user.
    """
    client_ids = {}
    for row in data_set:
        client_ids[row[1]] = True

    for i in xrange(len(data_set)):
        data_set[i] = data_set[i] + [1 if client == data_set[i][1] else 0 for client in list(client_ids)]

    return data_set


def get_data_frame_columns(data_set, features, add_client_boolean_columns):
    return ['time_interval', 'client', 'output'] + \
           [str(feature.__name__) for feature in features] + \
           ([str(i) for i in xrange(len(data_set[0]) - 3 - len(features))] if add_client_boolean_columns else [])


def convert_to_dataframe(data_set, features, add_client_boolean_columns):
    """
    Turn the array into a proper pandas DataFrame.
    """
    data_frame = pd.DataFrame(
        data=data_set,
        columns=get_data_frame_columns(data_set, features, add_client_boolean_columns)
    )
    data_frame.index = data_frame.apply(lambda df_row: (df_row.time_interval, df_row.client), axis=1)
    return data_frame


def generate_line_for_time_window(time_window, client, location_id, gender, opted_in, orders, features):
    """
    Generate line of data set data. Index = time_window & client
    """
    return [
        time_window,
        client,
        does_client_have_order_in_interval(time_window, orders)
    ] + [
        feature(FeatureArgs(orders, time_window, location_id, gender, opted_in))
        for feature in features
    ]


def generate_data_set(earliest_client_orders, time_intervals, client_order_map, features):
    """
    Generate full data set. Basically, for each time_interval, add the appropriate entries into the data_set.
    """
    return sum(
        [
            [
                generate_line_for_time_window(time_window, client, orders[0].location_id, orders[0].gender, orders[0].opted_in, orders, features)
                for client, orders in client_order_map.iteritems()
                if earliest_client_orders[client] <= time_window.end_time
            ]
            for time_window in time_intervals
        ],
        []
    )


def generate_data_frames(client_order_map, start_time, end_time, time_interval, features, add_client_boolean_columns):
    """
    Generate full DataFrame.
    """
    data_set = generate_data_set(
        earliest_client_orders=get_earliest_client_order(client_order_map),
        time_intervals=get_time_intervals(start_time, end_time, time_interval),
        client_order_map=client_order_map,
        features=features
    )

    if add_client_boolean_columns:
        data_set = add_client_columns(data_set)

    return convert_to_dataframe(data_set, features, add_client_boolean_columns)


def get_X(data_frame):
    return data_frame.drop("time_interval",axis=1).drop("client",axis=1).drop("output",axis=1)


def get_y(data_frame):
    return data_frame["output"]
