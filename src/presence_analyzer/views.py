# -*- coding: utf-8 -*-
"""
Defines views.
"""

import calendar
from flask import abort, redirect
from flask.ext.mako import render_template
#from mako.template import Template

from presence_analyzer.main import app
from presence_analyzer.main import mako
from presence_analyzer.utils import jsonify, get_data, mean, group_by_weekday,\
    group_by_start_end_means

import logging
log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@app.route('/')
def mainpage():
    """ Redirects to front page. """
    return render_template('presence_weekday.html', name='mako')
    #return redirect('/static/presence_weekday_old.html')


@app.route('/api/v1/users', methods=['GET'])
@jsonify
def users_view():
    """ Users listing for dropdown. """
    data = get_data()
    return [
        {'user_id': i, 'name': 'User {0}'.format(str(i))}
        for i in data.keys()
    ]


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


@app.route('/api/v1/base_template/<int:user_id>', methods=['GET', 'POST'])
def base_template_view(user_id):
    """ view using test template """
    data = get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    #template = mako.Template(filename="base_template.html")
    #return template.render(user_id=user_id)
    return render_template('base_template.html', name='mako', user_id=user_id)
