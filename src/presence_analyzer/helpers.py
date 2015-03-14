# -*- coding: utf-8 -*-
"""
Helper functions used in templates.
"""
import ConfigParser
import logging
import os
import urllib

INI_FILENAME = os.path.join(os.path.dirname(__file__),
                            '..', '..', 'runtime', 'debug.ini')

LOG = logging.getLogger(__name__)


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


def save_users_from_www():
    """ Get users xml url address from configuration file. """
    url_file = get_users_url()
    if url_file:
        filename = urllib.urlretrieve(url_file)[0]
        with open(filename) as _file:
            if [line for line in _file.readlines() if '<users>' in line]:
                xml_file = get_users_xml_file()
                if xml_file:
                    try:
                        with open(filename) as _filename:
                            with open(xml_file, 'w') as _xml_file:
                                _xml_file.writelines(_filename.readlines())
                            return True
                    except IOError:
                        LOG.debug("Problem during creation of %s file ! ",
                                  xml_file, exc_info=True)
            else:
                LOG.debug('Improper users xml file !', exc_info=True)
    return False
