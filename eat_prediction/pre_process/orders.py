import pandas as pd


def get_client_order_map(orders, minimum_visits, end_time):
    """
    Create map of client -> list of order rows. This is where we filter out any low frequency users.
    """
    return filter_out_low_frequency_users(
        client_order_map=build_order_map(
            convert_cdates(
                orders=orders
            )
        ),
        end_time=end_time,
        minimum_visits=minimum_visits
    )


def convert_cdates(orders):
    """
    Convert string dates to real datetimes.
    """
    orders.cdate = pd.to_datetime(orders.cdate, unit='s')
    return orders


def build_order_map(orders):
    """
    Build a map of clients -> list of order rows.
    """
    client_map = {}

    for order in orders.itertuples():
        if order.client in client_map:
            client_map[order.client].append(order)
        else:
            client_map[order.client] = [order]
    return client_map


def get_earliest_client_order(client_order_map):
    """
    Build a map of client -> earliest order date.

    We use this so that we don't add dataframes for users before they ever place an order.
    """
    return {
        client : min([order.cdate for order in orders])
        for client, orders in client_order_map.iteritems()
    }


def days_from_first_order(orders, end_time):
    """
    How many days have passed from the first order until today (end_time).

    Don't pass back 0 - default to 1 otherwise.
    """
    days = (end_time - min(orders, key=lambda order : order.cdate).cdate).days
    return days if days > 0 else 1


def filter_out_low_frequency_users(client_order_map, end_time, minimum_visits):
    """
    Let's ignore users who don't order all that frequently.
    """
    return {
        client : orders
        for client, orders in client_order_map.iteritems()
        if len(orders) >= minimum_visits
    }


