# -*- coding: utf-8 -*-
"""
Defines views.
"""

import calendar
import logging

from flask import abort
from flask import redirect
from flask_mako import render_template

from presence_analyzer.main import app
from presence_analyzer.utils import get_data
from presence_analyzer.utils import group_by_start_end_means
from presence_analyzer.utils import group_by_weekday
from presence_analyzer.utils import get_users_from_xml
from presence_analyzer.utils import mean
from presence_analyzer.utils import jsonify

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@app.route('/')
def mainpage():
    """ Redirects to front page. """
    return redirect('/static/presence_weekday.html')


@app.route('/api/v1/users', methods=['GET'])
@jsonify
def users_view():
    """ Users listing for dropdown. """
    data = get_users_from_xml()
    data = [{'user_id': user_id, 'name': item.get('name')}
            for user_id, item in data.items()]
    return sorted(data,
                  lambda item1, item2: cmp(item1.get("name"),
                                           item2.get("name")))


@app.route('/api/v1/mean_time_weekday/<int:user_id>', methods=['GET'])
@jsonify
def mean_time_weekday_view(user_id):
    """ Returns mean presence time of given user grouped by weekday. """
    data = get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    weekdays = group_by_weekday(data[user_id])
    return [
        (calendar.day_abbr[weekday], mean(intervals))
        for weekday, intervals in enumerate(weekdays)
    ]


@app.route('/api/v1/presence_weekday/<int:user_id>', methods=['GET'])
@jsonify
def presence_weekday_view(user_id):
    """ Returns total presence time of given user grouped by weekday. """
    data = get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    weekdays = group_by_weekday(data[user_id])
    result = [
        (calendar.day_abbr[weekday], sum(intervals))
        for weekday, intervals in enumerate(weekdays)
    ]

    result.insert(0, ('Weekday', 'Presence (s)'))
    return result


@app.route('/api/v1/presence_start_end/<int:user_id>', methods=['GET'])
@jsonify
def presence_start_end_view(user_id):
    """
    Returns presence of start and end mean time period of given user grouped by
    weekday.
    """
    data = get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    start_end_means = group_by_start_end_means(data[user_id])
    return [
        (calendar.day_abbr[weekday], intervals[0], intervals[1])
        for weekday, intervals in enumerate(start_end_means)
    ]


@app.route('/static/mean_time_weekday.html', methods=['GET'])
def mean_time_weekday_template_view():
    """ view using mean time template """
    return render_template('mean_time_weekday.html', name='mako')


@app.route('/static/presence_weekday.html', methods=['GET'])
def presence_weekday_template_view():
    """ view using presence template """
    return render_template('presence_weekday.html', name='mako')


@app.route('/static/presence_start_end.html', methods=['GET'])
def presence_start_end_template_view():  # pylint: disable=invalid-name
    """ view using presence start and template """
    return render_template('presence_start_end.html', name='mako')
