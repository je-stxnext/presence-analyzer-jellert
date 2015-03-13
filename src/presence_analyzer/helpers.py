# -*- coding: utf-8 -*-
"""
Helper functions used in templates.
"""
import ConfigParser
import os

INI_FILENAME = os.path.join(os.path.dirname(__file__),
                            '..', '..', 'runtime', 'debug.ini')


def get_users_xml_file():
    """ Get users xml file location from configuration file. """
    config = ConfigParser.ConfigParser()
    config.readfp(open(INI_FILENAME))
    return config.get("users", "users_xml_file")


def get_users_url():
    """ Get users xml url address from configuration file. """
    config = ConfigParser.ConfigParser()
    config.readfp(open(INI_FILENAME))
    return config.get("users", "users_url")
