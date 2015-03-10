# -*- coding: utf-8 -*-
""" Helper functions used in views. """

import csv
from datetime import datetime
from datetime import timedelta
from functools import wraps
from itertools import groupby
from json import dumps
from operator import itemgetter


from flask import Response

from presence_analyzer.main import app

import logging
log = logging.getLogger(__name__)  # pylint: disable=invalid-name


def jsonify(function):
    """
    Creates a response with the JSON representation of wrapped function result.
    """
    @wraps(function)
    def inner(*args, **kwargs):
        """ This docstring will be overridden by @wraps decorator. """
        return Response(
            dumps(function(*args, **kwargs)),
            mimetype='application/json'
        )
    return inner


def get_data():
    """
    Extracts presence data from CSV file and groups it by user_id.

    It creates structure like this:
    data = {
        'user_id': {
            datetime.date(2013, 10, 1): {
                'start': datetime.time(9, 0, 0),
                'end': datetime.time(17, 30, 0),
            },
            datetime.date(2013, 10, 2): {
                'start': datetime.time(8, 30, 0),
                'end': datetime.time(16, 45, 0),
            },
        }
    }
    """
    data = {}
    with open(app.config['DATA_CSV'], 'r') as csvfile:
        presence_reader = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(presence_reader):
            if len(row) != 4:
                # ignore header and footer lines
                continue

            try:
                user_id = int(row[0])
                date = datetime.strptime(row[1], '%Y-%m-%d').date()
                start = datetime.strptime(row[2], '%H:%M:%S').time()
                end = datetime.strptime(row[3], '%H:%M:%S').time()
            except (ValueError, TypeError):
                log.debug('Problem with line %d: ', i, exc_info=True)

            data.setdefault(user_id, {})[date] = {'start': start, 'end': end}

    return data


def group_by_weekday(items):
    """ Groups presence entries by weekday. """
    result = [[], [], [], [], [], [], []]  # one list for every day in week
    for date in items:
        start = items[date]['start']
        end = items[date]['end']
        result[date.weekday()].append(interval(start, end))
    return result


def seconds_since_midnight(time):
    """ Calculates amount of seconds since midnight. """
    return time.hour * 3600 + time.minute * 60 + time.second


def interval(start, end):
    """ Calculates inverval in seconds between two datetime.time objects. """
    return seconds_since_midnight(end) - seconds_since_midnight(start)


def mean(items):
    """ Calculates arithmetic mean. Returns zero for empty lists. """
    return float(sum(items)) / len(items) if len(items) > 0 else 0


def group_by_start_end_means(items):
    """ Groups presence entries by means of start and end times. """
    start_end_times = [{'day': date.weekday(),
                        'start': seconds_since_midnight(time_['start']),
                        'end': seconds_since_midnight(time_['end'])}
                       for (date, time_) in items.viewitems()]
    start_end_times = sorted(start_end_times,
                             lambda d1, d2: cmp(d1['day'], d2['day']))
    start_means = group_time_means(start_end_times, 'start')
    end_means = group_time_means(start_end_times, 'end')

    return [(get_time_from_seconds(s), get_time_from_seconds(e))
            for s, e in zip(start_means, end_means)]


def group_time_means(times, time_field):
    """
    Calculates mean if a time collection.
    Requires data sorted by a day identifier.
    """
    get_day = itemgetter('day')
    means = [0] * 7
    for key, group in groupby(times, get_day):
        means[key] = int(mean(list(item[time_field] for item in group)))
    return means


def get_time_from_seconds(seconds):
    """ Calculates time from seconds. """
    return [int(e) for e in str(timedelta(seconds=seconds)).split(':')]
