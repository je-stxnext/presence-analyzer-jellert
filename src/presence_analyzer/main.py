# -*- coding: utf-8 -*-
"""
Flask app initialization.
"""
import os.path
from flask import Flask
from flask_mako import MakoTemplates


MAIN_DATA_CSV = os.path.join(
    os.path.dirname(__file__), '..', '..', 'runtime', 'data', 'sample_data.csv'
)

# pylint: disable=invalid-name
app = Flask(__name__, template_folder="templates")
app.config.update(
    DEBUG=True,
    DATA_CSV=MAIN_DATA_CSV
)

MakoTemplates().init_app(app)
