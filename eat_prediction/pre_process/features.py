from lunch_club import format_time
from datetime import timedelta
from collections import namedtuple

FeatureArgs = namedtuple('FeatureArgs', [
        'orders', 
        'time_interval',
        'location_id',
        'gender',
        'opted_in'
    ])


def day_of_week(feature_args):
    """
    What's the day of the week for the given time interval? 6 == Sunday, 0 == Monday
    """
    return feature_args.time_interval.start_time.weekday()


def daily_order_frequency(feature_args):
    """
    What's the daily order frequency from the time of his first order until the current time?
    
    e.g.
    orders: [2016-05-05, 2016-05-07]
    time window: [2016-05-07]
    freq: 2/3
    """
    first_order = min(feature_args.orders, key=lambda order : order.cdate)
    days_from_first_to_now = (feature_args.time_interval.start_time - first_order.cdate).days + 1
    return 1.0 * len(feature_args.orders) / days_from_first_to_now if days_from_first_to_now > 0 else 0


def straight_location(feature_args):
    return feature_args.location_id


def opted_in(feature_args):
    return feature_args.opted_in


def gender(feature_args):
    """
    -1 for male, 1 for female, 0 for not sure
    """
    if has_gender(feature_args) == 0:
        return 0

    return -1 if feature_args.gender == 'M' else 1

def has_gender(feature_args):
    """
    0 for no, 1 for yes!
    """
    return 1 if feature_args.gender == feature_args.gender else 0
