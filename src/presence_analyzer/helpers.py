# -*- coding: utf-8 -*-
"""
Helper functions used in templates.
"""
import ConfigParser
import os


def get_users_xml_file():
    """ Get users xml file location from configuration file. """
    ini_filename = os.path.join(os.path.dirname(__file__),
                                '..', '..', 'runtime', 'debug.ini')
    config = ConfigParser.ConfigParser()
    config.readfp(open(ini_filename))
    return config.get("users", "users_xml_file")
