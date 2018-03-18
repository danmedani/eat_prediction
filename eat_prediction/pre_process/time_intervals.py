from collections import namedtuple

TimeWindow = namedtuple('TimeWindow', ['start_time', 'end_time'])


def get_time_intervals(start_time, end_time, time_interval):
    """
    Given start & end times, and a time_interval, generate all time intervals in between.
    """
    time_intervals = []

    time = start_time
    while time < end_time:
        time_intervals.append(TimeWindow(time, time + time_interval))
        time = time + time_interval

    return time_intervals


def falls_in_time_interval(time_interval, time):
    """
    Does this time fall within this time_interval?
    """
    return time >= time_interval.start_time and time < time_interval.end_time
