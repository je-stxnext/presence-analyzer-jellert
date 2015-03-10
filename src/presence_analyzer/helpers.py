# -*- coding: utf-8 -*-
"""
Helper functions used in templates.
"""
from flask import render_template
from presence_analyzer.main import app


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
